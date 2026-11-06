from app.services.diff_parser import parse_unified_diff, DiffError

def test_parses_added_line():
    diff = "diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n@@ -1,1 +1,2 @@\n old\n+print('hi')\n"
    parsed = parse_unified_diff(diff)
    assert parsed[0]["file_path"] == "a.py"
    assert parsed[0]["added"][0]["line_number"] == 2

def test_rejects_empty_diff():
    try:
        parse_unified_diff("")
        assert False, "Expected DiffError"
    except DiffError:
        assert True
