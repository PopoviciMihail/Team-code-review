from fastapi import FastAPI, HTTPException
import requests
import json
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()


class MyException(Exception):
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