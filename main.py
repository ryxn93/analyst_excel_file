import sys, os
import pandas as pd
from argparse import ArgumentParser
from lib.core.invoke import CoreExcelOps
from lib.utils.logger import Logger as L
from lib.core.handle_data2 import HandleData


parser = ArgumentParser(prog= 'analyst_excel_file')
parser.add_argument("--file", "-f", help="specify file location", dest="file", required=True)
parser.add_argument("--sheet", "-s", help="input sheet name")
parser.add_argument("--column", "-c", help="input column name")
args = parser.parse_args()
file_path = args.file


run = CoreExcelOps(file_name=args.file)
opt = HandleData()


if args.file:
    print(f"the -f option is called {file_path}")
    a = run.read_sheet()
    for i, sheets in enumerate(a):
        L.info(f"[{i}] {sheets}")
    
if args.sheet:
    print(f"the -s option is called {file_path} {args.sheet}")
    run.read_column(args.sheet)
    
if args.column:
    print(f"the -c option is called {file_path} {args.column}")
    run.read_data(file_path, args.sheet, args.column)
    
if not (args.sheet or args.column):
    sheet = run.read_sheet()
    input_sheet = int(input("input sheet: "))
    
    res_columns, df= run.read_column(sheet_name=sheet[input_sheet])
    for i, cols_name in enumerate(res_columns):
        L.info(f"[{i}] {cols_name}")
    
    key=int(input("Select one of the columns to perform the sorting operation. Enter column number: "))
    sorted_data = opt.sort_data(df=df, columns=res_columns[key])
    print("Sorted Data: ")
    print(sorted_data)
    
    filter_data = opt.filtered_data(df=df, column=res_columns[key])
    print(filter_data)
    
    for j, col1 in enumerate(res_columns):
        L.info(f"[{j}] {col1}")
    # input_col = input("Input column (comma-separated): ")
    input_col_to_opt_time = "1,4,6,7,8,9"
    indices = [int(k) for k in input_col_to_opt_time.split(",")]
    print(f"number: {indices}")
    
    columns = [res_columns[item] for item in indices]
    data = run.read_data(sheet_name=sheet[input_sheet], column=columns)
    print(f"DATAAA: {data}")
    convert_interval_to_sec, data_columns = opt.date_time_delta(data, columns)
    print("interval columns: ", data_columns)
    print(convert_interval_to_sec)
    
    for l, col2 in enumerate (data_columns):
        print(f"[{l}] {col2}")
    input_col_to_opt_group = input("Enter the column number to perform group opt by interval: ")
    indikator = [int(m) for m in input_col_to_opt_group.split(",")]
    print(f"number col input: {indikator}")
    column_intrv = [data_columns[items] for items in indikator]
    print(f"cek column_intv: {column_intrv}")
    
    group_interval = opt.category_interval(df=convert_interval_to_sec, column=column_intrv)
    print(group_interval)
    
    format_date = opt.fmt_date(df=convert_interval_to_sec, column=data_columns)
    print(format_date)
    
    opt.plot_bar_chart(group_interval, 'Interval Distribution', 'Interval', 'Count')