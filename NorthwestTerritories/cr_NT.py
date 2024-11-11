import requests
import csv
from bs4 import BeautifulSoup
import itertools
import string
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Define the URL
url = "https://www.justice.gov.nt.ca/app/cros-rsel/search"

# Define character sets for generating combinations
letters = string.ascii_lowercase
digits = string.digits
special_chars = string.punctuation

# Create a combined character set
combined_chars = letters + digits + special_chars + " "

# Function to generate 3-character combinations
def generate_combinations(chars, length=3):
    return [''.join(combination) for combination in itertools.product(chars, repeat=length)]

# Function to fetch data for a given search name and page
def fetch_data(search_name, page):
    params = {
        'search_name': search_name,
        'page': page,
        'reference': '',
        'btnSearch': ''
    }
    try:
        response = requests.get(url, params=params, timeout=3600)
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting table rows
        rows = []
        for row in soup.select('tbody tr'):
            columns = [td.get_text(strip=True) for td in row.find_all('td')[:-1]]
            rows.append(columns)
        return rows

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for '{search_name}' on page {page}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error for '{search_name}' on page {page}: {e}")
        return []

# Generate all combinations
combinations = generate_combinations(combined_chars)

# Initialize CSV file
with open('D:\\Nhon_work\\NorthwestTerritories\\table_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Entity Type", "File No.", "Jurisdiction", "Name Type", "Status"])

    # Use ThreadPoolExecutor for multi-threading
    with ThreadPoolExecutor(max_workers=50) as executor:  # Adjust max_workers based on testing
        future_to_combination = {
            executor.submit(fetch_data, search_name, page): (search_name, page)
            for search_name in combinations
            for page in range(1, 4)  # Adjust as needed
        }

        for future in tqdm(as_completed(future_to_combination), total=len(future_to_combination), desc="Searching combinations", unit="combination"):
            search_name, page = future_to_combination[future]
            try:
                rows = future.result()
                for row in rows:
                    writer.writerow(row)
            except Exception as e:
                print(f"Error processing '{search_name}' on page {page}: {e}")

            time.sleep(0.1)  # Sleep briefly between requests

print("Data collection completed.")
