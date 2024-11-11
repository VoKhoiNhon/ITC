import requests
from bs4 import BeautifulSoup
import json
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing

# Load article IDs from JSON file
with open('/home/customer/North_Calirona/data_detail/data_id.json', 'r') as file:
    data = json.load(file)

# Define the URL and headers for the POST request
url = "https://www.sosnc.gov/online_services/search/_Business_Registration_profile"

headers = {
    "accept": "*/*",
    "accept-language": "en,vi;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.sosnc.gov",
    "referer": "https://www.sosnc.gov/online_services/search/Business_Registration_Results",
    "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 Edg/129.0.0.0",
    "x-requested-with": "XMLHttpRequest"
}

def fetch_data(article_id):
    max_retries = 10000  # Adjust the number of retries as needed
    
    for attempt in range(max_retries):
        data_payload = {
            "Id": article_id
        }

        try:
            response = requests.post(url, headers=headers, data=data_payload)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            entity_details = {
                "Legal Name": extract_text_after_label(soup, "Legal Name"),
                "Previous Legal Name": extract_text_after_label(soup, "Prev Legal Name"),
                "SosId": extract_text_after_label(soup, "SosId:"),
                "Status": extract_text_after_label(soup, "Status:"),
                "Date Formed": extract_text_after_label(soup, "Date Formed:"),
                "Citizenship": extract_text_after_label(soup, "Citizenship:"),
                "Fiscal Month": extract_text_after_label(soup, "Fiscal Month:"),
                "Annual Report Due Date": extract_text_after_label(soup, "Annual Report Due Date:")
            }

            registered_agent = extract_text_after_label(soup, "Registered Agent:")

            addresses = {}
            for label in ["Mailing", "Principal Office", "Reg Office", "Reg Mailing"]:
                addresses[label] = extract_address(soup, label)

            officers = extract_officers(soup)
            stock_info = extract_stock(soup)

            final_data = {
                "Article ID": article_id,
                "Entity Details": entity_details,
                "Registered Agent": registered_agent,
                "Addresses": addresses,
                "Officers": officers,
                "Stock": stock_info
            }

            # Append data to file immediately
            with open('/home/customer/North_Calirona/data/res.json', 'a') as outfile:
                json.dump(final_data, outfile, indent=4)
                outfile.write(',\n')

            print(f"Data for article_id {article_id} saved to results_data.json")
            time.sleep(1)  # Reduced sleep time
            break  # Exit the loop if successful

        except requests.RequestException as e:
            print(f"Request failed for article_id {article_id}: {e}")
            # Optionally, wait before retrying
            time.sleep(2)  # Reduced wait time between retries

def extract_text_after_label(soup, label_text):
    label_element = soup.find(string=lambda text: text and label_text in text)
    if label_element:
        span_element = label_element.find_next('span')
        if span_element:
            return span_element.get_text(strip=True)
    return "Not Found"

def extract_address(soup, label):
    address_element = soup.find(string=lambda text: text and label in text)
    if address_element:
        address_parts = []
        next_elements = address_element.find_all_next(['span', 'br'])
        for elem in next_elements:
            if elem.name == 'span' and elem.get_text(strip=True):
                address_parts.append(elem.get_text(strip=True))
            elif elem.name == 'br':
                continue
            if elem.find_next_sibling(name='p') is None:
                break
        return ', '.join(address_parts)
    return "Not Found"

def extract_officers(soup):
    officers = []
    for officer in soup.find_all('p'):
        title_element = officer.find('span', class_='greenLabel')
        name_element = officer.find('a')
        if title_element and name_element:
            title = title_element.get_text(strip=True)
            name = ' '.join(name_element.get_text(strip=True).split())
            address = ', '.join(officer.get_text(strip=True).split('\n')[-4:])
            officers.append({
                "Title": title,
                "Name": name,
                "Address": address
            })
    return officers

def extract_stock(soup):
    stock_info = {}
    for stock_class in ['COMMON', 'PREFERRED']:
        stock_section = soup.find(string=lambda text: text and stock_class in text)
        if stock_section:
            shares_element = stock_section.find_next(string=lambda text: text and "Shares:" in text)
            no_par_value_element = stock_section.find_next(string=lambda text: text and "No Par Value:" in text)
            if shares_element and no_par_value_element:
                shares = shares_element.find_next('span').get_text(strip=True)
                no_par_value = no_par_value_element.find_next('span').get_text(strip=True) == "Yes"
                stock_info[f"{stock_class.capitalize()} Stock"] = {
                    "Shares": int(shares.replace(',', '')),
                    "No Par Value": no_par_value
                }
    return stock_info

def process_article_ids(article_ids):
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(fetch_data, article_ids)

def main():
    num_workers = min(multiprocessing.cpu_count(), 20)  # Use a sensible number of workers
    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for chunk in chunks:
            article_ids = [item.get("article_id") for item in chunk]
            executor.submit(process_article_ids, article_ids)

if __name__ == "__main__":
    main()
