# expense-report
personal tool for parsing CSV files provided by Wells Fargo

## Installation
- clone repository
- `pip3 install -r requirements.txt`

## Usage
```
usage: report.py [-h] [-c CONFIG_FILE] csvfile

positional arguments:
  csvfile         The path to the Checking.csv provided from wellsfargo.com

optional arguments:
  -h, --help      show this help message and exit
  -c CONFIG_FILE  The Path to the config file. (Default: config.json)
```

## Configuration
This program will only run with the use of a `config.json` file. A default one is included with the repository and can be modified as necessary.
```javascript
{
	"gasoline": {
		"regex": "^.*(CHEVRON|EXXONMOBIL).*$", // match transactions with the words "CHEVRON" or "EXXONMOBIL" in the description
		"flags": "--debits-only" // only count the sum of the debits (-X amount)
	},
	"total debits": {
		"regex": ".", // match transactions with any description (every transaction)
		"flags": "--debits-only"
	},
	"total credits": {
		"regex": ".",
		"flags": "--credits-only" // only count the sum of the credits (+X amount)
	},
	"total net": { // determine the sum of every transaction
		"regex": ".",
		"flags": ""
	}
}
```
#### Output
```
gasoline:       -44.87
total debits:   -500.00
total credits:  1250.00
total net:       750.00
```


## Downloading CSV files from Wells Fargo
[Wells Fargo has a support page on this topic](https://www.wellsfargo.com/help/online-banking/comma-delimited/)