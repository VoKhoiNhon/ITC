import requests
from bs4 import BeautifulSoup
import itertools
import string
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import csv
from tqdm import tqdm
import threading
import time

# URLs and headers
url = "https://cofs.lara.state.mi.us/SearchApi/Search/Search/GetSearchResults"
headers = {
    "Referer": "https://cofs.lara.state.mi.us/SearchApi/Search/Search",
}
base_url = "https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSummary.aspx?token="

# Global variables for tracking records
record_count = 0
file_index = 1
data_lock = threading.Lock()

def fetch_data(search_value, start, end):
    """ Fetch data from the server """
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
        response = requests.post(url, headers=headers, data=data, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            filtered_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(base_url)]
            return filtered_links
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return []

def save_data(search_value, link, count, index):
    """ Save data to CSV file """
    filename = f"/home/customer/michigan/link/data_{index}.csv"
    with open(filename, "a", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow([search_value, link, count, index])

def process_combinations(combination):
    """ Process character combinations """
    global record_count, file_index
    search_value = ''.join(combination)
    all_links = []
    
    with ProcessPoolExecutor(max_workers=20) as thread_pool:
        futures = [thread_pool.submit(fetch_data, search_value, start, start + 100)
                   for start in range(1, 10001, 100)]
        
        for future in as_completed(futures):
            result = future.result()
            if result:
                all_links.extend(result)
    
    # Save results
    if all_links:
        for link in all_links:
            with data_lock:
                record_count += 1
                if record_count > 100000:
                    file_index += 1
                    record_count = 1
            save_data(search_value, link, record_count, file_index)
    else:
        no_results_filename = "/home/customer/michigan/link/no_results.csv"
        with open(no_results_filename, "a", newline='') as no_results_file:
            csv_writer = csv.writer(no_results_file)
            csv_writer.writerow([search_value])
    
def update_progress():
    """ Update data count every 10 minutes """
    while True:
        time.sleep(600)  # 10 minutes
        with data_lock:
            print(f"Records processed: {record_count}, File index: {file_index}")

if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()
    special_characters = string.punctuation + ' '
    characters = string.ascii_lowercase + string.digits + special_characters

    # Start the progress update thread
    progress_thread = threading.Thread(target=update_progress, daemon=True)
    progress_thread.start()

    # Process combinations
    with ProcessPoolExecutor(max_workers=12) as process_pool:
        total_combinations = sum(36 ** length for length in range(3, 5))
        with tqdm(total=total_combinations) as pbar:
            for length in range(3, 5):
                combinations = itertools.product(characters, repeat=length)
                futures = [process_pool.submit(process_combinations, combination) for combination in combinations]
                for future in as_completed(futures):
                    pbar.update(1)
