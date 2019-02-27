
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







def nutrition_dataframe_beta1(foods = ['milk','broccoli'],c = 'safeway',key = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2', debug = 0, mode = 'ui'):


	if debug == 1:
		d1 = ['45109162', '45361064']
		d2 = ['test.json','test2.json']
		df = pd.DataFrame(hfc.debug1(d2,key = key))
		return df


	if mode == 'ui':
		if len(foods) > 1:

			df = pd.DataFrame(hfc.ndhelper1( foods, c),columns = ['Food Name','Nutrients', 'Value']).set_index(['Food Name' ,'Nutrients' ])
			return df


	if mode == 'test':
		return hfc.ndhelper1(foods,c)

	if mode == 'test2':
		return hfc.ndhelper1(foods,c)


def merge_nd():
	x = 'https://docs.google.com/spreadsheets/u/1/d/1d8t2PHjkGs2pOcx1aTfWZBCiJtFV-QCScxws_B98-aw/edit#gid=0'
	pass

def save_nd():
	pass

def open_nd():
	pass


x = nutrition_dataframe_beta1( ['milk','broccoli'])

