
import pandas as pd
import numpy as np
import json
import requests
import gc
import pprint
import helper
from helper import HelperFucClass as hfc
import re
from  scipy.optimize import linprog as lp
import ndb
#pd.set_option('display.width', 1000)
#pd.set_option('display.max_columns', 3)




#print (ndb.ndb_search(ndb.apikey,"Broccoli"))


diet_min = pd.read_csv('diet_minimums.csv')
diet_max = pd.read_csv('diet_maximums.csv')


def nutrition_dataframe_beta1(foods = ['milk','broccoli'],c = 'safeway',mode = 'ui', exact_word = True, key = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2',**kwargs  ):

	if mode == 'ndbno':
		df = pd.DataFrame(hfc.getting_nutrition_data_ndbno( foods, **kwargs),columns = ['Food Name','Nutrients','Nutritional value'], dtype = float).set_index(['Nutrients' ]).pivot(columns = 'Food Name')
		
		df.columns  = df.columns.droplevel(level=0)



		return df


	helper.mode = mode
	hfc._exact_word = exact_word

	df = pd.DataFrame(hfc.getting_nutrition_data( foods, c, **kwargs),columns = ['Food Name','Nutrients','Nutritional value']).set_index(['Nutrients' ]).pivot(columns = 'Food Name')
	df.columns  = df.columns.droplevel(level=0)
	df = df.apply(lambda x: [float(i) for i in x])
	#df = pd.DataFrame(hfc.getting_nutrition_data( foods, c, **kwargs),columns = ['Food Name','Nutrients','Nutritional value']).set_index(['Nutrients' ])
	print ( "[" + ", ".join(hfc.oraora) + ']  do/does not exist'  if len(hfc.oraora) != 0 else '')
	gc.collect()
	return df
	"""except:
		print (hfc._ora)
		print ( " ".join(hfc._ora) + 'do/does not exist'  if len(hfc._ora) != 0 else '')
		return"""


def gsheet():
	return pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vQVh0_LyaOHQdxv_iYMqJGgLVZ9qAkH0FTJBiltXTSB86KeanGtIpeghO4S09sSPyAtqlh_mHXJAV9K/pub?output=csv')
	#return requests.get('https://docs.google.com/spreadsheets/u/1/d/1d8t2PHjkGs2pOcx1aTfWZBCiJtFV-QCScxws_B98-aw/edit#gid=0')







def save_nd():
	pass

def open_nd():
	pass

ora = nutrition_dataframe_beta1
sh = gsheet()
lst = sh['Food'][ sh['NDB'] != 'index(' ].tolist()[:34]
ind = [ int(re.sub("index|\(|\)" ,"", i)) for i in sh['NDB'] if i != 'index(']

#print (np.array(lst))
#ora(lst,mode='test2',lst_index = ind)
#x = ora(lst,mode='test2',lst_index = ind)
#x.columns = x.columns.droplevel(level=0)

#print (x)

#print (np.array(x.columns.tolist()))
#print (x['Bananas, raw'])
#y = np.array(x.index,dtype = str)
#print (diet_min['Nutrition'].tolist())


#muda1 = gsheet().set_index('Food').loc[:'PASTA, UPC: 814553000406',:]


