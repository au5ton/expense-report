
from colorama import init
init()
from colorama import Fore, Back, Style

def print_report(report):
	for section in report["sections"]:
		print("\n", end="")
		print(section["title"])
		print("=" * len(section["title"]))
		for group in section["groups"]:
			print(Style.BRIGHT + group["name"] + ": " + Style.RESET_ALL + "\t", end="")
			print(Fore.MAGENTA + str(round(group["sum"], 3)) + Style.RESET_ALL)
		if len(section["meta"]) > 0:
			print("-" * len(section["title"]))
			for group in section["meta"]:
				print(Style.BRIGHT + group["name"] + ": " + Style.RESET_ALL + "\t", end="")
				print(Fore.MAGENTA + str(round(group["sum"], 3)) + Style.RESET_ALL)
	print("\n", end="")