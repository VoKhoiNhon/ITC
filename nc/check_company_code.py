import json

def read_ids_from_txt(txt_file):
    with open(txt_file, 'r', encoding='utf-8') as f:
        ids = [line.strip() for line in f if line.strip()]
    return ids

def write_missing_ids_to_txt(missing_ids, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for id in missing_ids:
            f.write(f"{id}\n")

def read_ids_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('company_codes', [])

# Đường dẫn tới file
id_file_path = 'D:\\Nhon_work\\North_Calirona\\northcalirona\\sos_ids.txt'
company_code_file_path = 'D:\\Nhon_work\\North_Calirona\\company_code.json'
output_file_path = 'D:\\Nhon_work\\North_Calirona\\not_in_id.txt'

# Đọc dữ liệu từ file soid.txt
id_company_codes = read_ids_from_txt(id_file_path)

# Đọc dữ liệu từ file company_code.json
company_codes_in_file = read_ids_from_json(company_code_file_path)

# Tìm các company_code có trong company_code.json nhưng không có trong soid.txt
not_in_id_codes = set(company_codes_in_file) - set(id_company_codes)

# Lưu các company_code này vào file not_in_id.txt
write_missing_ids_to_txt(not_in_id_codes, output_file_path)

print(f"Đã lưu các company_code không có trong soid.txt vào file {output_file_path}.")
