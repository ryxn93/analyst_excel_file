import os  
import sys  
import pandas as pd  
from search_folder import find_excel_file  

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
        print(f"Error, terjadi kesalahan: {e}")  
        return None  

def read_column(nama_file, sheet_name):  
    try:  
        rescol = []  
        excel_file = pd.read_excel(nama_file, sheet_name=sheet_name)  
        for col in excel_file.columns:  
            rescol.append(col)  
        return rescol  
    except FileNotFoundError:  
        print(f"Error: file '{nama_file}' tidak ditemukan!")  
        return None  
    except KeyError as e:  
        print(f"Error: kolom '{e}' tidak ditemukan didalam file excel!")  
        return None  
    except Exception as e:  
        print(f"terjadi kesalahan: {e}")  
        return None  

def read_data(nama_file, sheet_name, columns):  
    try:  
        excel_file = pd.read_excel(nama_file, sheet_name=sheet_name)  
        selected_data = excel_file[columns]  
        return selected_data  
    except KeyError as e:  
        print(f"Error: kolom '{e}' tidak ditemukan!")  
        return None  
    except Exception as e:  
        print(f"terjadi kesalahan: {e}")  
        return None  

def main():  
    file_name = "../../data/Data Pengajuan - Penerbitan 2024-11.xlsx"  
    
    sheets = read_sheet(file_name)  
    
    for i, sheet in enumerate(sheets):  
        print(f"[{i}] {sheet}")  
    input_sheet = int(input("enter sheet number: "))   
    sheet_name = sheets[input_sheet]  
    
    selected_columns_excel_file = read_column(file_name, sheet_name)  
    if selected_columns_excel_file is not None:  
        for j, listcol in enumerate(selected_columns_excel_file):  
            print(f"[{j}] {listcol}")  
        
        column_indices = input("Input column indices (comma-separated): ")  
        try:  
            indices = [int(i) for i in column_indices.split(",")]  
            columns = [selected_columns_excel_file[i] for i in indices]  
        except (ValueError, IndexError):  
            print("Input tidak valid. Pastikan menggunakan indeks yang benar.")  
            return  

    hasil = read_data(file_name, sheet_name, columns)  
    if hasil is not None:  
        print(f"Data from columns '{columns}':")  
        # print("test", hasil)  
        
        # Define the mapping of input column names to required names  
        column_mapping = {  
            'submit_date': 'tanggal_submit',  
            'validation_date': 'tgl_validasi',  
            'published_date': 'tanggal_terbit',  
            'payment_date': 'tanggal_pembayaran'  
        }  

        # Rename columns based on the mapping  
        hasil.rename(columns=column_mapping, inplace=True)  

        required_columns = ['tanggal_submit', 'tgl_validasi', 'tanggal_terbit', 'tanggal_pembayaran']  
        if all(col in hasil.columns for col in required_columns):  
            for col in required_columns:  
                hasil[col] = pd.to_datetime(hasil[col], errors='coerce')  
            
            hasil['interval_seconds_validasi'] = (hasil['tgl_validasi'] - hasil['tanggal_submit']).dt.total_seconds()  
            hasil['interval_seconds_terbit'] = (hasil['tanggal_terbit'] - hasil['tanggal_pembayaran']).dt.total_seconds()  
            
            def convert_seconds(seconds):  
                if pd.isnull(seconds):  
                    return "N/A"  
                seconds = int(seconds)  
                days = seconds // 86400  
                hours = (seconds % 86400) // 3600  
                minutes = (seconds % 3600) // 60  
                seconds = seconds % 60  
                return f"{days} hari, {hours} jam, {minutes} menit, {seconds} detik"  

            hasil['interval_waktu_validasi'] = hasil['interval_seconds_validasi'].apply(convert_seconds)  
            hasil['interval_waktu_terbit'] = hasil['interval_seconds_terbit'].apply(convert_seconds)  
            print(hasil)  
        else:  
            print("Kolom yang diperlukan tidak lengkap dalam data.")  

if __name__ == "__main__":  
    try:  
        main()  
    except KeyboardInterrupt:  
        exit(1)