
from colorama import init
init()
from colorama import Fore, Back, Style

verbose = False

def set_verbose(v):
	global verbose
	verbose = v

def print_good(*args):
	global verbose
	if verbose == False:
		return
	print("["+ Fore.GREEN + Style.BRIGHT + "✓" + Style.RESET_ALL + "] ", end="")
	print(*args)

def print_warn(*args):
	global verbose
	if verbose == False:
		return
	print("["+ Fore.RED + Style.BRIGHT + "✗" + Style.RESET_ALL + "] ", end="")
	print(*args)

def print_info(*args):
	global verbose
	if verbose == False:
		return
	print("[i] ", end="")
	print(*args)