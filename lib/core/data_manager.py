import os, sys
import pandas as pd  
from datetime import datetime, timedelta  

def filter_by_province(data, province_filter):  
    # Ensure that the province filter is a string 
    df = pd.read_excel(data) 
    province = str(province_filter).strip().upper()  # Normalize case and trim  
    
    # Filtering the DataFrame  
    try:  
        filtered_data = df.loc[df['provinsi'] == province]  
        return filtered_data
    except Exception as e:
        print("Error during filtering:", {e})  
 
data = '../../data/Data Pengajuan - Penerbitan 2024-11.xlsx'

int_province = input("masukkan nama provinsi: ")
print(f'{int_province.strip().upper()}')

filtered_result = filter_by_province(data, int_province)  
print("TES", filtered_result)

print(f"Filtered data for {int_province}:")
for i, dt in enumerate (filtered_result):
    print(f"[{i}] {dt}")