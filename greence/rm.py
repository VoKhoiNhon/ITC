def remove_duplicates(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Sử dụng set để loại bỏ các dòng trùng lặp
    unique_lines = set(lines)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)

# Gọi hàm với tên file cần xử lý
remove_duplicates('D:\\Nhon_work\\greence\\com_ids.txt', 'D:\\Nhon_work\\greence\\ids.txt')
