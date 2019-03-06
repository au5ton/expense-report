#!/usr/bin/env python3
import csv
import json
import re


"""
json_data=open(file_directory).read()

data = json.loads(json_data)
pprint(data)
"""

if __name__ == "__main__":

	config = 0
	with open("config.json") as f:
		config = json.load(f)

	# iterate over dictionary `config`, let k and v be key-value data
	for k, v in config.items():
		print(str(k)+": ", end="")
		print(v)

	with open("checking.csv", newline="") as csvfile:
		reader = csv.reader(csvfile, delimiter=",", quotechar="\"")
		for row in reader:
			continue
			#print(row[1])
			#print(', '.join(row))
