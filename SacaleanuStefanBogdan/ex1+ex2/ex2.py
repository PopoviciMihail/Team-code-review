import requests
import json
import logging
from typing import List, Dict, Any, Tuple

logging.basicConfig(
    filename='solution_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

URLS = (
    "https://swapi.dev/api/people/1",
    "https://swapi.dev/api/people/2",
    "https://swapi.dev/api/people/3",
)
URL_TEMPLATE = "https://swapi.dev/api/people/{}"
RESULT_FILE_NAME = "../result.json"

class SWAPIAggregationError(Exception):
    pass

def fetch_data(url: str) -> Tuple[Dict[str, Any], str]:
    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise ValueError(
                f"Non-200 status code received: {response.status_code} for URL: {url}"
            )

        try:
            data = response.json()
        except json.JSONDecodeError:
            raise ValueError(f"Failed to decode JSON from response for URL: {url}")

        if not data:
            raise ValueError(f"Received empty data for URL: {url}")

        return data, url
    except requests.exceptions.RequestException as e:

        raise e

def solution(urls: Tuple[str, ...]) -> List[Dict[str, Any]]:
    aggregated_data: List[Dict[str, Any]] = []

    for url in urls:
        try:
            data, fetched_url = fetch_data(url)
            aggregated_data.append(data)
        except requests.exceptions.RequestException as e:

            error_message = f"Error fetching data from {url}: {e}"
            logging.error(error_message)

            raise SWAPIAggregationError(error_message) from e
        except ValueError as e:

            logging.error(str(e))

            continue
        except Exception as e:

            error_message = f"An unexpected error occurred for {url}: {e}"
            logging.error(error_message)
            continue

    try:

        sortable_data = [item for item in aggregated_data if item.get('height', '').isdigit()]
        non_sortable_data = [item for item in aggregated_data if not item.get('height', '').isdigit()]

        sortable_data.sort(
            key=lambda item: int(item['height']),
            reverse=True
        )

        return sortable_data + non_sortable_data

    except Exception as e:

        logging.error(f"Error during data sorting: {e}")
        return []

def write_result_to_file(data: List[Dict[str, Any]], filename: str) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"\nSuccessfully wrote aggregated data to {filename}")
    except IOError as e:
        logging.error(f"Failed to write data to file {filename}: {e}")
    except TypeError as e:
        logging.error(f"Data serialization error for file {filename}: {e}")

def main_ex2():
    print("--- Starting SWAPI Data Aggregation and Sorting ---")

    try:

        sorted_data = solution(URLS)

        if sorted_data:

            write_result_to_file(sorted_data, RESULT_FILE_NAME)

            print("\n--- Sorted Data Preview (Height Descending) ---")
            for item in sorted_data:

                print(json.dumps(item, indent=2))
                print()
        else:
            print("\n Could not generate a final result due to critical errors. Check solution_errors.log.")

    except SWAPIAggregationError as e:

        print(f"\nA critical aggregation error occurred: {e}. See solution_errors.log for details.")
    except Exception as e:
        print(f"\nA fatal, unhandled error occurred: {e}")

if __name__ == "__main__":
    main_ex2()