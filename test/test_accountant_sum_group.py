
import unittest
import os
import sys 
sys.path.append('..')

from src import load
from src import accountant

example_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "example.csv")
csvdata = load.csvf(example_file)

class AccountantTest(unittest.TestCase):

	# test sum_group
	def test_sum_group_valid(self):
		sigma = accountant.sum_group(transactions=csvdata, regex="^.*(CHEVRON).*$")
		self.assertAlmostEqual(sigma, -36.24)
		
	def test_sum_group_exception_1(self):
		self.assertRaises(Exception, accountant.sum_group, regex="^.*(CHEVRON).*$")
		
	def test_sum_group_exception_2(self):
		self.assertRaises(Exception, accountant.sum_group, transactions=csvdata)
		
	def test_sum_group_exception_3(self):
		self.assertRaises(Exception, accountant.sum_group)

if __name__ == '__main__':
	unittest.main() 