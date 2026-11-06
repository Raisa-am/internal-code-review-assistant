from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.database.db import get_db
from app.services.diff_parser import parse_unified_diff, DiffError
from app.services.rule_analyzer import analyze_changes
from app.services.suggestion_manager import prepare_suggestions

review_bp = Blueprint("review", __name__)

@review_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        diff_text = request.form.get("diff_text", "")
        uploaded = request.files.get("diff_file")
        filename = "pasted.diff"
        if uploaded and uploaded.filename:
            filename = secure_filename(uploaded.filename)
            if not filename.lower().endswith((".diff", ".patch", ".txt")):
                flash("Unsupported file type. Upload .diff, .patch or .txt.", "error")
                return redirect(url_for("review.index"))
            try:
                diff_text = uploaded.read(2 * 1024 * 1024 + 1).decode("utf-8")
            except UnicodeDecodeError:
                flash("The uploaded file must use UTF-8 text encoding.", "error")
                return redirect(url_for("review.index"))
        try:
            parsed = parse_unified_diff(diff_text)
        except DiffError as exc:
            flash(str(exc), "error")
            return redirect(url_for("review.index"))

        findings = prepare_suggestions(analyze_changes(parsed))
        db = get_db()
        summary = f"{len(parsed)} file(s), {sum(len(f['added']) for f in parsed)} added line(s), {sum(len(f['deleted']) for f in parsed)} deleted line(s)"
        cursor = db.execute("INSERT INTO review_sessions(filename, diff_summary) VALUES (?, ?)",
                            (filename, summary))
        session_id = cursor.lastrowid
        for item in findings:
            db.execute("""INSERT INTO suggestions
                (session_id, source, file_path, line_number, category, severity, comment, suggested_fix, fingerprint)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (session_id, item["source"], item["file_path"], item["line_number"],
                 item["category"], item["severity"], item["comment"],
                 item["suggested_fix"], item["fingerprint"]))
        db.commit()
        return redirect(url_for("review.results", session_id=session_id))
    return render_template("index.html")

@review_bp.route("/review/<int:session_id>")
def results(session_id):
    db = get_db()
    session = db.execute("SELECT * FROM review_sessions WHERE session_id=?", (session_id,)).fetchone()
    if not session:
        flash("Review session not found.", "error")
        return redirect(url_for("review.index"))
    suggestions = db.execute("""
        SELECT s.*, f.decision, f.feedback_note
        FROM suggestions s LEFT JOIN reviewer_feedback f USING(suggestion_id)
        WHERE s.session_id=? ORDER BY CASE s.severity WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END, s.suggestion_id
    """, (session_id,)).fetchall()
    return render_template("results.html", session=session, suggestions=suggestions)

@review_bp.route("/history")
def history():
    sessions = get_db().execute("SELECT * FROM review_sessions ORDER BY session_id DESC LIMIT 50").fetchall()
    return render_template("history.html", sessions=sessions)
