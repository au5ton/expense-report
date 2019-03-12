
from colorama import init
init()
from colorama import Fore, Back, Style

def print_report(report):
	last_section = ""

	# dict is sorted by alphabetical order of flag `f`
	for k, v in sorted(report.items(), key=_wrap):
		# starting a new section
		if(last_section != v["section"]):
			last_section = v["section"]
			if(v["section"] is not ""):
				print("\n", end="")
				print(v["section"])
				print("=" * len(v["section"]))
		print(Style.BRIGHT + k + ": " + Style.RESET_ALL + "\t", end="")
		print(Fore.MAGENTA + str(round(v["sum"],3)) + Style.RESET_ALL)
	
	print("\n", end="")
	
def _wrap(d):
		return d[1]["section"]