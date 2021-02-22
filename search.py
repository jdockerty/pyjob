import os
import sys
import requests
from loguru import logger

# REED_SEARCH_API_URL=f"https://www.reed.co.uk/api/1.0/search?keyterms=accountant&location=london&distancefromlocation=15"

# API Reference docs: https://www.reed.co.uk/developers/jobseeker
class Search(object):
    
    _API_KEY = None
    _SEARCH_URL = "https://www.reed.co.uk/api/1.0/search?"
    _logger = None
    
    _search_keyterms = None
    _location = None
    _distance_from_location = 10 # Default
    _result_amount = 100 # Default and upper limit according to Reed API.
    _results_to_skip = 0
    _minimum_salary = 0
    _maximum_salary = 0
    _session = requests.Session()
    

    results = {}
    
    def __init__(self, log_level="INFO"):
        self._API_KEY = os.getenv("REED_API_KEY")
        self._session.auth = (self._API_KEY, '') # Password is left blank according to Reed API docs.

        # Reset logger for ability to specify custom level.
        logger.remove()
        logger.add(sys.stderr, level=log_level)
        
    @classmethod
    def setup_class(cls):
        return cls()

    def set_keyterms(self, keyterms: list):
        
        try:
            assert len(keyterms) != 0
            
            if len(keyterms) == 1:
                self.search_keyterms = keyterms[0]
            else:
                self._search_keyterms = []
                for keyword in keyterms:
                    self._search_keyterms.append(keyword)

        except AssertionError:
            logger.info("Key terms must be populated")
            raise
            
    def set_location(self, location: str):
        
        self._location = location
    
    def set_location_distance(self, distance: int):
        
        try:
            assert distance >= 0
            self._distance_from_location = distance
            logger.debug("Distance from location set to {}", self._distance_from_location)
            
        except AssertionError as err:
            logger.info("Cannot have a distance lower than 0, using default of 10.")
    
    def set_max_salary(self, value: int):
        
        try:
            assert value >= 0
            self._maximum_salary = value
            logger.debug("Maximum salary set to {}", self._maximum_salary)
        
        except AssertionError:
            logger.info("Cannot have a negative maximum salary.")
            raise
        
    def set_min_salary(self, value: int): 
        
        try:
            assert value >= 0
            self._minimum_salary = value
            logger.debug("Minimum salary set to {}", self._minimum_salary)
        
        except AssertionError:
            logger.info("Cannot have a negative minimum salary.")
            raise
    
    def _build_url(self):
        
        url = self._SEARCH_URL
        
        
        if self._search_keyterms is None:
            logger.debug("No search keyterms are set.")
        else:
            # url += f"&keywords="
            # for keyword in self._search_keyterms:
            #     url += f"%20{keyword}"
            url += f"&keywords={self._search_keyterms}" # Check whether list items affect the query params in URL.
  
        if self._location is None:
            logger.debug("No location set.")
        else:
            logger.info("Location set to {}", self._location)
            url += f"&location={self._location}"
        
        print(url)
     
    def search(self):
        
        if self._search_keyterms is None:
            logger.info("No search keyterms are set. Exiting search...")
            return
        else:
            logger.info("Search terms are {}", self._search_keyterms)
            
            search_url = f"{self._SEARCH_URL}keywords={self._search_keyterms}&location=Newcastle&resultsToTake=3&postedByRecruitmentAgency=false"
            resp = self._session.get(search_url)
            self.results = resp.json()['results']
            print(self.results)
            for result in self.results:
                # print(result)
                logger.info("\nTitle: {}\nEmployer: {}\nSalary range (£): {}-{}\n", result['jobTitle'], result['employerName'], result['minimumSalary'], result['maximumSalary'])
        
s = Search()
s.set_keyterms(["devops engineer", "software engineer"])
s.set_location("London")
s.set_location_distance(50)
# s.search()
s._build_url()