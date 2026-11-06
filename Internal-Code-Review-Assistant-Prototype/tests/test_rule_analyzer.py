from app.services.rule_analyzer import analyze_changes

def test_detects_print_and_bare_except():
    files = [{"file_path": "a.py", "added": [
        {"line_number": 3, "content": "print('debug')"},
        {"line_number": 4, "content": "except:"}
    ], "deleted": []}]
    results = analyze_changes(files)
    assert {x["category"] for x in results} == {"Maintainability", "Reliability"}
