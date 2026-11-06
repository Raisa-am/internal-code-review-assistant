import re

class DiffError(ValueError):
    pass

def parse_unified_diff(diff_text):
    if not isinstance(diff_text, str) or not diff_text.strip():
        raise DiffError("Please paste or upload a unified Git diff.")
    if len(diff_text) > 2 * 1024 * 1024:
        raise DiffError("The submitted diff is larger than 2 MB.")

    files = []
    current = None
    old_line = new_line = None
    saw_diff = False

    for raw in diff_text.splitlines():
        if raw.startswith("diff --git "):
            saw_diff = True
            if current:
                files.append(current)
            parts = raw.split()
            old_path = parts[2][2:] if len(parts) > 2 else "unknown"
            new_path = parts[3][2:] if len(parts) > 3 else old_path
            current = {"file_path": new_path, "added": [], "deleted": []}
            continue

        if raw.startswith("--- ") or raw.startswith("+++ "):
            if current is None:
                current = {"file_path": raw[6:].strip() if raw.startswith("+++ ") else "unknown",
                           "added": [], "deleted": []}
            if raw.startswith("+++ "):
                path = raw[4:].strip()
                if path != "/dev/null":
                    current["file_path"] = path[2:] if path.startswith("b/") else path
            continue

        if raw.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", raw)
            old_match = re.search(r"-(\d+)(?:,(\d+))?", raw)
            new_line = int(match.group(1)) if match else None
            old_line = int(old_match.group(1)) if old_match else None
            continue

        if current is None:
            continue
        if raw.startswith("+") and not raw.startswith("+++"):
            current["added"].append({"line_number": new_line, "content": raw[1:]})
            if new_line is not None:
                new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            current["deleted"].append(raw[1:])
            if old_line is not None:
                old_line += 1
        elif raw.startswith(" ") or raw == "":
            if new_line is not None:
                new_line += 1
            if old_line is not None:
                old_line += 1

    if current:
        files.append(current)
    if not files or not any(f["added"] or f["deleted"] for f in files):
        raise DiffError("No changed lines were found. Please provide a valid unified Git diff.")
    return files
