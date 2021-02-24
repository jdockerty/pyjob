import os
import sys
import requests
from loguru import logger

# REED_SEARCH_API_URL=f"https://www.reed.co.uk/api/1.0/search?keyterms=accountant&location=london&distancefromlocation=15"

# API Reference docs: https://www.reed.co.uk/developers/jobseeker
class Search(object):
    
    _API_KEY = None
    _SEARCH_URL = "https://www.reed.co.uk/api/1.0/search?"
    _LOG_LEVEL = None

        
    _search_keyterms = None
    _employer_id = None # Set ID for jobs by a specific employer, e.g. BAE Systems is 413757. This is best to glean from a particular job posting.
    _employer_profile_id = None # Reed API is not very clear around this, even responses usually contain 'None', generally avoid. Added for completeness.
    _location = None
    _distance_from_location = 10 # Default in miles
    _result_amount = 100 # Default and upper limit according to Reed API.
    _results_to_skip = 0
    _minimum_salary = 0
    _maximum_salary = 0
    _permanent = None
    _temporary = None
    _contract = None
    _recruitment_agency_post = None
    _employer_direct_post = None
    _graduate_suitable = None
    _total_results = 0
    _full_time_hours = None
    _part_time_hours = None
    _session = requests.Session()
    
    results = {}
    
    def __init__(self):
        
        self._API_KEY = os.getenv("REED_API_KEY")
        if self._API_KEY is None:
            logger.info("REED_API_KEY is not set, exiting...")
            sys.exit(1)
            
        self._session.auth = (self._API_KEY, '') # Password is left blank according to Reed API docs.
        
        # Reset logger for ability to specify custom level.
        logger.remove()
        self._LOG_LEVEL = os.getenv("PYJOB_LEVEL")
        if self._LOG_LEVEL is None:
            logger.add(sys.stderr, level="INFO")

        else:
            logger.add(sys.stderr, level=self._LOG_LEVEL.upper())

    def set_max_results(self, value: int):
        
        if value > 0 and value <= 100:
            self._result_amount = value
        else:
            logger.info("Max results must be between 0 and 100.")
            exit()

    def set_graduate_roles(self, grad: bool):
        
        self._graduate_suitable = grad
        
    def set_employer_id(self, id: str):
        
        self._employer_id = id
    
    def set_employer_profile_id(self, id: str):
        
        self._employer_profile_id = id
        
    def set_keyterms(self, keyterms: list):
        
        if len(keyterms) != 0:
            
            if len(keyterms) == 1:
                logger.debug("Singular term: {}", keyterms[0])
                self.search_keyterms = keyterms[0]
            else:
                logger.debug("Multiple terms: {}", keyterms)
                self._search_keyterms = []
                for keyword in keyterms:
                    self._search_keyterms.append(keyword)
        else:
            logger.info("Key terms must be populated for a search.")
            sys.exit(1)


            
    def set_location(self, location: str):
        
        self._location = location
    
    def set_location_distance(self, distance: int):
        
        if distance >= 0:
            self._distance_from_location = distance
            logger.debug("Distance from location set to {}", self._distance_from_location)
        else:
            logger.info("Cannot have a distance lower than 0, using default of 10.")
            self._distance_from_location = 10
    

    
    def set_salary_range(self, min=0, max=0):
        
        if min >= 0 and max >= 0:
            self._minimum_salary = min
            self._maximum_salary = max
            logger.info("Maximum salary: {}, Minimum salary: {}", self._maximum_salary, self._minimum_salary)
        else:
            logger.info("Salary must be between greater than 0.")
            sys.exit(1)
    
    def set_posted_by(self, poster: str):
        
        if poster.lower() == "employer":
            self._employer_direct_post = True
        elif poster.lower() == "recruiter":
            self._recruitment_agency_post = True
        else:
            logger.info("Available values are 'employer' and 'recruiter' for job postings.")
            sys.exit(1)
        
    
    def set_job_type(self, job_type: str):
         
        if job_type.lower() == "permanent":
            self._permanent = True
        elif job_type.lower() == "temporary":
            self._temporary = True    
        elif job_type.lower() == "contract":
            self._contract = True
        else:
            logger.info("Available job types are 'permanent', 'contract', and 'temporary'.")
            sys.exit(1)
        
    def set_work_type(self, work_type: str):
        
        if work_type.lower() == "ft":
            self._full_time_hours = True
        elif work_type.lower() == "pt":
            self._part_time_hours = True
        else:
            logger.info("Work type must be either 'ft' or 'pt', denoting either full time or part-time working hours.")
            sys.exit(1)  
        
    
    def _build_url(self):
        
        url = self._SEARCH_URL
        
        
        if self._search_keyterms is None:
            logger.debug("No search keyterms are set.")
        else:
            url += f"&keywords="
            for keyword in self._search_keyterms:
                url += f"%20{keyword}"
  
        if self._location is None:
            logger.debug("No location set.")
        else:
            logger.debug("Location set to {}", self._location)
            url += f"&location={self._location}"
        
        if self._maximum_salary > 0:
            logger.debug("Maximum salary set to {}", self._maximum_salary)
            url += f"&maximumSalary={self._maximum_salary}"
        
        elif self._minimum_salary > 0:
            logger.debug("Minimum salary set to {}", self._minimum_salary)
            url += f"&minimumSalary={self._minimum_salary}"
        
        if self._result_amount > 0:
            logger.debug("Results to display set to {}", self._result_amount)
            url += f"&resultsToTake={self._result_amount}"
        
        if self._permanent is not None:
            url += f"&permanent={self._permanent}"
            
        elif self._contract is not None:
            url += f"&contract={self._permanent}"
            
        elif self._temporary is not None:
            url += f"&temp={self._temporary}"
        
        if self._full_time_hours is not None:
            url += f"&fullTime={self._full_time_hours}"
        elif self._part_time_hours is not None:
            url += f"&partTime={self._part_time_hours}"
        
        if self._graduate_suitable is not None:
            url += f"&graduate={self._graduate_suitable}"
        
        if self._employer_direct_post is not None:
            url += f"&postedByDirectEmployer={self._employer_direct_post}"
        elif self._recruitment_agency_post is not None:
            url += f"&postedByRecruitmentAgency={self._recruitment_agency_post}"
        
        if self._employer_id is not None:
            url += f"&employerId={self._employer_id}"
        
        if self._employer_profile_id is not None:
            url += f"&employerProfileId={self._employer_profile_id}"
                    
        logger.debug("Built url: {}", url)
        return url
     
    def search(self):
        
        URL = self._build_url()
        try:
            resp = self._session.get(URL)
            resp.raise_for_status()
            self.results = resp.json()['results']
            self._total_results = resp.json()['totalResults']
            
            print(self.results)
            for result in self.results:
                # if result['employerName'] == "JP Morgan Chase":
                #     print(result)
                print(result['employerName'])
                
        except requests.HTTPError as err:
            logger.info("There was an error performing the request: {}", err)
            raise requests.HTTPError
            
    def get_total_results(self):
        
        if len(self.results) == 0:
            logger.info("You must conduct a search with results before retrieving the total.")
            sys.exit(1)
        else:
            return self._total_results
        
s = Search()
s.set_keyterms(['developer'])
# s.set_location("Newcastle")
# s.set_job_type("permanent")
# s.set_max_results(2)
# s.set_posted_by("employer")
# s.set_employer_id("413757")
s.set_employer_profile_id("p61278")
s.search()