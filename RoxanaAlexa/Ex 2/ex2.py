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

------------------------------------------------------------------------

"""


from fastapi import FastAPI, HTTPException
import requests
import json
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()


class MyException(Exception):
    """Custom exception used for handling domain-specific and network errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
)

URLS_TEMPLATE = "https://swapi.dev/api/people/{}"


@app.get("/fetch")
async def solution(height: str | None = None):
    if height is None:
        raise MyException("Missing required query parameter: height")

    results = []

    for url in URLS:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if not data:
                raise MyException("Missing data")

            results.append(data)

        except requests.exceptions.RequestException as e:
            with open("solutions_errors.log", "a") as f:
                f.write(f"[NETWORK ERROR] {url}: {e}\n")
            raise MyException("Network error")

    results_sorted = sorted(results, key=lambda x: int(x["height"]), reverse=True)

    with open("result.json", "w") as f:
        json.dump(results_sorted, f, indent=4)

    return {"results": results_sorted}


@app.exception_handler(MyException)
async def solution_exception_handler(request: Request, exc: MyException):
    return JSONResponse(
        status_code=400,
        content={"error": exc.message}
    )