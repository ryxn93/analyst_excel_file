import os

def find_excel_file(fileloc: str):
    cwd = os.getcwd()
    print(f"ASDFASDF: {fileloc}")
    dirname = os.path.dirname(cwd)

    data_directory = os.path.join(dirname, '../data')
    
    print(f"data: {data_directory}")

    if os.path.exists(data_directory):
        print("Folder 'data' ditemukan!")
    else:
        print("Folder 'data' tidak ditemukan.")
        
def main():
    find_excel_file()
    
if __name__ == "__main__":
    main()