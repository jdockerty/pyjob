from search import Search
import pytest

search = Search()

def test_api_key_set():
    assert search._API_KEY != ""

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

    with pytest.raises(AssertionError):
        search.set_keyterms(terms)

def test_invalid_max_salary():

    max_salary = -30000
    
    with pytest.raises(AssertionError):
        search.set_max_salary(max_salary)

def test_invalid_min_salary():

    min_salary = -35000
    
    with pytest.raises(AssertionError):
        search.set_min_salary(min_salary)