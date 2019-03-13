
import re
import copy
import json

"""
New functions
- generate_report
- mutate_group_sums
- mutate_meta_section_sums
- mutate_overall_totals
"""

def generate_report(config, transactions):
	report = {}
	report["sections"] = copy.deepcopy(config)
	mutate_group_sums(report, transactions)
	mutate_meta_section_sums(report, transactions)
	mutate_overall_totals(report, transactions)
	return report

def mutate_group_sums(report, transactions):
	for section in report["sections"]:
		for group in section["groups"]:
			group["sum"] = sum_group(transactions=transactions, regex=access(group, "regex"), flags=access(group, "flags"))

def mutate_meta_section_sums(report, transactions):
	for section in report["sections"]:
		section["meta"] = []
		if "meta_prop" not in section:
			section["meta_prop"] = []
		for prop in section["meta_prop"]:
			if(prop == "net_total"):
				d = dict()
				d["name"] = "Net total"
				d["flag"] = None
				d["regex"] = None
				d["sum"] = sum_section(transactions=transactions, section=section, flags="")
				section["meta"].append(d)
			if(prop == "debit_total"):
				d = dict()
				d["name"] = "Total debits"
				d["flag"] = None
				d["regex"] = None
				d["sum"] = sum_section(transactions=transactions, section=section, flags="--debits-only")
				section["meta"].append(d)
			if(prop == "credit_total"):
				d = dict()
				d["name"] = "Total credits"
				d["flag"] = None
				d["regex"] = None
				d["sum"] = sum_section(transactions=transactions, section=section, flags="--credits-only")
				section["meta"].append(d)

def mutate_overall_totals(report, transactions):
	# this is honestly more succinct
	sect = json.loads("""
	{
		"title": "Overall totals",
		"exclusive": false,
		"optional": false,
		"groups": [
			{
				"name": "Total debits",
				"flags": null,
				"regex": null,
				"sum": 0
			},
			{
				"name": "Total credits",
				"flags": null,
				"regex": null,
				"sum": 0
			},
			{
				"name": "Net total",
				"flags": null,
				"regex": null,
				"sum": 0
			}
		],
		"meta": []
	}
	""")
	for group in sect["groups"]:
		if(group["name"] == "Total debits"):
			group["sum"] = sum_group(transactions=transactions, regex="^.*$", flags="--debits-only")
		if(group["name"] == "Total credits"):
			group["sum"] = sum_group(transactions=transactions, regex="^.*$", flags="--credits-only")
		if(group["name"] == "Net total"):
			group["sum"] = sum_group(transactions=transactions, regex="^.*$", flags="")
	
	report["sections"].append(sect)
	


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
	
	for row in access(args, "transactions"):
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
	return sigma

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
		
	# total sum
	sigma = 0.0
	# indexes of rows of `transactions`
	DATE = 0
	AMOUNT = 1
	INFO = 4
	
	for section in access(args, "config"):
		if "only_section" in args:
			if access(args, "only_section") != access(section, "title"):
				continue
			
		sigma += sum_section(
				 transactions=access(args, "transactions"),
				 section=section,
				 flags=access(section, "flags"))
	return sigma

# Return None if the key isn't found, otherwise return the value
def access(d, key):
	if key in d:
		return d[key]
	else:
		return None