#!/usr/bin/env python3
import csv
import json
import re
import argparse
from colorama import init
init()
from colorama import Fore, Back, Style

"""
json_data=open(file_directory).read()

data = json.loads(json_data)
pprint(data)
"""

def print_good(*args):
	print("["+ Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL + "] ", end="")
	print(*args)

def print_warn(*args):
	print("["+ Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL + "] ", end="")
	print(*args)

def print_info(*args):
	print("[i] ", end="")
	print(*args)

if __name__ == "__main__":

	# cli arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("csvfile", help="The path to the Checking.csv provided from wellsfargo.com")
	parser.add_argument("-c", action="store", default="config.json", dest="config_file", help="The Path to the config file. (Default: config.json)")
	args = parser.parse_args()

	config = 0 # initial value has no bearing
	# load config file
	print_info("Loading config file")
	try:
		with open(args.config_file) as f:
			config = json.load(f)
			print_good("Config file loaded")
	except Exception as err:
		print_warn("An error was thrown. Take a look.")
		print(err)
		exit(1)

	transactions = [] # initial value has no bearing
	# load account data
	print_info("Loading csv file")
	try:
		with open(args.csvfile, newline="") as csvfile:
			reader =  csv.reader(csvfile, delimiter=",", quotechar="\"")
			for row in reader:
				transactions.append(row)
			print_good("Csv file loaded")
	except Exception as err:
		print_warn("An error was thrown. Take a look.")
		print(err)
		exit(1)

	print_info("Generating report\n")

	# iterate over dictionary `config`, let k and v be key-value data
	for k, v in config.items():
		for row in transactions:
			continue
			#print(row[0])

