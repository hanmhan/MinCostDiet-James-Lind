
import pandas as pd
import numpy as np
import json
import requests

import pprint
import helper
from helper import HelperFucClass as hfc
#pd.set_option('display.width', 1000)
#pd.set_option('display.max_columns', 20)




#print (ndb.ndb_search(ndb.apikey,"Broccoli"))







def nutrition_dataframe_beta1(foods = ['milk','broccoli'],c = 'safeway',exact_word = True, key = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2', debug = 0, mode = 'ui'):

	if debug == 1:
		d1 = ['45109162', '45361064']
		d2 = ['test.json','test2.json']
		df = pd.DataFrame(hfc.debug1(d2,key = key))
		return df

	hfc.mode = mode
	hfc._exact_word = exact_word
	df = pd.DataFrame(hfc.ndhelper1( foods, c),columns = ['Food Name','Nutrients', 'Value']).set_index(['Food Name' ,'Nutrients' ])
	print (hfc._ora)
	print ( "[" + ", ".join(hfc._ora) + ']  do/does not exist'  if len(hfc._ora) != 0 else '')
	hfc._ora = []
	return df
	"""except:
		print (hfc._ora)
		print ( " ".join(hfc._ora) + 'do/does not exist'  if len(hfc._ora) != 0 else '')
		return"""


def test():
	return pd.read_csv('Project2Data_Sheet1.csv')
	#return requests.get('https://docs.google.com/spreadsheets/u/1/d/1d8t2PHjkGs2pOcx1aTfWZBCiJtFV-QCScxws_B98-aw/edit#gid=0')
def merge_nd():
	x = 'https://docs.google.com/spreadsheets/u/1/d/1d8t2PHjkGs2pOcx1aTfWZBCiJtFV-QCScxws_B98-aw/edit#gid=0'
	pass

def save_nd():
	pass

def open_nd():
	pass


#x = nutrition_dataframe_beta1( foods = ['frozen broccoli'])
y = test()
yy = y['Food'].iloc
#ora = nutrition_dataframe_beta1
#asdf = ora(foods= list(yy[5:7]),mode='test')
