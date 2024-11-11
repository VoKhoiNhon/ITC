import requests
from bs4 import BeautifulSoup
import itertools
import string
from concurrent.futures import ProcessPoolExecutor, as_completed
import csv
import json
from tqdm import tqdm
import threading
import time

# URLs and headers
url = "https://cofs.lara.state.mi.us/SearchApi/Search/Search/GetSearchResults"
headers = {
    "Referer": "https://cofs.lara.state.mi.us/SearchApi/Search/Search",
}
base_url = "https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSummary.aspx?token="

# Global variable for file output
data_lock = threading.Lock()
output_file = "all_links.csv"
json_output_file = "entity_data.json"

def fetch_data(search_value, start, end):
    """ Fetch data from the server and save it immediately """
    data = {
        "SearchValue": search_value,
        "SearchType": "E",
        "SearchMethod": "B",
        "StartRange": str(start),
        "EndRange": str(end),
        "SortColumn": "",
        "SortDirection": ""
    }
    
    try:
        response = requests.post(url, headers=headers, data=data, timeout=60)
        time.sleep(5)  # Introduce delay to prevent overwhelming the server
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            filtered_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(base_url)]
            return filtered_links
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return []

def save_data(links):
    """ Save links to the CSV file immediately and scrape entity data """
    with data_lock:
        with open(output_file, "a", newline='') as file:
            csv_writer = csv.writer(file)
            for link in links:
                csv_writer.writerow([link])
                # Scrape entity data and save it as JSON
                entity_data = scrape_entity_data(link)
                if entity_data:
                    save_json_data(entity_data)

def scrape_entity_data(url):
    headers = {
        "Referer": "https://cofs.lara.state.mi.us/SearchApi/Search/Search",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 Edg/129.0.0.0",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"'
    }

    try:
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting data
        id_number = safe_find_text(soup, 'span', id='MainContent_lblIDNumberHeader')
        entity_name = safe_find_text(soup, 'span', id='MainContent_lblEntityNameHeader')

        previous_entity_name_td = soup.find('td', text='The name was changed from:')
        if previous_entity_name_td:
            previous_entity_name_change = previous_entity_name_td.find_next('div').text.strip()
            date_of_change = previous_entity_name_td.find_next('span').text.strip()
        else:
            previous_entity_name_change = date_of_change = 'N/A'

        entity_type = safe_find_text(soup, 'span', id='MainContent_lblEntityType')
        identification_number_current = id_number
        identification_number_old = safe_find_text(soup, 'span', id='MainContent_lblOldIDNumber')
        incorporation_date = safe_find_text(soup, 'span', id='MainContent_lblOrganisationDate')
        dissolution_date = safe_find_text(soup, 'span', id='MainContent_lblInactiveDate')
        term = safe_find_text(soup, 'span', id='MainContent_lblTerm')
        most_recent_ar = safe_find_text(soup, 'span', id='MainContent_lblMostRecentAnnualReportYear')
        most_recent_ar_officers = safe_find_text(soup, 'span', id='MainContent_lblMostRecentAnnualReportWithOfficers')

        resident_agent_name = safe_find_text(soup, 'span', id='MainContent_lblResidentAgentName')
        resident_agent_address = f"{safe_find_text(soup, 'span', id='MainContent_lblResidentStreet')}, {safe_find_text(soup, 'span', id='MainContent_lblResidentCity')}, {safe_find_text(soup, 'span', id='MainContent_lblResidentState')} {safe_find_text(soup, 'span', id='MainContent_lblResidentZip')}"

        officers_table = soup.find('table', id='MainContent_grdOfficers')
        officers = []
        if officers_table:
            for row in officers_table.find_all('tr', class_='GridRow'):
                cells = row.find_all('td')
                if len(cells) >= 3:
                    officer = {
                        'title': cells[0].text.strip(),
                        'name': cells[1].text.strip(),
                        'address': cells[2].text.strip()
                    }
                    officers.append(officer)

        return {
            'ID Number': id_number,
            'Entity Name': entity_name,
            'Previous Entity Name': previous_entity_name_change,
            'Date of Change': date_of_change,
            'Entity Type': entity_type,
            'Identification Number': {
                'Current': identification_number_current,
                'Old': identification_number_old
            },
            'Date of Incorporation': incorporation_date,
            'Dissolution Date': dissolution_date,
            'Term': term,
            'Most Recent Annual Report': most_recent_ar,
            'Most Recent Annual Report with Officers & Directors': most_recent_ar_officers,
            'Resident Agent Details': {
                'Name': resident_agent_name,
                'Address': resident_agent_address
            },
            'Officers and Directors': officers
        }
    except Exception as e:
        return {'url': url, 'error': str(e)}

def save_json_data(data):
    """ Save entity data as a JSON line """
    with data_lock:
        with open(json_output_file, "a") as json_file:
            json.dump(data, json_file)
            json_file.write("\n")  # Write newline for line-separated JSON

def safe_find_text(soup, tag, **kwargs):
    """ Helper function to find text safely """
    element = soup.find(tag, **kwargs)
    return element.text.strip() if element else 'N/A'

def process_combinations(combination):
    """ Process character combinations and fetch/save data immediately """
    search_value = ''.join(combination)
    
    with ProcessPoolExecutor(max_workers=5) as thread_pool:
        futures = [thread_pool.submit(fetch_data, search_value, start, start + 100)
                   for start in range(1, 10001, 100)]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                save_data(result)  # Save the links and scrape entity data

if __name__ == "__main__":
    special_characters = string.punctuation + ' '
    characters = string.ascii_lowercase + string.digits + special_characters

    # Initialize the CSV file with headers (optional)
    with open(output_file, "w", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Link"])  # You can remove this if headers aren't needed.

    # Process combinations for 4-character strings
    with ProcessPoolExecutor(max_workers=20) as process_pool:
        total_combinations = 36 ** 3  # Updated for 4-character combinations
        with tqdm(total=total_combinations) as pbar:
            length = 3  # Set length to 4 characters
            combinations = itertools.product(characters, repeat=length)
            futures = [process_pool.submit(process_combinations, combination) for combination in combinations]
            for future in as_completed(futures):
                pbar.update(1)
