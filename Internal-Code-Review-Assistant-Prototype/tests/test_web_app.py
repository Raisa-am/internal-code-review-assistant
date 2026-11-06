def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200

def test_review_workflow(client):
    diff = """diff --git a/a.py b/a.py
--- a/a.py
+++ b/a.py
@@ -1,1 +1,2 @@
 old()
+print("debug")
"""
    response = client.post("/", data={"diff_text": diff}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Maintainability" in response.data
