import sys, os
from argparse import ArgumentParser

from lib.core.read_excel import read_excel



parser = ArgumentParser()

parser.add_argument("--file", "-f", help="specify file location")
args = parser.parse_args()

if args.file:
    print(f"opsi -f terpanggil {args.file}")
    read_excel(args.file)