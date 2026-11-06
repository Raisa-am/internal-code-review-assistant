import hashlib
import re

ORDER = {"High": 0, "Medium": 1, "Low": 2}

def fingerprint(finding):
    normal = re.sub(r"\s+", " ", finding["comment"].strip().lower())
    raw = "|".join([finding["file_path"], str(finding["line_number"]),
                    finding["category"], normal])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def prepare_suggestions(findings):
    unique = {}
    for item in findings:
        item = dict(item)
        item["fingerprint"] = fingerprint(item)
        unique.setdefault(item["fingerprint"], item)
    return sorted(unique.values(),
                  key=lambda x: (ORDER.get(x["severity"], 9),
                                 x["file_path"], x["line_number"] or 0))
