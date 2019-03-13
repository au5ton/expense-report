
import re
import copy

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
	


def sum_group(**args):
	"""Sum_group
	Calculates the sum with the provided filters as named variables.
	Parameters with a * denote that it's required.
	- * transactions (parsed csv)
	- * regex (string)
	- flags (string)
	"""
	
	if "transactions" not in args: 
		raise Exception("`transactions` is a required parameter of sum_group(**args)")
	if "regex" not in args:
		raise Exception("`regex` is a required parameter of sum_group(**args)")
	
	# total sum
	sigma = 0.0
	# indexes of rows of `transactions`
	DATE = 0
	AMOUNT = 1
	INFO = 4
	
	for row in transactions:
		conditions_met = True
		# if arg provided
		if access(args, "regex") != None:
			# note if condition is not met
			r = re.compile(access(args, "regex"))
			if(r.search(row[INFO]) == None):
				conditions_met = False
		if access(args, "flags") != None:
			# note if condition is not met
			if("--debits-only" in access(args, "flags")):
				# if not a debit
				if(float(row[AMOUNT]) >= 0.0):
					conditions_met = False
			if("--credits-only" in access(args, "flags")):
				# if not a credit
				if(float(row[AMOUNT]) <= 0.0):
					conditions_met = False
		if conditions_met == True:
			sigma += float(row[AMOUNT])
	return sigma

def sum_section(**args):
	"""Sum_section
	Calculates the sum with the provided filters as named variables.
	Parameters with a * denote that it's required.
	- * transactions (parsed csv)
	- * section (object)
	- flags (string)
	"""
	
	if "transactions" not in args: 
		raise Exception("`transactions` is a required parameter of sum_section(**args)")
	if "section" not in args:
		raise Exception("`section` is a required parameter of sum_section(**args)")
	
	# total sum
	sigma = 0.0
	# indexes of rows of `transactions`
	DATE = 0
	AMOUNT = 1
	INFO = 4
	
	for group in args["section"]["groups"]:
		sigma += sum_group(
						transactions=access(args, "transactions"), 
						regex=access(group, "regex"),
						flags=access(group, "flags") if "flags" not in args else access(args, "flags"))

def sum_config(**args):
	"""Sum_config
	Calculates the sum with the provided filters as named variables.
	Parameters with a * denote that it's required.
	- * transactions (parsed csv)
	- * config (object)
	- flags (string)
	- only_section (string)
	"""
	
	if "transactions" not in args: 
		raise Exception("`transactions` is a required parameter of sum_config(**args)")
	if "config" not in args:
		raise Exception("`config` is a required parameter of sum_config(**args)")

# Return None if the key isn't found, otherwise return the value
def access(d, key):
	if key in d:
		return d[key]
	else:
		return None

if __name__ == '__main__':
	sum(transactions=[], regex="hello")