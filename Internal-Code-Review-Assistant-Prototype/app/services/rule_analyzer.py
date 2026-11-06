
import re

def analyze_changes(files):
    findings = []

    for file in files:
        path = file["file_path"]

        for item in file["added"]:
            code = item["content"]
            line = item["line_number"]

            # Check suspicious logical conditions
            if re.search(r"\b(if|elif)\b.*<.*\band\b.*>", code):
                findings.append(_finding(
                    path, line, "Logic", "Medium",
                    "This condition may be impossible if it checks the same value against opposite sides of a range. Verify whether AND was intended.",
                    "Check the intended range and use the appropriate comparison and logical operator."
                ))

            # Check hardcoded credentials
            if re.search(
                r"""(?i)\b(api[_-]?key|password|secret|token)\s*=\s*['"][^'"]{4,}['"]""",
                code
            ):
                findings.append(_finding(
                    path, line, "Security", "High",
                    "A credential-like value appears to be hardcoded. Avoid storing secrets in source code.",
                    "Load the value from an environment variable or an approved secret manager."
                ))

            # Check bare except clauses
            if re.search(r"\bexcept\s*:", code):
                findings.append(_finding(
                    path, line, "Reliability", "Medium",
                    "A bare except clause can hide unexpected errors. Catch only the exceptions you can handle.",
                    "Catch a specific exception type and handle or log it appropriately."
                ))

            # Check print statements
            if re.search(r"\bprint\s*\(", code):
                findings.append(_finding(
                    path, line, "Maintainability", "Low",
                    "A print statement may be unsuitable for production diagnostics.",
                    "Consider using the application's configured logging framework."
                ))

    return findings


def _finding(path, line, category, severity, comment, fix):
    return {
        "source": "rule",
        "file_path": path,
        "line_number": line,
        "category": category,
        "severity": severity,
        "comment": comment,
        "suggested_fix": fix
    }
