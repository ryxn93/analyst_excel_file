import os, sys
import pandas as pd

def read_sheet(file_name):
    try:
        data = []
        xlsx = pd.ExcelFile(file_name)
        print(f"File '{file_name}' berhasil dibaca!")
        for i, sheet in enumerate(xlsx.sheet_names):
            data.append(sheet)
        return data
    except FileNotFoundError:
        print(f"File '{file_name}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"terjadi kesalahan: {e}")
        return None
            
def read_column (file_name, sheet_name):
    try:
        result_column = []
        xlsx = pd.read_excel(file_name, sheet_name=sheet_name)
        for column in xlsx:
            result_column.append(column)
        return result_column
    except FileNotFoundError:
        print(f"Error: file '{file_name}' tidak ditemukan!")
        return None
    except KeyError as e:
        print(f"kolom '{e}' tidak ditemukan!")
        return None
    except Exception as e:
        print(f"terjadi kesalahan: '{e}'")
        return None
        
def main():
    file_name = ' '
    sheets = read_sheet(file_name)
    
    for i, sheet in enumerate(sheets):
        print(f"[{i}] {sheet}")
    input_sheet = int(input("enter sheet number: "))
    sheet_name = sheets[input_sheet]
    
    selected_column = read_column (file_name, sheet_name)
    # if selected_column is not None:
    for j, listcol in enumerate (selected_column):
        print (f"[{j}] {listcol}")
if __name__ == "__main__":
    main()