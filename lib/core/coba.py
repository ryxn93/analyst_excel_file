import os, sys, math
import pandas as pd
from search_folder import find_excel_file
# from lib.core.search_folder import find_excel_file
# sys.path.append(os.path.abspath('../lib/core'))
# print("Python Path:", sys.path)  

def read_sheet(nama_file):
    try:
        data = []
        excel_file = pd.ExcelFile(nama_file)
        print("File excel berhasil dibaca!")
        for i, sheet in enumerate(excel_file.sheet_names):
            data.append(sheet)
        return data
    except FileNotFoundError:
        print(f"Error, file '{nama_file}' tidak ditemukan!")
    except Exception as e:
        print(f"Error , terjadi kesalahan: {e}")
        return None
 
def read_column(nama_file, sheet_name):
    try:
        rescol = []
        excel_file = pd.read_excel(nama_file, sheet_name=sheet_name)
        for col in excel_file:
            rescol.append(col)
            # print(f"- {col}")
        return rescol
        # selected_column_excel_file = excel_file[columns]
    except FileNotFoundError:
        print(f"Error: file '{nama_file}' tidak ditemukan!")
        return None
    except KeyError as e: 
        print(f"Error: kolom '{e}' tidak ditemukan didalam file excel!")
        return None
    except Exception as e:
        print(f"terjadi kesalahan: {e}")
        return None
    
def read_data(nama_file, sheet_name, column):
    try:
        excel_file = pd.read_excel(nama_file, sheet_name=sheet_name)
        selected_data = excel_file[column]
        return selected_data
    except KeyError as e:
        print(f"Error: kolom '{column}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"terjadi kesalahan: {e}")
        return None
    
def convert_seconds(seconds):
    if pd.isnull(seconds):
        return "N/A"
    seconds = int(seconds)
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{days} hari, {hours} jam, {minutes} menit, {seconds} detik"


def main():
    file_name = "../../data/Data Pengajuan - Penerbitan 2024-11.xlsx"
    
    sheets = read_sheet(file_name)
    
    for i, sheet in enumerate(sheets):
        print(f"[{i}] {sheet}")
    input_sheet = int(input("enter sheet number: ")) 
    sheet_name = sheets[input_sheet]
    
    selected_columns_excel_file= read_column(file_name, sheet_name )
    if selected_columns_excel_file is not None:
        for j, listcol in enumerate (selected_columns_excel_file):
            print(f"[{j}] {listcol}")
        # input_column = int(input("input col: "))
        # if input_column:
        #     columns = selected_columns_excel_file[input_column]
        column_indices = input("Input column indices (comma-separated): ")
        try:  
            indices = [int(i) for i in column_indices.split(",")]  
            columns = [selected_columns_excel_file[i] for i in indices]
            # print(f"col: {columns}")  
        except (ValueError, IndexError):  
            print("Input tidak valid. Pastikan menggunakan indeks yang benar.")  
            return  

    hasil = read_data(file_name, sheet_name, columns)
    
    if hasil is not None:  
        print(f"Data from columns {columns}:")  
        print(hasil)
        
        
        
        
        for col in columns:
            if pd.api.types.is_datetime64_any_dtype(hasil[col]):
                hasil[f'interval_seconds_{col}'] = (hasil[col].shift(-1) - hasil[col]).dt.total_seconds()
                hasil[f'interval_waktu_{col}'] = hasil[f'interval_seconds_{col}'].apply(convert_seconds)
                print(hasil[[col, f'interval_seconds_{col}', f'interval_waktu_{col}']])
                # hasil[f'interval_seconds_{col}'] = (hasil[col] - hasil[col].shift()).dt.total_seconds()
                # print(hasil[[col, f'interval_seconds_{col}']])
            else:
                print(f"Column '{col}' is not a datetime column.")
                    
    # if hasil is not None:  
    #     print(f"Data from column '{columns}':")  
    #     print("test", hasil)
    #     # return hasil
    
    #     # required_columns = ['tanggal_submit', 'tgl_validasi', 'tanggal_terbit', 'tanggal_pembayaran']
    #     if (col in hasil for col in columns):
    #         # if col in hasil and for col in columns
    #         for col in columns[:-1]:
    #             print(f"ccc {col}")
    #             if hasil[col] == pd.to_datetime(hasil[col], errors='coerce'):
    #                 hasil['interval_seconds_validasi'] = (hasil[col] - hasil[col]).dt.total_seconds()
    #                 # hasil['interval_seconds_terbit'] = (hasil['tanggal_terbit'] - hasil['tanggal_pembayaran']).dt.total_seconds()
    #                 print(hasil)
    #                 # hasil['interval_waktu_validasi'] = hasil['interval_seconds_validasi'].apply(convert_seconds)
    #                 # hasil['interval_waktu_terbit'] = hasil['interval_seconds_terbit'].apply(convert_seconds)
                    
    #             # elif hasil[col] == pd.to_datetime(hasil[col], errors='coerce'):
    #             #     hasil['interval_seconds_validasi'] = (hasil['tgl_validasi'] - hasil['tanggal_submit']).dt.total_seconds()
    #             #     hasil['interval_seconds_terbit'] = (hasil['tanggal_terbit'] - hasil['tanggal_validasi']).dt.total_seconds()
                    
    #             #     hasil['interval_waktu_validasi'] = hasil['interval_seconds_validasi'].apply(convert_seconds)
    #             #     hasil['interval_waktu_terbit'] = hasil['interval_seconds_terbit'].apply(convert_seconds)
                    
                    
    #             # else:
    #             #     pass
                    
    #             # hasil['interval_waktu_validasi'] = hasil['interval_seconds_validasip'].apply(convert_seconds)
    #             # print(hasil)
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt):
        exit(1)
        
        
# a = set() '''uniq value'''
# a.add("asdf")
# def compare_strings(list1, list2):
#     return [item for item in list1 if item in list2]

# list1 = ["apple", "banana", "cherry"]
# list2 = ["banana", "cherry", "date"]

# common_elements = compare_strings(list1, list2)
# print("Common elements:", common_elements)