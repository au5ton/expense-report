#!/usr/bin/env python3
import csv
import json
import re
import argparse
from colorama import init
init()
from colorama import Fore, Back, Style

def print_good(*args):
	if verbose == False:
		return
	print("["+ Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL + "] ", end="")
	print(*args)

def print_warn(*args):
	if verbose == False:
		return
	print("["+ Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL + "] ", end="")
	print(*args)

def print_info(*args):
	if verbose == False:
		return
	print("[i] ", end="")
	print(*args)

def generate_report(config, transactions):
	"""Generate Report

	Args:
		config (dict): Parsed JSON data that holds the configuration for the report.
		transactions (list): Parsed CSV data that holds the transactions in the exact structure as provided by Wells Fargo

	Returns:
		dict: Dictionary of report data where each entry has properties: flags, sum

	"""
	
	# d4 = {}' 'for d in (d1, d2, d3): d4.update(d)

	# report object to return
	report = dict()

	# indexes of rows of `transactions`
	DATE = 0
	AMOUNT = 1
	INFO = 4

	# fill `report` with user-defined values
	# iterate over dictionary `config`, let k and v be key-value data
	for k, v in config.items():
		# initialize the 2d dictionary
		report[k] = dict()
		report[k]["flags"] = v["flags"]
		report[k]["sum"] = 0
		report[k]["section"] = v["section"] if "section" in v else ""
		# 
		for row in transactions:
			r = re.compile(v["regex"])
			# if this is the type of transaction we're looking for
			if(r.search(row[INFO]) != None):
				# record sums				
				if("--debits-only" in v["flags"]):
					if(float(row[AMOUNT]) < 0.0):
						report[k]["sum"] += float(row[AMOUNT])
				elif("--credits-only" in v["flags"]):
					if(float(row[AMOUNT]) > 0.0):
						report[k]["sum"] += float(row[AMOUNT])
				else:
					report[k]["sum"] += float(row[AMOUNT])
	
	# generate special values based on flags
	reserved = dict()
	reserved_keywords = ["Grouped debits", "Grouped credits", "Ungrouped debits", "Ungrouped credits", "Total debits", "Total credits", "Net Total"]
	for item in reserved_keywords:
		if(item not in reserved):
			reserved[item] = dict()
			reserved[item]["flags"] = ""
			reserved[item]["section"] = "Automatic"
			reserved[item]["sum"] = 0
	
	# iterate over dictionary `config`, let k and v be key-value data
	for k, v in config.items():
		# initialize the 2d dictionary
		for row in transactions:
			r = re.compile(v["regex"])
			# if this is the type of transaction we're looking for
			if(r.search(row[INFO]) != None):
				if("--grouped" in v["flags"]):
					if(float(row[AMOUNT]) < 0.0):
						reserved["Grouped debits"]["sum"] += float(row[AMOUNT])
					if(float(row[AMOUNT]) > 0.0):
						reserved["Grouped credits"]["sum"] += float(row[AMOUNT])
	
	for row in transactions:
		# totals
		if(float(row[AMOUNT]) < 0.0):
				reserved["Total debits"]["sum"] += float(row[AMOUNT])
		if(float(row[AMOUNT]) > 0.0):
			reserved["Total credits"]["sum"] += float(row[AMOUNT])
		# Net
		reserved["Net Total"]["sum"] += float(row[AMOUNT])
			
	reserved["Ungrouped debits"]["sum"] = reserved["Total debits"]["sum"] - reserved["Grouped debits"]["sum"]
	reserved["Ungrouped credits"]["sum"] = reserved["Total credits"]["sum"] - reserved["Grouped credits"]["sum"]
	
	concatenated = dict()
	for d in (report, reserved):
		concatenated.update(d)
	
	return concatenated

last_section = ""

def print_report(report):
	global last_section
	
	def wrap(d):
		return d[1]["section"]

	# dict is sorted by alphabetical order of flag `f`
	for k, v in sorted(report.items(), key=wrap):
		# starting a new section
		if(last_section != v["section"]):
			last_section = v["section"]
			if(v["section"] is not ""):
				print("\n", end="")
				print(v["section"])
				print("=" * len(v["section"]))
		print(Style.BRIGHT + k + ": " + Style.RESET_ALL + "\t", end="")
		print(Fore.MAGENTA + str(round(v["sum"],3)) + Style.RESET_ALL)
	
	print("\n", end="")
		

if __name__ == "__main__":

	# cli arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("csvfile", help="The path to the Checking.csv provided from wellsfargo.com")
	parser.add_argument("-c", action="store", default="config.json", dest="config_file", help="The Path to the config file. (Default: config.json)")
	parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	global verbose
	verbose = args.verbose

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
	report = generate_report(config, transactions)
	print_report(report)

