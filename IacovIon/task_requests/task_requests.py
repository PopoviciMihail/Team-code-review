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

import requests
import json
import logging

URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
)

# Configure logging
logging.basicConfig(
    filename="solution_errors.log", 
    level=logging.ERROR, 
    format="%(asctime)s - %(message)s"
    )


class FetchDataError(Exception):
    """
    Raised when there is an error fetching data from the API.
    """
    pass

def get_height(item):
    """
    Helper function to get height as integer for sorting.

    :param item: Dictionary containing 'height' key
    :return: Height as integer or -1 if not a valid number
    """
    height_str = item.get("height", "")
    return int(height_str) if height_str.isdigit() else -1

def show_results():
    """
    Load and print the contents of 'result.json' in a readable format.
    
    :return: None
    """
    try:
        with open("result.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print("No result.json file found. Run the solution() first.")


def solution():
    """
    Fetch data from the first 3 URLs, handle exceptions, 
    and save results to result.json
    
    :return: None
    """
    results = []

    for url in URLS:
        try:
            response = requests.get(url)

            if response.status_code != 200:
                raise FetchDataError(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            
            data = response.json()
            
            if not data or "height" not in data or "name" not in data:
                raise FetchDataError(f"Invalid data received from {url}")
            
            results.append(data)
        
        except (requests.RequestException, FetchDataError) as e:
            logging.error(str(e))
            print(f"Error: {e}")

    results.sort(key=get_height, reverse=True)


    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    
    print("Data has been saved to result.json")


if __name__ == "__main__":
    solution()
    print("\n--- Showing results from result.json ---\n")
    show_results()