import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from tqdm import tqdm  # Import tqdm
import time

# Load company codes from JSON file
with open('D:\\Nhon_work\\North_Calirona\\company_code.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    company_codes = data.get("company_codes", [])

# Define URL and headers
url = 'https://www.sosnc.gov/online_services/search/Business_Registration_Results'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'en,vi;q=0.9,en-GB;q=0.8,en-US;q=0.7',
    'cache-control': 'max-age=0',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'ASP.NET_SessionId=yyj22cvkpasa5dwjufcwfrcr; __RequestVerificationToken=gVLxTenFX6yq9wj9unpBEmL5DujOVM-UM7zMY1ZEyGST2SNCgpC0-vCzOJ1EMSAVvQRhBI1Zfi2H3z7H3UZICbLNeII1; _gid=GA1.2.1246038449.1730687080; _ga_FC1YEDLDBJ=GS1.1.1730691021.2.1.1730691022.0.0.0; _ga=GA1.2.1160022206.1730687079; _gat_gtag_UA_71814177_4=1',
    'origin': 'https://www.sosnc.gov',
    'referer': 'https://www.sosnc.gov/online_services/search/by_title/_Business_Registration',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36 Edg/128.0.0.0',
}

MAX_RETRIES = 3  # Maximum number of retries

def fetch_article_ids(company_code, file_lock):
    for attempt in range(MAX_RETRIES):
        try:
            payload = {
                '__RequestVerificationToken': 'Xd2TNU5W2pCxRHlEuSWuxpHzEG1QHgSLB4QdMgZrTN8dTUnEuqCLaRGSmfaxx_rRAW-yG6pHiWoP5ylFOU0UmI3fU0c1',
                'CorpSearchType': 'CORPORATION',
                'EntityType': 'ORGANIZATION',
                'Words': 'SOSID',
                'SearchCriteria': company_code,
                'IndividualsSurname': '',
                'FirstPersonalName': '',
                'AdditionalNamesInitials': ''
            }

            response = requests.post(url, headers=headers, data=payload, timeout=120)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                article_tags = soup.find_all('article', itemscope=True, itemtype='http://schema.org/Thing')
                
                # Extract article IDs
                article_ids = [tag.get('id') for tag in article_tags if tag.get('id')]
                
                record = {"company_code": company_code, "article_id": article_ids[0] if article_ids else None}
                
                with file_lock:
                    with open('D:\\Nhon_work\\North_Calirona\\northcalirona\\id_ar.json', 'a') as file:
                        file.write(json.dumps(record) + '\n')
                
                return record
            
            else:
                print(f"Received status code {response.status_code} for {company_code}")

        except requests.RequestException as e:
            print(f"Error fetching data for {company_code}: {e}")

        # Wait before retrying
        time.sleep(2 ** attempt)  # Exponential backoff

    print(f"Failed to fetch data for {company_code} after {MAX_RETRIES} attempts")
    record = {"company_code": company_code}
    
    with file_lock:
        with open('D:\\Nhon_work\\North_Calirona\\northcalirona\\id_fail.txt', 'a') as file:
            file.write(json.dumps(record) + '\n')
    
    return record

def main():
    file_lock = threading.Lock()
    with ThreadPoolExecutor(max_workers=250) as executor:
        # Wrap company_codes with tqdm for progress tracking
        futures = {executor.submit(fetch_article_ids, company_code, file_lock): company_code for company_code in company_codes}

        # Use tqdm to track progress
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing", unit="request"):
            future.result()  # Ensuring all futures are completed

if __name__ == "__main__":
    main()
