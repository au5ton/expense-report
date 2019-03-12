[![CircleCI](https://circleci.com/gh/au5ton/expense-report.svg?style=svg)](https://circleci.com/gh/au5ton/expense-report)

# expense-report
personal tool for parsing CSV files provided by Wells Fargo

## Installation
- clone repository
- `pip3 install -r requirements.txt`
- `python3 -m expense-report`

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
This program will only run with the use of a `config.json` file. A default one is included with the repository and can be modified as necessary. Below is an example and doesn't reflect the live repository version.
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

#### example.csv
This is the exact format that Wells Fargo provides. I am unsure what columns 3 and 4 are intended for, but this program makes no use of them.
```csv
"01/31/2019","-4.00","*","","PURCHASE AUTHORIZED ON 01/30 HEB #999 HOUSTON TX S1234567890 CARD 7865"
"01/22/2019","-1.07","*","","PURCHASE AUTHORIZED ON 01/20 GOOGLE*SAM RUSTON G.CO HELPPAY# CA S1234567890 CARD 7865"
"01/18/2019","-5.62","*","","PURCHASE AUTHORIZED ON 01/17 MCDONALD'S COLLEGE STATI TX S1234567890 CARD 7865"
"01/15/2019","746.00","*","","DUNDER MIFFLIN REG SALARY JOHN DOE"
"01/07/2019","-8.09","*","","PURCHASE AUTHORIZED ON 01/04 CHEVRON #999 HOUSTON TX S1234567890 CARD 7865"
"01/03/2019","-19.00","*","","PURCHASE AUTHORIZED ON 01/02 999 GREAT CLIPS AT HOUSTON TX S1234567890 CARD 7865"
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

## TODO
- document `--grouped`
- document `section`
- print section totals
