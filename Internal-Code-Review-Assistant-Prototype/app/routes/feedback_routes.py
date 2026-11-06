from flask import Blueprint, request, redirect, url_for, flash
from app.database.db import get_db

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/feedback/<int:suggestion_id>", methods=["POST"])
def save_feedback(suggestion_id):
    decision = request.form.get("decision", "")
    note = request.form.get("feedback_note", "").strip()[:1000]
    if decision not in {"Accept", "Reject", "Dismiss"}:
        flash("Choose a valid reviewer decision.", "error")
        return redirect(request.referrer or url_for("review.index"))
    db = get_db()
    row = db.execute("SELECT session_id FROM suggestions WHERE suggestion_id=?",
                     (suggestion_id,)).fetchone()
    if not row:
        flash("Suggestion not found.", "error")
        return redirect(url_for("review.index"))
    db.execute("""INSERT INTO reviewer_feedback(suggestion_id, decision, feedback_note)
                  VALUES (?, ?, ?)
                  ON CONFLICT(suggestion_id) DO UPDATE SET
                  decision=excluded.decision, feedback_note=excluded.feedback_note,
                  created_at=CURRENT_TIMESTAMP""", (suggestion_id, decision, note))
    db.commit()
    flash("Reviewer decision saved.", "success")
    return redirect(url_for("review.results", session_id=row["session_id"]))
