
import json
import csv

from .pretty_print import print_good, print_warn, print_info

def jsonf(config_file):
	try:
		with open(config_file) as f:
			config = json.load(f)
			print_good("Config file loaded")
	except Exception as err:
		print_warn("An error was thrown. Take a look.")
		print(err)
		exit(1)
	return config
	
def csvf(csvfile):
	transactions = []
	try:
		with open(csvfile, newline="") as f:
			reader = csv.reader(f, delimiter=",", quotechar="\"")
			for row in reader:
				transactions.append(row)
			print_good("Csv file loaded")
	except Exception as err:
		print_warn("An error was thrown. Take a look.")
		print(err)
		exit(1)
	return transactions