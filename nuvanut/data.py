# from bs4 import BeautifulSoup
# import json
# import requests
# from concurrent.futures import ThreadPoolExecutor

# def fetch_business_info(business_id):
#     url = f"https://nni.gov.nu.ca/business/profile/{business_id}"

#     headers = {
#         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#         "Accept-Language": "en-GB,en;q=0.9",
#         "Cache-Control": "max-age=0",
#         "Connection": "keep-alive",
#         "Sec-Fetch-Dest": "document",
#         "Sec-Fetch-Mode": "navigate",
#         "Sec-Fetch-Site": "none",
#         "Sec-Fetch-User": "?1",
#         "Upgrade-Insecure-Requests": "1",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
#         "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": "\"Windows\""
#     }

#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     data = {}
#     table = soup.find('table')
#     if table:
#         for row in table.find_all('tr'):
#             cells = row.find_all(['td'])
#             if len(cells) == 2:
#                 key = cells[0].get_text(strip=True)
#                 value = cells[1].get_text(strip=True)
#                 data[key] = value
#     else:
#         business_name = soup.find('h1').get_text(strip=True)
#         # status_message = soup.find('div', class_='visually-hidden').find_next('em').get_text(strip=True) if soup.find('div', class_='visually-hidden') else None
#         status_div = soup.find('div', role='contentinfo')
#         status_message = status_div.get_text(strip=True) if status_div else "Status message not found"

#         # Loại bỏ "Status message" khỏi thông báo trạng thái
#         status_message = status_message.replace("Status message", "").strip()
#         data = {
#             "Business Name": business_name,
#             "Status": status_message
#         }
    
#     return business_id, data

# def save_to_json(business_id, data):
#     with open('D:\\Nhon_work\\canada\\info1.json', 'a') as json_file:
#         json.dump({business_id: data}, json_file)
#         json_file.write("\n")  # Append a comma for the next entry

# def main():
#     # Create or overwrite the file initially

#     with ThreadPoolExecutor(max_workers=100) as executor:
#         futures = {executor.submit(fetch_business_info, business_id): business_id for business_id in range(1, 10000)}
        
#         for future in futures:
#             business_id = futures[future]
#             try:
#                 id, result = future.result()
#                 # Check if the Business Name is "Page not found"
#                 if result.get("Business Name") != "Page not found":
#                     save_to_json(id, result)
#             except Exception as e:
#                 print(f"Error fetching data for ID {business_id}: {e}")


#     print("Data saved to business_info.json")

# if __name__ == "__main__":
#     main()
from bs4 import BeautifulSoup
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm

def fetch_business_info(business_id):
    url = f"https://nni.gov.nu.ca/business/profile/{business_id}"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {"Business Number": business_id}  # Start with the business ID
    business_name = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Business Name not found"
    data["Business Name"] = business_name  # Add the Business Name to data

    table = soup.find('table')
    if table:
        for row in table.find_all('tr'):
            cells = row.find_all(['td'])
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                data[key] = value
    else:
        status_div = soup.find('div', role='contentinfo')
        status_message = status_div.get_text(strip=True) if status_div else "Status message not found"
        status_message = status_message.replace("Status message", "").strip()
        data["Status"] = status_message

    return business_id, data

def save_to_json(data_list):
    with open('D:\\Nhon_work\\canada\\info1.json', 'w') as json_file:
        json.dump(data_list, json_file)

def main():
    results = []
    business_ids = range(1, 10000)

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(fetch_business_info, business_id): business_id for business_id in business_ids}
        
        for future in tqdm(futures, desc="Fetching Business Info"):
            business_id = futures[future]
            try:
                id, result = future.result()
                if result.get("Business Name") != "Page not found":
                    results.append({id: result})
            except Exception as e:
                print(f"Error fetching data for ID {business_id}: {e}")

            # Optional: add a delay between requests to avoid rate limits
            time.sleep(0.1)

    save_to_json(results)
    print("Data saved to info1.json")

if __name__ == "__main__":
    main()
