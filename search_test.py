from search import Search
import pytest


search = Search("DEBUG")

def test_api_key_set():
    assert search._API_KEY != ""

def test_api_key_error(monkeypatch):
    
    monkeypatch.delenv("REED_API_KEY")
    with pytest.raises(SystemExit):
        new_search = Search()   
                       
        
def test_default_location_distance():

    search.set_location_distance(-50) # Default of 10 should be used
    assert search._distance_from_location == 10

def test_set_location():
    
    search.set_location("London")
    
    assert search._location == "London"

def test_keyterms_set():
    
    terms = ['software engineer', 'devops', 'SRE']
    search.set_keyterms(terms)
    
    assert search._search_keyterms == terms

def test_keyterms_errors():
    
    terms = ''

    with pytest.raises(SystemExit):
        search.set_keyterms(terms)

def test_invalid_salary():
    
    min_salary_invalid = -50000
    max_salary_invalid = -90000
    
    with pytest.raises(SystemExit):
        search.set_salary_range(min=min_salary_invalid)
    
    with pytest.raises(SystemExit):
        search.set_salary_range(max=max_salary_invalid)