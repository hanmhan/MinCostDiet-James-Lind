
import pandas as pd
import numpy as np
import json
import requests

import pprint

from helper import HelperFucClass as hfc
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 20)




#print (ndb.ndb_search(ndb.apikey,"Broccoli"))




def search(food, c = 'safeway',maxx = 1500, url = 'https://api.nal.usda.gov/ndb/search?format=json', mode = 'ui'):

	def helper1(x):
		return x.replace("'", "").replace('"', "").replace(",", "").replace("&", "").replace(" ", "").replace("-","").lower()

	data = requests.get(url , params = (('q', food),('api_key', hfc.profkey),('max',maxx)))

	tempx =  np.array([i for i in data.json()['list']['item'] if c.lower() in i['manu'].lower()])


	if len(tempx) != 1:


		temp2 = [   (' '.join(i['name'].split()[:[k for j,k in zip(i['name'].split(), range(len(i['name'].split()))) if 'UPC' in j][0]])) for i in tempx]
		pprint.pprint(temp2)
		print ('========================================================================')
		print ('please input the products you want following the next line ')
		print ('For instance:')
		print ('1. x1')
		print ('2. x1/x2/x3')
		print ('3. index(0,1,2,3)')
		_input = input('>>>>> ')
		if '/' in _input:
			temp3 = np.array([ helper1(i) for i in  _input.replace("'", "").replace('"', "").split("/")])


			return tempx[[True if helper1(i) in temp3 else False for i in temp2]]
		elif 'index' in _input:
			temp3 = [int(i) for i in _input.replace('index',"").replace('(',"").replace(')','').split(',')]

			return [i for i,j in zip(tempx,range(len(tempx))) if j in temp3 ]
			 
		else:
			return [ i for i in tempx if _input.lower() in i['name'].lower()][0]

	return list(tempx)





def nutrition_dataframe_beta1(foods = ['demo1','demo2'],c = 'safeway', debug = 0, mode = 'ui'):
	tl = []
	col = []

	if debug == 1:
		d1 = ['45109162', '45361064']
		d2 = ['test.json','test2.json']
		df = pd.DataFrame(hfc.debug1(d2))
		return df


	if mode == 'ui':
		if len(foods) > 1:
			df = pd.DataFrame(hfc.ndhelper1( foods, c))
			return df