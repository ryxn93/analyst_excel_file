import pandas as pd  

from lib.utils.logger import Logger as L

def read_sheets_name(file_name):  
    try:  
        excel_file = pd.ExcelFile(file_name)  
        return excel_file.sheet_names
    except FileNotFoundError:  
        L.error(f"File '{file_name}' not found!")  
    except Exception as e:  
        L.error(f"Error: {e}")  
        return None  

def read_columns_name(file_name, sheet_name):  
    try:  
        excel_file = pd.read_excel(file_name, sheet_name=sheet_name)  
        return list(excel_file.columns)
    except FileNotFoundError:  
        L.error(f"File {file_name} not found!")  
        return None  
    except KeyError as e:  
        L.error(f"Coulmn not found")  
        return None  
    except Exception as e:  
        L.error(f"{e}")  
        return None  

def read_data_in_column(file_name, sheet_name, columns):  
    try:  
        excel_file = pd.read_excel(file_name, sheet_name=sheet_name)  
        selected_data = excel_file[columns]  
        return selected_data[0:11]
    except KeyError as e:  
        L.error(f"Coulmn not found")  
        return None  
    except Exception as e:  
        L.error(f"{e}")
        return None  
    

def convert_seconds(seconds):  
    if pd.isnull(seconds):  
        return "N/A"  
    seconds = int(seconds)  
    days = seconds // 86400  
    hours = (seconds % 86400) // 3600  
    minutes = (seconds % 3600) // 60  
    seconds = seconds % 60  
    return f"{days:02d} D, {hours:02d}h:{minutes:02d}m:{seconds:02d}s"  

def main():  
    file_name = "./data/Data Pengajuan - Penerbitan 2024-11.xlsx"  
    
    sheets = read_sheets_name(file_name)  
    
    for i, sheet in enumerate(sheets):  
        print(f"[{i}] {sheet}")  
    # input_sheet = int(input("enter sheet number: "))   
    
    input_sheet = 0
    sheet_name = sheets[input_sheet]  
    
    selected_columns_excel_file = read_columns_name(file_name, sheet_name)  
    
    if selected_columns_excel_file is not None:  
        for j, listcol in enumerate(selected_columns_excel_file):  
            print(f"[{j}] {listcol}")  
        
        # column_indices = input("Input column indices (comma-separated): ")  
        input_columns = "6, 7, 8, 9"
        
        try:  
            split_by_comma = [int(i) for i in input_columns.split(",")]  
            select_columns_by_index = [selected_columns_excel_file[i] for i in split_by_comma]  
        except (ValueError, IndexError):  
            L.error("Invalid input, please enter right index!")  
            return  

    data_columnn = read_data_in_column(file_name, sheet_name, select_columns_by_index)  
    
    if data_columnn is None:
        return 
    
    for col in select_columns_by_index:
        data_columnn[col] = pd.to_datetime(data_columnn[col], errors="coerce")
    
    if len(select_columns_by_index) % 2 != 0:
        L.error("invalid column")
        return
    
    for i in range(0, len(select_columns_by_index), 2):
        start_col = select_columns_by_index[i]
        end_col = select_columns_by_index[i + 1]
        
        interval_col = f"interval_seconds_{i//2 + 1}"
        data_columnn[interval_col] = (data_columnn[end_col] - data_columnn[start_col]).dt.total_seconds()
        data_columnn[f"interval_waktu_{i//2 + 1}"] = data_columnn[interval_col].apply(convert_seconds)

    print(data_columnn)

if __name__ == "__main__":  
    try:  
        main()  
    except KeyboardInterrupt:  
        exit(1)