import json
from bs4 import BeautifulSoup
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor,as_completed
from tqdm import tqdm
import time
import os

def safe_find_text(soup, *args, **kwargs):
    element = soup.find(*args, **kwargs)
    return element.text.strip() if element else 'N/A'

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
        response = requests.get(url, headers=headers, timeout=6000000)
        time.sleep(1)  # Be polite and avoid overwhelming the server
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')



        # Extracting existing data
        id_number = safe_find_text(soup, 'span', id='MainContent_lblIDNumberHeader')
        entity_name = safe_find_text(soup, 'span', id='MainContent_lblEntityNameHeader')

        # Update to extract previous entity name and date of change
        previous_entity_name_td = soup.find('td', string='The name was changed from:')
        if previous_entity_name_td:
            previous_entity_name_change = previous_entity_name_td.find_next('div').text.strip()
            date_of_change = previous_entity_name_td.find_next('b').text.strip().split('on')[-1].strip() if previous_entity_name_td.find_next('b') else 'N/A'
        else:
            previous_entity_name_change = date_of_change = 'N/A'

        entity_type = safe_find_text(soup, 'span', id='MainContent_lblEntityType')
        identification_number_old = safe_find_text(soup, 'span', id='MainContent_lblOldIDNumber')
        incorporation_date = safe_find_text(soup, 'span', id='MainContent_lblOrganisationDate')
        dissolution_date = safe_find_text(soup, 'span', id='MainContent_lblInactiveDate')
        term = safe_find_text(soup, 'span', id='MainContent_lblTerm')
        most_recent_ar = safe_find_text(soup, 'span', id='MainContent_lblMostRecentAnnualReportYear')
        most_recent_ar_officers = safe_find_text(soup, 'span', id='MainContent_lblMostRecentAnnualReportWithOfficersAndDirectors')

        # Extract Resident Agent Details
        resident_agent_name = safe_find_text(soup, 'span', id='MainContent_lblResidentAgentName')
        resident_agent_street = safe_find_text(soup, 'span', id='MainContent_lblResidentStreet')
        resident_agent_city = safe_find_text(soup, 'span', id='MainContent_lblResidentCity')
        resident_agent_state = safe_find_text(soup, 'span', id='MainContent_lblResidentState')
        resident_agent_zip = safe_find_text(soup, 'span', id='MainContent_lblResidentZip')
        resident_agent_apartment = safe_find_text(soup, 'span', id='MainContent_lblaptsuiteother')  # Assuming the ID is correct

        # Extract Principal Office Mailing Address
        mailing_street = safe_find_text(soup, 'span', id='MainContent_lblPrincipleStreet')
        mailing_city = safe_find_text(soup, 'span', id='MainContent_lblPrincipleCity')
        mailing_state = safe_find_text(soup, 'span', id='MainContent_lblPrincipleState')
        mailing_zip = safe_find_text(soup, 'span', id='MainContent_lblPrincipleZip')
        mailing_apartment = safe_find_text(soup, 'span', id='MainContent_lblaptsuiteotherlblpricipal')  # Assuming the ID is correct

        # Extract Officers and Directors
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

        # Extract Act Formed Under
        act_formed_under = safe_find_text(soup, 'span', id='MainContent_lblActsFormedUnder')

        # Extract Total Authorized Shares
        total_authorized_shares = safe_find_text(soup, 'span', id='MainContent_lblSum')

        # Return structured data in the requested format
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
                'Street Address': resident_agent_street,
                'Apartment/Suite/Other': resident_agent_apartment,
                'City': resident_agent_city,
                'State': resident_agent_state,
                'Zip Code': resident_agent_zip
            },
            'Registered Office Mailing Address': {
                'P.O. Box or Street Address': mailing_street,
                'Apt/Suite/Other': mailing_apartment,
                'City': mailing_city,
                'State': mailing_state,
                'Zip Code': mailing_zip
            },
            'Officers and Directors': officers,
            'Act Formed Under': act_formed_under,
            'Total Authorized Shares': total_authorized_shares
        }
    except Exception as e:
        return {'url': url, 'error': str(e)}

def save_data(data, filepath):
    with open(filepath, 'a') as json_file:
        json_file.write(json.dumps(data) + '\n')

if __name__ == "__main__":
    input_filepath = 'D:\\Nhon_work\\michigan_data\\cout.txt'
    output_filepath = 'D:\\Nhon_work\\michigan_data\\test\\entities_details_again1.json'
    failed_filepath = 'D:\\Nhon_work\\michigan_data\\data\\failed_urls.txt'

    # Load existing data if the file exists
    all_data = []
    if os.path.exists(output_filepath):
        with open(output_filepath, 'r') as json_file:
            all_data = [json.loads(line) for line in json_file]

    failed_urls = []

    with open(input_filepath, 'r') as file:
        urls = file.readlines()

    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = {executor.submit(scrape_entity_data, url.strip()): url.strip() for url in urls if url.strip()}
        
        for future in tqdm(as_completed(futures), total=len(futures)):
            result = future.result()
            if 'error' in result:
                failed_urls.append(result)
            else:
                all_data.append(result)

                # Incrementally save the data after each successful scrape
                save_data(result, output_filepath)  # Save each result as a separate line

    # Save the failed URLs after processing all
    with open(failed_filepath, 'w') as fail_file:
        for failed in failed_urls:
            fail_file.write(f"URL: {failed['url']}, Error: {failed['error']}\n")