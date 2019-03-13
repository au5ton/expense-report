[![CircleCI](https://circleci.com/gh/au5ton/expense-report.svg?style=svg)](https://circleci.com/gh/au5ton/expense-report)

# expense-report
personal tool for parsing CSV files provided by Wells Fargo

## Installation
- clone repository
- `pip3 install -r requirements.txt`
- `python3 -m src` run the script (or `main.sh`)

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
[ //array of every section
	{
		"title": "Home",
		"exclusive": false, //not yet implemented
		"optional": false, //if the sum of the section is zero, omit the entire section
		"groups": [ //every group within a section
			{
				"name": "internet",
				"flags": "",
				"regex": "^.*(SUDDENLINK).*$" //the sum of every purchase matching this regex
			},
			{
				"name": "electricity",
				"flags": "",
				"regex": "^.*(ENTERGY).*$"
			},
			{
				"name": "utilities",
				"flags": "",
				"regex": "^.*(CITY OF NAVASOTA).*$"
			},
			{
				"name": "groceries",
				"flags": "",
				"regex": "^.*(ARLANS|H-E-B|WAL-MART).*$" //purchase contains "ARLANS" or "H-E-B" or "WAL-MART"
			}
		],
		"meta_prop": ["debit_total", "credit_total", "net_total"] //automatically calculate the sums of the entire section
	},
	{
		"title": "Entertainment",
		"exclusive": false,
		"optional": false,
		"groups": [
			{
				"name": "server hosting",
				"flags": "",
				"regex": "^.*(DIGITALOCEAN|WHATBOX).*$"
			},
			{
				"name": "music",
				"flags": "",
				"regex": "^.*(BANDCAMP).*$"
			},
			{
				"name": "patreon",
				"flags": "",
				"regex": "^.*(PATREON).*$"
			}
		]
	},
	{
		"title": "Transportation",
		"exclusive": false,
		"optional": false,
		"groups": [
			{
				"name": "gasoline",
				"flags": "",
				"regex": "^.*(CHEVRON|EXXONMOBIL|GAS).*$"
			}
		]
	}
]
```

#### example.csv
This is the exact format that Wells Fargo provides. I am unsure what columns 3 and 4 are intended for, but this program makes no use of them.
```csv
"03/11/2019","-83.02","*","","PURCHASE AUTHORIZED ON 03/08 TAKE 5 OIL CHANGE COLLEGE STATI TX S0123456789 CARD 1234"
"03/08/2019","-16.23","*","","PURCHASE AUTHORIZED ON 03/08 AUTOZONE 3535 2706 TEXAS COLLEGE STATI TX P0123456789 CARD 1234"
"03/08/2019","-3.45","*","","PURCHASE AUTHORIZED ON 03/07 MCDONALD'S F123456 NAVASOTA TX S0123456789 CARD 1234"
"03/07/2019","-16.76","*","","PURCHASE AUTHORIZED ON 03/06 CHEVRON 0123456 NAVASOTA TX S0123456789 CARD 1234"
"03/06/2019","-9.80","*","","PURCHASE AUTHORIZED ON 03/04 PAYPAL *UBER 402-935-7733 CA S0123456789 CARD 1234"
"03/06/2019","-1.00","*","","PURCHASE AUTHORIZED ON 03/03 BANDCAMP FORHILL bandcamp.com CA S0123456789 CARD 1234"
"03/05/2019","-1.25","*","","PURCHASE AUTHORIZED ON 03/02 MUNICIPAL ONLINE P 844-7244507 TX S0123456789 CARD 1234"
"03/04/2019","-35.54","*","","PURCHASE AUTHORIZED ON 03/02 H-E-B #619 COLLEGE STATI TX P0123456789 CARD 1234"
"03/04/2019","-109.99","*","","PURCHASE AUTHORIZED ON 03/02 CITY OF NAVASOTA - 936-825-6475 TX S0123456789 CARD 1234"
"03/04/2019","-9.15","*","","PURCHASE AUTHORIZED ON 03/01 APL* ITUNES.COM/BI 866-712-7753 CA S0123456789 CARD 1234"
"03/04/2019","-5.92","*","","RECURRING PAYMENT AUTHORIZED ON 03/01 DIGITALOCEAN.COM DIGITALOCEAN. NY S0123456789 CARD 1234"
"03/01/2019","-19.48","*","","PURCHASE AUTHORIZED ON 02/28 CHEVRON 0123456 NAVASOTA TX S0123456789 CARD 1234"
"03/01/2019","320.00","*","","TX A&M ENG EX ST REG SALARY 12345 DOE JOHN"
```

#### Output
```
Home
====
internet:       0.0
electricity:    0.0
utilities:      -109.99
groceries:      -35.54
----
Total debits:   -145.53
Total credits:  0.0
Net total:      -145.53

Entertainment
=============
server hosting:         -5.92
music:  -1.0
patreon:        0.0

Transportation
==============
gasoline:       -36.24

Overall totals
==============
Total debits:   -311.59
Total credits:  320.0
Net total:      8.41
```

## Downloading CSV files from Wells Fargo
[Wells Fargo has a support page on this topic](https://www.wellsfargo.com/help/online-banking/comma-delimited/)

## TODO
- ungrouped feature
- write more unit tests