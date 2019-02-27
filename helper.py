
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
	api_key = profkey
	nd_url = 'https://api.nal.usda.gov/ndb/V2/reports?format=json&type=b'
	mode = 'ui'
	_ora = []
	_exact_word = 0
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


	def ndhelper1(foods,c='all'):
		
		def data_recursive_helper(foods_nd_lst):
			if foods_nd_lst:
				return []

			return [ [foods_nd_lst[0]['food']['desc']['name'],i['name'] , i['value']] for i in  foods_nd_lst[0]['food']['nutrients']]  + data_recursive_helper(foods_nd_lst[1:])
		"""def average of duplicates(x,a):

			pd.Series(x).groupby(a).agg(lambda y : sum(y)/len(y))
			return  """

		if foods:

			return []

		try:
			data1 = classificationforfoods.search_user(foods[0],c) if HelperFucClass.mode == 'ui' else classificationforfoods.search_insider(foods[0]) if HelperFucClass.mode == 'test' else None
			data1 = requests.get(HelperFucClass.nd_url , params = tuple(( ('ndbno',i['ndbno']) for i in data1)) + (('api_key', HelperFucClass.api_key),)    ).json()
		
		except:
			HelperFucClass._ora += [foods[0]]
			return HelperFucClass.ndhelper1(foods[1:],c)
		 


		return data_recursive_helper(data1['foods']) + HelperFucClass.ndhelper1(foods[1:],c)



class classificationforfoods:

	def search_user(food, c = 'safeway',maxx = 1500, url = 'https://api.nal.usda.gov/ndb/search?format=json'):
		qwertyui = "UPC [0-9]+"
		punct_re = r'[^\w ]|  +'
		food = re.sub(punct_re," ",food.lower())
		fil_re =  '|'.join(food.split()) if len(food.split()) > 1 else food.lower()
		print(fil_re)
		data = requests.get(url , params = (('q', food),('api_key', HelperFucClass.api_key),('max',maxx)))

		tempx =  np.array([i for i in data.json()['list']['item'] if re.findall(fil_re, re.sub(punct_re ," ",i['name'].lower()) ) ]) if HelperFucClass._exact_word  else np.array([i for i in data.json()['list']['item'] if len( re.sub(punct_re ," ",i['name'].lower())) == len(fil_re.split('|')) ])

		#tempx =  np.array([i for i in data.json()['list']['item']])



		#temp2 = [   (' '.join(i['name'].split()[:[k for j,k in zip(i['name'].split(), range(len(i['name'].split()))) if 'UPC' in j][0]])) for i in tempx]
		pprint.pprint([ str(j) + ': '+i['name'] for i,j in zip(tempx,range(len(tempx)))][:20])
		print ('========================================================================')
		print ('please input the products you want following the next line ')
		print ('For instance:')
		#print ('1. x1')
		#print ('2. x1/x2/x3')
		print ('3. index(0,1,2,3)')
		print ('4. esc')
		_input = input('>>>>> ')
		if 'index' in _input:
			temp3 = [int(i) for i in _input.replace('index',"").replace('(',"").replace(')','').split(',')]
	
			return [i for i,j in zip(tempx,range(len(tempx))) if j in temp3 ]


		elif '/' in _input:
			temp3 = np.array([ HelperFucClass._helper1(i) for i in  _input.replace("'", "").replace('"', "").split("/")])
	

			return tempx[[True if HelperFucClass._helper1(i) in temp3 else False for i in temp2]]
		elif 'esc' == _input:
			return None
		else:
			return [ i for i in tempx if _input.lower() in i['name'].lower()][0]
		return list(tempx)



	def search_insider(food, c = 'safeway',maxx = 1500, url = 'https://api.nal.usda.gov/ndb/search?format=json'):


		punct_re = r'[^\w ]'
		temp_raw = 'raw ' + re.sub(punct_re," ",food)
		#abcd = re.sub(punct_re," ",'Broccoli raab, raw'.lower())
		#print (len(abcd.split()))

		if not cache_ndb._boolean_exist('ndbno','raw ' + food, index = True):

			

			data2 = requests.get(url , params = (('q', temp_raw),('api_key', HelperFucClass.api_key),('max',maxx), ('ds','Standard Reference'))).json()['list']['item']
			data1 = requests.get(url , params = (('q', temp_raw),('api_key', HelperFucClass.api_key),('max',maxx))).json()['list']['item']

			cache_ndb._update('ndbno', {temp_raw.lower(): data1}, index = 0)
			cache_ndb._update('ndbno', {temp_raw.lower(): data2}, index = 1)



		else:

			data1 = cache_ndb._caches['ndbno'][0][temp_raw.lower()]
			data2 = cache_ndb._caches['ndbno'][1][temp_raw.lower()]
	

		#temp_list = [i if len(re.findall( 'raw|'+food.lower(),re.sub(punct_re," ",i['name'].lower()) )) == len(temp_raw.split()) and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split())  else None if not len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split()) + 2 or not 'UPC' in i['name'] else i for i in data1]
		#temp_list = [i for i in temp_list if i != None] 
		temp_list = None
		temp_list2 =  [i for i in data2 if len(re.findall( 'raw|'+food.lower(),re.sub(punct_re," ",i['name'].lower()) )) == len(temp_raw.split()) and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split())]

		

		if temp_list or temp_list2:

			return temp_list2 if temp_list2 else temp_list


		print ('Errorrrrrrrrrrrrrrrrrrrrrrrrr')
		"""else:
		
			if not cache_ndb._boolean_exist('ndbno',food):

				data = requests.get(url , params = (('q', food),('api_key', HelperFucClass.mykey),('max',maxx))).json()['list']['item']
				cache_ndb._update('ndbno', {food.lower(): [i for i in data]})

			else:

				data = cache_ndb._caches['ndbno'][food]

			return [1,2]"""

class cache_ndb:

	if os.path.isfile('caches.json'):

		with open('caches.json') as file:
			_caches = json.load(file)

	else:
		_caches = {'ndbno':[{},{}], 'nd':{}}
		print (_caches['ndbno'][0] )
		print (_caches['ndbno'][1] )
		with open('caches.json','w') as file:
			json.dump(_caches,file)

	def _update(type, dict_x, index = None):
		if index == None:
			cache_ndb._caches[type].update(dict_x)
		else:
			cache_ndb._caches[type][index].update(dict_x)

		with open('caches.json','w') as file:
			json.dump(cache_ndb._caches,file)


	def _boolean_exist(type,food, index = None):
		
		return food.lower() in cache_ndb._caches[type] if index == None else food.lower() in cache_ndb._caches[type][0] or food.lower() in cache_ndb._caches[type][1]


#print (classificationforfoods.search_insider('broccoli',c='safeway'))

#print (HelperFucClass.ndhelper1(['broccoli'],c='safeway'))
