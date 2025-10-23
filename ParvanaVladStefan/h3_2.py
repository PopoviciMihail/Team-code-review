"""
Exercise 2

Create a function solution() that aggregates the responses from the following URLs within a list.
Your function should return the data, sorted by height, in descending order.
(ATTENTION: height is of type str). Make sure you have some minimal sanity checks (e.g. status_code, empty data).

You only need to fetch the data from the first 3 URLs. That is:

URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
)
NOTE:

URLS_TEMPLATE = "https://swapi.dev/api/people/{}"
Create a custom exception class. Handle an exception (at your choice) that the requests module
might raise in the function you have just created. Raise the newly created exception.

Write the final result to a result.json file and log the exceptions in solution_errors.log.

Pay attention to:
Naming conventions (or really, any PEP8 conventions, in general);
Scalability of your code (what if we want to extend the functionality by getting the data from
all the available URLs / or create unit tests etc);
Runtime complexity.
Resources
requests | already installed
Exceptions
JSON

"""
from string import Template
import requests
import json

class MustHaveHairError(Exception):
    def __init__(self, message: str = "Character must have hair") -> None:
        self.message = message
        super().__init__(self.message)

URLS_TEMPLATE = Template("https://swapi.dev/api/people/${id}")
IDS = [1,2,3,1000]
URLS = [URLS_TEMPLATE.substitute(id=id) for id in IDS]

def solution(urls: list) -> list:
    results = []
    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("hair_color") == "n/a":
                raise MustHaveHairError(f"Character at {url} has no hair.")
            if data:
                results.append(data)
            else:
                raise ValueError(f"Empty data received from {url}")
        except (requests.RequestException, ValueError, MustHaveHairError) as e:
            with open("solution_errors.log", "a") as log_file:
                log_file.write(f"Error fetching data from {url}: {e}\n")
    sorted_results=sorted(results, key= lambda x: int(x['height']),reverse= True)
    return sorted_results

if __name__ == "__main__":
    results = solution(URLS)

    with open("result.json", "w") as result_file:
        json.dump(results, result_file, indent=4)