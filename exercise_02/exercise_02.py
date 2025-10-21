import json
import requests
from SwapiFetchError  import SwapiFetchError

URLS = (
    "https://swapi.dev/api/people/1/",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
    "badurl",
    "https://bad.url/12345"
)

def log_error(err) -> None:
    with open("solution_errors.log", "a") as f:
        f.write(json.dumps(err.as_dict()) + "\n")


def to_int(s: str) -> int:
    try:
        return int(s)
    except Exception:
        return -1


def write_result_to_file(result: list) -> None:
    try:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        log_error(f"Failed to write result.json: {e}")


def get_data_from_url(url: str):
    try:
        response = requests.get(url)
    except Exception as e:
        log_error(SwapiFetchError(url, "Request failed"))
        return None
    
    return response


def solution() -> list:
    results = []

    for url in URLS:
        response = get_data_from_url(url)

        if not response or response.status_code != 200:
            log_error(SwapiFetchError(url, "Bad status", status_code=response.status_code if response else None))
            continue

        data = response.json()
        
        if not data or "height" not in data:
            log_error(SwapiFetchError(url, "Empty or missing data"))
            continue

        results.append(data)

    results.sort(key=lambda x: to_int(x.get("height")), reverse=True)

    write_result_to_file(results)

    return results


if __name__ == "__main__":
    solution()