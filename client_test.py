from client import Search

def test_api_key_set():
    s = Search.setup_class()
    assert s._API_KEY != ""