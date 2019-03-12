
import re

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
			reserved[item]["section"] = "Generated Section"
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