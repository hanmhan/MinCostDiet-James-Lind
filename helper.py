
import pandas as pd
import numpy as np
import json
import requests
import re
import pprint
import os
class HelperFucClass:

	profkey = 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'
	mykey = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2'



	def _helper1(x):
		return x.replace("'", "").replace('"', "").replace(",", "").replace("&", "").replace(" ", "").replace("-","").lower()

	def debug1(x):
		tl = {}
		col = {}

		for i in x:

			with open(i,'r') as file:
				data = json.load(file)

			tl[i] = {}
			for j in data:
				if j['name'] not in col:
					col[j['name']] = 0
				tl[i][j['name']] = j['value']

		for i in col:


			col[i] = [tl[j][i] if i in tl[j] else None for j in tl]


		return col


	def ndhelper1(x,c,key = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2', url = 'https://api.nal.usda.gov/ndb/V2/reports?format=json', mode = 'ui'):
		tl = {}
		col = {}
		if mode == 'ui':
			for i in x:
				temp1 = classificationforfoods.search_user(i,c) 
				for q in temp1:
				
					data = requests.get(url , params = (('api_key', HelperFucClass.mykey),('ndbno',q['ndbno']))).json()['foods'][0]['food']['nutrients']


				tl[i] = {}
				for j in data:
					if j['name'] not in col:
						col[j['name']] = 0
					tl[i][j['name']] = j['value']

			for i in col:


				col[i] = [tl[j][i] if i in tl[j] else None for j in tl]


			return col


		if mode == 'test':
			for i in x:
				temp1 = classificationforfoods.search_insider(i)
				for q in temp1:
				
					data = requests.get(url , params = (('api_key', HelperFucClass.mykey),('ndbno',q['ndbno']))).json()['foods'][0]['food']['nutrients']
				tl[i] = {}
				for j in data:
					if j['name'] not in col:
						col[j['name']] = 0
					tl[i][j['name']] = j['value']

			for i in col:


				col[i] = [tl[j][i] if i in tl[j] else None for j in tl]


			return col
		if mode == 'test2':
			return classificationforfoods.search_insider(x[0])

class classificationforfoods:

	def search_user(food, c = 'safeway',maxx = 1500, url = 'https://api.nal.usda.gov/ndb/search?format=json'):

		data = requests.get(url , params = (('q', food),('api_key', HelperFucClass.profkey),('max',maxx)))

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
				temp3 = np.array([ HelperFucClass._helper1(i) for i in  _input.replace("'", "").replace('"', "").split("/")])
	

				return tempx[[True if HelperFucClass._helper1(i) in temp3 else False for i in temp2]]
			elif 'index' in _input:
				temp3 = [int(i) for i in _input.replace('index',"").replace('(',"").replace(')','').split(',')]
	
				return [i for i,j in zip(tempx,range(len(tempx))) if j in temp3 ]
				 
			else:
				return [ i for i in tempx if _input.lower() in i['name'].lower()][0]

		return list(tempx)



	def search_insider(food, c = 'safeway',maxx = 1500, url = 'https://api.nal.usda.gov/ndb/search?format=json'):
		cache_ndb
		temp_raw = 'raw ' + food
		punct_re = r'[^\w \n]'

		if not cache_ndb._boolean_exist('ndbno','raw ' + food):

			

			data2 = requests.get(url , params = (('q', temp_raw),('api_key', HelperFucClass.mykey),('max',maxx), ('ds','Standard Reference'))).json()['list']['item']
			data = requests.get(url , params = (('q', temp_raw),('api_key', HelperFucClass.mykey),('max',maxx))).json()['list']['item']
			cache_ndb._update('ndbno', {temp_raw.lower(): [i for i in data]})
			print (1)

		else:

			data = cache_ndb._caches['ndbno'][temp_raw]
			data2 = cache_ndb._caches['ndbno'][temp_raw]
			print (2)


		temp_list =  [i for i in data if len(re.findall( '^raw|'+food,re.sub(punct_re," ",i['name'].lower()) )) == 2 and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split()) + 2]
		temp_list2 =  [i for i in data2 if len(re.findall( '^raw|'+food,re.sub(punct_re," ",i['name'].lower()) )) == 2 and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split()) + 2]

		if temp_list or temp_list2:
			print (temp_list)
			return temp_list if temp_list else temp_list2

		else:
		
			if not cache_ndb._boolean_exist('ndbno',food):

				data = requests.get(url , params = (('q', food),('api_key', HelperFucClass.mykey),('max',maxx))).json()['list']['item']
				cache_ndb._update('ndbno', {food.lower(): [i for i in data]})

			else:

				data = cache_ndb._caches['ndbno'][food]

			return [1,2]

class cache_ndb:

	if os.path.isfile('caches.json'):

		with open('caches.json') as file:
			_caches = json.load(file)

	else:
		_caches = {'ndbno':{}, 'nd':{}}
		with open('caches.json','w') as file:
			json.dump(_caches,file)

	def _update(type, dict_x):
		cache_ndb._caches[type].update(dict_x)
		with open('caches.json','w') as file:
			json.dump(cache_ndb._caches,file)


	def _boolean_exist(type,food):

		return food.lower() in cache_ndb._caches[type]


