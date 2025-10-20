import requests
import json
import logging

URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
)

RESULT_FILE = "result.json"
LOG_FILE = "solution_errors.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class FetchDataException(Exception):
    """Custom exception for data fetching errors."""
    
    def __init__(self, url:str, status_code:int | None = None, message: str | None = None):
        self.url = url
        self.status_code = status_code
        self.message = message or f"An error occurred while fetching data from {url}."
        super().__init__(self.message)
    def __str__(self):
        """Readable representation of the exception."""
        code_info = f" Status code: {self.status_code}." if self.status_code else ""
        return f"{self.message}{code_info} URL: {self.url}"
    
def solution():
    """Fetch data from predefined URLs, sort by height in descending order, and save to a JSON file."""
    data = []

    for url in URLS:
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            if status_code != 200:
                raise FetchDataException(url, status_code, f"Unexpected status code {status_code}.")
            json_data = response.json()
            if not json_data or "height" not in json_data:
                raise FetchDataException(url, status_code, "Invalid or empty data received.")
            data.append(json_data)
        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException for URL {url}: {e}")
            raise FetchDataException(url, None, f"Network or connection error: {e}") from e
        except FetchDataException as e:
            logging.error(str(e))
            continue
        except ValueError as e:
            logging.error(f"JSON decoding error for URL {url}: {e}")
            continue 

    def parse_height(h: str) -> int:
        try:
            return int(h)
        except ValueError:
            return -1 
        
    data.sort(key=lambda x: parse_height(x["height"]), reverse=True)
    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data


if __name__ == "__main__":
    try:
        result = solution()

        if not result:
            print("No valid data fetched. Check the log for details.")
        else:
            print("Data fetched successfully and saved to result.json.")
            print(f"Most tall character: {result[0]['name']} ({result[0]['height']} cm)")

    except FetchDataException as e:
        print(f"FetchDataException: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")