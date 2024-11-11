import requests
import json
import concurrent.futures
import os
from tqdm import tqdm  # Thư viện tqdm để hiển thị thanh tiến độ

# Đường dẫn lưu trữ dữ liệu
output_file = 'D:\\Nhon_work\\Switzerland\\data\\Switzerland_data.json'

# Hàm để gửi yêu cầu và lấy dữ liệu
def fetch_data(id):
    url_without_shab_pub = f'https://www.zefix.admin.ch/ZefixREST/api/v1/firm/{id}/withoutShabPub.json'
    url_with_shab_pub = f'https://www.zefix.admin.ch/ZefixREST/api/v1/firm/{id}/shabPub.json'
    
    try:
        response_without_shab_pub = requests.get(url_without_shab_pub, timeout=3600)
        data_without_shab_pub = response_without_shab_pub.json()
        
        response_with_shab_pub = requests.get(url_with_shab_pub, timeout=3600)
        data_with_shab_pub = response_with_shab_pub.json()

        # Kết hợp dữ liệu từ hai API
        return {
            'id': id,
            'without_shab_pub': data_without_shab_pub,
            'with_shab_pub': data_with_shab_pub
        }
    except Exception as e:
        print(f"An error occurred for ID {id}: {e}")
        return None

# Hàm để lưu dữ liệu vào tệp JSON từng dòng
def save_data(data):
    if data is not None:
        with open(output_file, 'a', encoding='utf-8') as json_file:  # Mở với chế độ 'a' để thêm
                json.dump(data, json_file)
                json_file.write("\n")  # Ghi thêm dòng mới sau mỗi mục

# Danh sách các ID cần fetch
ids = range(1, 3000001)

# Sử dụng ThreadPoolExecutor để tạo luồng
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    future_to_id = {executor.submit(fetch_data, id): id for id in ids}
    
    # Tạo thanh tiến độ với tqdm
    for future in tqdm(concurrent.futures.as_completed(future_to_id), total=len(future_to_id), desc='Fetching data'):
        id = future_to_id[future]
        try:
            data = future.result()
            save_data(data)  # Chỉ lưu nếu dữ liệu hợp lệ
        
        except Exception as e:
            print("")

print("Tất cả dữ liệu đã được lưu vào Switzerland_data.json")
