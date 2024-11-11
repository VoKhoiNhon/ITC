import requests
from bs4 import BeautifulSoup
import itertools
import string
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import threading
from tqdm import tqdm
import time

# URLs and headers
url = "https://cofs.lara.state.mi.us/SearchApi/Search/Search/GetSearchResults"
headers = {
    "Referer": "https://cofs.lara.state.mi.us/SearchApi/Search/Search",
}
base_url = "https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSummary.aspx?token="

# Global variable for file output
data_lock = threading.Lock()
output_file = "D:\\Nhon_work\\michigan_data\\test\\data.json"
failed_links_file = "D:\\Nhon_work\\michigan_data\\test\\failed_links.json"
saved_data_set = set()  # To track saved data

def fetch_data(search_value, start, end, retries=100000):
    data = {
        "SearchValue": search_value,
        "SearchType": "E",
        "SearchMethod": "B",
        "StartRange": str(start),
        "EndRange": str(end),
        "SortColumn": "",
        "SortDirection": ""
    }

    attempt = 0
    while attempt < retries:
        try:
            response = requests.post(url, headers=headers, data=data, timeout=3600)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                filtered_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(base_url)]
                return filtered_links
            else:
                print(f"Failed request, status code: {response.status_code}")
                attempt += 1
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            if attempt < retries:
                time.sleep(2)

    return []

def safe_find_text(soup, *args, **kwargs):
    element = soup.find(*args, **kwargs)
    return element.text.strip() if element else 'N/A'

def detail(link, retries=100000):
    headers = {
        "Referer": "https://cofs.lara.state.mi.us/SearchApi/Search/Search",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 Edg/129.0.0.0",
    }

    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(link, headers=headers, timeout=3600)
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
                    'Current': id_number,
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
            # print(f"Error fetching details from {link}: {e}")
            attempt += 1
            if attempt < retries:
                time.sleep(2)  # Optional: add delay between retries

    return {'url': link, 'error': 'Max retries exceeded'}

def save_data(data):
    global saved_data_set
    with data_lock:
        if data['ID Number'] not in saved_data_set:  # Check for duplicates
            try:
                with open(output_file, 'a') as json_file:
                    json.dump(data, json_file)
                    json_file.write('\n')  # New line for each entry for easier readability
                saved_data_set.add(data['ID Number'])  # Add to saved data set
            except Exception as e:
                # print(f"Error saving data: {e}")
                print()

def save_failed_link(link):
    with data_lock:
        try:
            with open(failed_links_file, 'a') as failed_file:
                json.dump(link, failed_file)
                failed_file.write('\n')  # New line for each entry for easier readability
        except Exception as e:
            # print(f"Error saving failed link: {e}")
            print()

def process_combinations(combination):
    search_value = ''.join(combination)
    failed_links = []

    with ProcessPoolExecutor(max_workers=5) as thread_pool:
        futures = [thread_pool.submit(fetch_data, search_value, start, start + 100)
                   for start in range(1, 10001, 100)]

        for future in as_completed(futures):
            result = future.result()
            if result:
                for link in result:
                    detail_data = detail(link)
                    if "error" in detail_data:
                        failed_links.append(link)
                    else:
                        save_data(detail_data)

    # Save any failed links to the separate file
    for link in failed_links:
        save_failed_link(link)

if __name__ == "__main__":
    special_characters = string.punctuation + ' '
    characters = string.ascii_lowercase + string.digits + special_characters

    # Process combinations for 1 to 3-character strings
    with ProcessPoolExecutor(max_workers=10) as process_pool:
        total_combinations = sum(len(characters) ** length for length in range(1, 5))
        with tqdm(total=total_combinations) as pbar:
            for length in range(1, 5):  # From 1 to 4
                combinations = itertools.product(characters, repeat=length)
                futures = [process_pool.submit(process_combinations, combination) for combination in combinations]
                for future in as_completed(futures):
                    pbar.update(1)