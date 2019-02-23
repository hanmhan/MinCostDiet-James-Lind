import ndb
import pandas as pd
import numpy as np
import json
import requests
import ndb
import pprint
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', 20)


profkey = 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'
mykey = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2'


#print (ndb.ndb_search(ndb.apikey,"Broccoli"))

def search(food, c = 'safeway',maxx = 1500, url = 'https://api.nal.usda.gov/ndb/search?format=json'):

	def helper1(x):
		return x.replace("'", "").replace('"', "").replace(",", "").replace("&", "").replace(" ", "").replace("-","").lower()

	data = requests.get(url , params = (('q', food),('api_key', profkey),('max',maxx)))

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





def nutrition_dataframe_beta1(foods = ['demo1','demo2'],c = 'safeway', url = 'https://api.nal.usda.gov/ndb/V2/reports?format=json', debug = 0):
	tl = []

	if debug == 1:
		d1 = ['45109162', '45361064']
		for i in d1:
			data = requests.get(url , params = (('api_key', 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'),('ndbno',i))).json()['foods'][0]['food']['nutrients']
			nutrition_dataframe_beta1.data = data
			temp2 = np.array([j['value'] for j in  data ])
			tl = tl + [temp2]

		
		testt = [j['name'] for j in data]
		nutrition_dataframe_beta1.testt = testt
		nutrition_dataframe_beta1.tl = tl
		return pd.DataFrame(data = np.array(tl) , index = foods, columns= testt)

	if len(foods) > 1:
		for i in foods:
			temp1 = search(i,c)

			for q in temp1:
				data = requests.get(url , params = (('api_key', 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'),('ndbno',q['ndbno']))).json()['foods'][0]['food']['nutrients']

			#iter1 = ( j['value'] for j in  data )
			#temp2 = np.fromiter(iter1,float)

			temp2 = np.array([j['value'] for j in  data ])
			

			tl = tl + [temp2]


	testt = [j['name'] for j in data]


	return pd.DataFrame(data = np.array(tl) , index = foods, columns= testt)


#print (search("Broccoli",'Baby Foods'))
#x = search("Broccoli",c = 'safeway')

