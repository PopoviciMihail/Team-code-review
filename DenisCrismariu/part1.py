"""
Exercise 1

Using pandas, determine the following for the sales.csv data:
The total revenue for each product (quantity  x price_per_unit).
The total cost for each product (quantity  x cost_per_unit).
The profit for each product (total revenue - total cost).
Finally, find the most profitable product overall.
"""
import pandas as pd
df = pd.read_csv("sales.csv")
df["total_revenue"] = df["quantity"] * df["price_per_unit"]
df["total_cost"] = df["quantity"] * df["cost_per_unit"]
df["profit"] = df["total_revenue"] * df["total_cost"]
print(df[df.profit==df.profit.max()]["product"].values[0])
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
JSON-
"""
import requests
import numpy as np
from requests import HTTPError
import json
import logging

class HeightMissingError(Exception):
    def __init__(self, message: str = "Request failed") ->None:
        self.message = message
        super().__init__(self.message)

def solution(url_list : list[str]):
    responses = []
    logging.basicConfig(filename="solution_errors.log",
                        level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        encoding="utf-8"
                        )
    
    logger = logging.getLogger(__name__)
    
    for url in url_list:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if "height" not in data:
                raise HeightMissingError(f"Height missing in reponse from {url}")
            
            responses.append(data)
            
        except HTTPError as ex:
            logger.error(f"404 Not Found: {url}")
        except HeightMissingError as ex:
            logger.error(str(ex))
            
        responses.sort(key= lambda x:x["height"],reverse=True)
    if responses:
        with open("result.json","w") as f:
            json.dump(responses,f)
    
          
solution([f"https://swapi.dev/api/people/{i}" for i in range(100)])
