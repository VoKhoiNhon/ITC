import requests
from bs4 import BeautifulSoup
import json
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import random
from tqdm import tqdm
import threading
import multiprocessing

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

# List of proxies
file_lock = threading.Lock()
def fetch_data(article_id):
    # max_retries = len(proxies_list)
    max_retries = 250
    for attempt in range(max_retries):
        # proxy = random.choice(proxies_list)
        # proxies = {
        #     "http": proxy,
        #     "https": proxy
        # }

        data_payload = {
            "Id": article_id
        }

        try:
            response = requests.post(url, headers=headers, data=data_payload)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            section_title = soup.find('h2', class_='section-title').get_text(strip=True)
            entity_details = {
                "Entity type":section_title, 
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
            with file_lock:
                with open('D:\\Nhon_work\\North_Calirona\\northcalirona\\results_data.json', 'a') as outfile:
                    json.dump(final_data, outfile)
                    outfile.write('\n')
    
            # print(f"Data for article_id {article_id} saved to output_data.json")
            break  # Exit the loop if successful

        except requests.RequestException as e:
            print(f"Request failed for article_id {article_id}")
            # Optionally, wait before retrying
            time.sleep(1)

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
                address_parts.append(elem.get_text(separator=" ", strip=True))
            elif elem.name == 'br':
                continue
            if elem.find_next_sibling(name='p') is None:
                break
        return address_parts
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

# Use ThreadPoolExecutor within a ProcessPoolExecutor to parallelize the fetching
# def process_article_ids(article_ids):
#     with ThreadPoolExecutor(max_workers=7) as executor:
#         executor.map(fetch_data, article_ids)

# def main():
#     # Load JSON data from file
#     data = []
#     with open('D:\\Nhon_work\\North_Calirona\\northcalirona\\id_ar.json', 'r') as file:
#             data = [json.loads(line)['article_id'] for line in file]
    
#     # Check that data is loaded
#     if not data:
#         print("No valid data found.")
#         return

#     # Determine the number of workers and chunk size
#     num_workers = multiprocessing.cpu_count()
#     chunk_size = max(1, len(data) // 5)  # Prevent chunk_size from being 0
    
#     # Debugging: Check chunk_size
#     print(f"Chunk size: {chunk_size}")

#     # Split data into chunks for each worker
#     chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

#     # Debugging: Check the number of chunks
#     print(f"Number of chunks: {len(chunks)}")

#     # Use ProcessPoolExecutor to process the chunks of article IDs
#     with ThreadPoolExecutor(max_workers=200) as executor:
#         # Pass the function reference and the chunks to the executor
#         executor.map(fetch_data, chunks)

# if __name__ == "__main__":
#     main()
# def process_article_ids(article_ids):
#     # Iterate through article_ids and fetch data
#     for article_id in tqdm(article_ids, desc="Processing Article IDs", unit="ID"):
#         fetch_data(article_id)

# def main():
#     # Load JSON data from file
#     data = []
#     with open('D:\\Nhon_work\\North_Calirona\\northcalirona\\id_ar.json', 'r') as file:
#         data = [json.loads(line)['article_id'] for line in file]
    
#     # Check that data is loaded
#     if not data:
#         print("No valid data found.")
#         return

#     # Use ThreadPoolExecutor for parallel execution
#     with ThreadPoolExecutor(max_workers=200) as executor:
#         # Pass chunks of data to the executor
#         chunk_size = max(1, len(data) // 200)  # Chunk size for splitting the data
#         chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
#         # Map chunks to the process_article_ids function with a progress bar
#         list(tqdm(executor.map(process_article_ids, chunks), desc="Processing Chunks", total=len(chunks)))

# if __name__ == "__main__":
#     main()
def main():
    # Load JSON data from file
    data = []
    with open('D:\\Nhon_work\\North_Calirona\\northcalirona\\id_ar.json', 'r') as file:
        data = [json.loads(line)['article_id'] for line in file]
    
    # Check that data is loaded
    if not data:
        print("No valid data found.")
        return

    # Use ThreadPoolExecutor for parallel execution
    with ThreadPoolExecutor(max_workers=200) as executor:
        # Map each article_id to fetch_data function directly
        # Using tqdm for progress bar
        list(tqdm(executor.map(fetch_data, data), desc="Processing Article IDs", total=len(data)))

if __name__ == "__main__":
    main()