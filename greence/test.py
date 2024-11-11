import requests
import json
import itertools
import string
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

url = "https://publicity.businessportal.gr/api/searchCompany"

# Generate combinations of one and two characters
characters = string.ascii_lowercase + string.digits + string.punctuation + " "
combinations = [''.join(comb) for r in range(1, 3) for comb in itertools.product(characters, repeat=r)]

# Prepare headers
headers = {
    'Content-Type': 'application/json',
    'Origin': 'https://publicity.businessportal.gr',
    'Referer': 'https://publicity.businessportal.gr/'
}

# File to save responses
output_file = 'D:\\Nhon_work\\greence\\res.json'

# Initialize the JSON file with an empty list if it doesn't exist
if not os.path.exists(output_file):
    with open(output_file, 'w') as f:
        json.dump([], f)

# Create a lock for file access
file_lock = threading.Lock()

def make_request(input_field, page):
    payload = json.dumps({
        "dataToBeSent": {
            "inputField": input_field,
            "city": None,
            "postcode": None,
            "legalType": [],
            "status": [],
            "suspension": [],
            "category": [],
            "specialCharacteristics": [],
            "employeeNumber": [],
            "armodiaGEMI": [],
            "kad": [],
            "recommendationDateFrom": None,
            "recommendationDateTo": None,
            "closingDateFrom": None,
            "closingDateTo": None,
            "alterationDateFrom": None,
            "alterationDateTo": None,
            "person": [],
            "personrecommendationDateFrom": None,
            "personrecommendationDateTo": None,
            "radioValue": "eponimia",
            "places": [],
            "page": page
        },
        "token": None,
        "language": "en"
    })

    max_retries = 100
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            response_data = response.json()
            ids = [hit['id'] for hit in response_data.get('hits', [])]

            # Only write to the file if there are IDs
            if ids:
                with file_lock:  # Ensure exclusive access to the file
                    with open(output_file, 'r+') as f:
                        current_data = json.load(f)
                        current_data.extend(ids)  # Extend the list with new IDs
                        f.seek(0)
                        json.dump(current_data, f, indent=4)

            return  # Exit the function if the request is successful

        except requests.exceptions.RequestException as e:
            return f"Request failed for Input: {input_field}, Page: {page}, Attempt: {attempt + 1} - {e}"
        except json.JSONDecodeError as e:
            return f"JSON decode error for Input: {input_field}, Page: {page}, Attempt: {attempt + 1} - {e}"

# Main processing loop
for input_field in combinations:
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(make_request, input_field, page): page for page in range(1, 1001)}
        
        # Progress bar for the requests
        for future in tqdm(futures.keys(), desc=f"Processing '{input_field}'", total=len(futures)):
            result = future.result()
            if result:  # Print error messages if any
                print(result)

    time.sleep(0.5)  # Delay between input fields to avoid overwhelming the server

print("Data saved incrementally to responses.json")
