import pandas as pd

# Đọc file CSV
df = pd.read_csv('D:\\Nhon_work\\NorthwestTerritories\\table_data.csv')

# Loại bỏ các dòng trùng lặp
df_unique = df.drop_duplicates()

# Lưu lại file CSV đã loại bỏ trùng lặp
df_unique.to_csv('D:\\Nhon_work\\NorthwestTerritories\\NorthwestTerritories.csv', index=False)
