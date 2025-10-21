from requests import Response, get as get_request, RequestException
import json
import logging

logging.basicConfig(filename='solution_errors.log', level=logging.ERROR)
URLS_TEMPLATE :str = "https://swapi.dev/api/people/{}"

class FetchDataException(Exception):
    """Custom exception for data fetching errors."""
    pass

def fetch_data(url: str) -> dict:
    try:
        response :Response = get_request(url)
        response.raise_for_status()
        data :dict = response.json()
        if not data:
            raise FetchDataException(f"No data found at {url}")
        return data
    except RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        raise FetchDataException(f"Failed to fetch data from {url}") from e

def solution() -> None:
    results :list[dict] = []
    for i in range(1, 4):
        url :str = URLS_TEMPLATE.format(i)
        data :dict = fetch_data(url)
        results.append(data)
    sorted_results :list[dict] = sorted(results, key=lambda x: int(x['height']), reverse=True)
    with open('result.json', 'w') as f:
        json.dump(sorted_results, f, indent=4)

if __name__ == '__main__':
    try:
        solution()
    except FetchDataException as e:
        logging.error(f"An error occurred in solution(): {e}")
