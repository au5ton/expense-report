import csv
import json
import argparse

from .pretty_print import print_good, print_warn, print_info
from . import pretty_print
from . import accountant
from . import ui

def run():

	# cli arguments
	parser = argparse.ArgumentParser()
	parser.add_argument("csvfile", help="The path to the Checking.csv provided from wellsfargo.com")
	parser.add_argument("-c", action="store", default="config.json", dest="config_file", help="The Path to the config file. (Default: config.json)")
	parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()
	pretty_print.set_verbose(args.verbose)

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
	report = accountant.generate_report(config, transactions)
	ui.print_report(report)



if __name__ == '__main__':
	run() 