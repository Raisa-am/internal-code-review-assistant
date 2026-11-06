from app.services.suggestion_manager import prepare_suggestions

def test_deduplicates_same_finding():
    item = {"source":"rule","file_path":"a.py","line_number":1,"category":"Logic",
            "severity":"Low","comment":"Same comment","suggested_fix":"Fix"}
    assert len(prepare_suggestions([item, item])) == 1
