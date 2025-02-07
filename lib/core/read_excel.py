import os, sys, math
import pandas as pd
from lib.core.search_folder import find_excel_file
from lib .utils.logger import Logger
# from lib.core.search_folder import find_excel_file
# sys.path.append(os.path.abspath('../lib/core'))
# print("Python Path:", sys.path)  

def read_sheet(nama_file):
    try:
        data = []
        excel_file = pd.ExcelFile(nama_file)
        Logger.success("File excel berhasil dibaca!")
        for i, sheet in enumerate(excel_file.sheet_names):
            data.append(sheet)
        for i, item in enumerate(data):
            print(f"[{i}] {item}")
    except FileNotFoundError:
        Logger.error(f"Error, file '{nama_file}' tidak ditemukan!")
        return None
    except Exception as e:
        Logger.error(f"Error , terjadi kesalahan: {e}")
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
        Logger.error(f"Error: file '{nama_file}' tidak ditemukan!")
        return None
    except KeyError as e: 
        Logger.error(f"Error: kolom '{e}' tidak ditemukan didalam file excel!")
        return None
    except Exception as e:
        Logger.error(f"terjadi kesalahan: {e}")
        return None
    
def read_data(nama_file, sheet_name, column):
    try:
        excel_file = pd.read_excel(nama_file, sheet_name=sheet_name)
        selected_data = excel_file[column]
        return selected_data[0:11]
    except KeyError as e:
        Logger.error(f"Error: kolom '{column}' tidak ditemukan!")
        return None
    except Exception as e:
        Logger.error(f"terjadi kesalahan: {e}")
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
    file_name = "./data/Data Pengajuan - Penerbitan 2024-11.xlsx"
    
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
            Logger.error("Input tidak valid. Pastikan menggunakan indeks yang benar.")  
            return  

    hasil = read_data(file_name, sheet_name, columns)
    
    if hasil is not None:  
        Logger.debug(f"Data from columns {columns}:")
        # print(hasil)
        
        for col in columns:  
    # Periksa apakah kolom bertipe datetime  
            if pd.api.types.is_datetime64_any_dtype(hasil[col]):  
        # Jika ada kolom yang tidak bertipe datetime, informasikan dan lewati  
                if len(columns) % 2 != 0:  
                    Logger.warn("Invalid number of columns for interval calculation.")  
                    return  
        
                for i in range(0, len(columns), 2):  
                    start_col = columns[i]  
                    end_col = columns[i + 1]  

                    # Pastikan kolom adalah datetime  
                    if pd.api.types.is_datetime64_any_dtype(hasil[start_col]) and pd.api.types.is_datetime64_any_dtype(hasil[end_col]):  
                        interval_col = f"interval_seconds_{i//2 + 1}"  
                        hasil[interval_col] = (hasil[end_col] - hasil[start_col]).dt.total_seconds()  
                        hasil[f"interval_waktu_{i//2 + 1}"] = hasil[interval_col].apply(convert_seconds)  
                    else:  
                        Logger.info(f"Skipping columns '{start_col}' and '{end_col}' as they are not both datetime columns.")  
                        
            else:  
                print(f"Column '{col}' is not a datetime column. No operation performed.")  

                # Tampilkan hasil akhir  
        Logger.success(hasil)
                
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