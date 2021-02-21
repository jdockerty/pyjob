from client import Search
import pytest

def test_api_key_set():
    s = Search()
    assert s._API_KEY != ""

def test_default_location_distance():
    s = Search()
    s.set_location_distance(-50) # Default of 10 should be used
    assert s._distance_from_location == 10

def test_set_location():
    s = Search()
    s.set_location("London")
    
    assert s._location == "London"

def test_keyterms_set():
    
    s = Search()
    terms = ['software engineer', 'devops', 'SRE']
    s.set_keyterms(terms)
    
    assert s._search_keyterms == terms

def test_keyterms_errors():
    s = Search()
    terms = ''

    with pytest.raises(AssertionError):
        s.set_keyterms(terms)
