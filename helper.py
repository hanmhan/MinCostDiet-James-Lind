
import pandas as pd
import numpy as np
import json
import requests
import re
import pprint
import os


GodMode = False
ind = None


mode = 'ui'

class HelperFucClass:

	profkey = 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'
	mykey = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2'
	mykey2 = 'qKtE5wujwySVB2sCbwQEpNkCt3r3i2BrIU23F6TL'
	api_key = mykey2


	nd_url = 'https://api.nal.usda.gov/ndb/V2/reports?format=json&type=b'

	oraora = []
	_exact_word = 0
	def _helper1(x):
		return x.replace("'", "").replace('"', "").replace(",", "").replace("&", "").replace(" ", "").replace("-","").lower()

	def getting_nutrition_data(foods,c=None,**kwargs):
		
		def recursive_helper(foods_nd_lst):

			if len(foods_nd_lst) == 0:
				return []


			return [ [foods[0],i['name'] , i['value']] for i in  foods_nd_lst[0]['food']['nutrients']]  + recursive_helper(foods_nd_lst[1:])
		"""def average of duplicates(x,a):

			pd.Series(x).groupby(a).agg(lambda y : sum(y)/len(y))
			return  """




		if len(foods) == 0:

			return []



		try:
			data1 = search.FoodNDB()(foods[0],c,**kwargs )

			if not cache_ndb._boolean_exist('nd',foods[0]):


				data1 = requests.get(HelperFucClass.nd_url , params = tuple(( ('ndbno',i['ndbno']) for i in data1)) + (('api_key', HelperFucClass.api_key),)    ).json()

				cache_ndb._update('nd', {foods[0]: data1})

			else:

				data1 = cache_ndb._caches['nd'][foods[0]]

					



			if kwargs:
				
				kwargs = { i:kwargs[i][1:]  for i in kwargs}

			return recursive_helper(data1['foods']) + HelperFucClass.getting_nutrition_data(foods[1:],c , **kwargs)


		except KeyError:

			HelperFucClass.oraora += [foods[0]]
			return HelperFucClass.getting_nutrition_data(foods[1:],c ,**kwargs)


	def getting_nutrition_data_ndbno(foods,ndbno=[]):
		def recursive_helper(foods_nd_lst):

			if len(foods_nd_lst) == 0:
				return []


			return [ [foods[0],i['name'] , i['value']] for i in  foods_nd_lst[0]['food']['nutrients']]  + recursive_helper(foods_nd_lst[1:])
		if len(foods) == 0:

			return []
		data1 = requests.get(HelperFucClass.nd_url , params = (('api_key', HelperFucClass.api_key), ('ndbno',ndbno[0]))    ).json()
		return recursive_helper(data1['foods']) + HelperFucClass.getting_nutrition_data_ndbno(foods[1:],ndbno[1:])
class search:
	nd_url = 'https://api.nal.usda.gov/ndb/search?format=json'
	maxx = 1500

	def __init__(self):
		pass


	def FoodNDB():

		if mode == 'ui':

			return search.search_user

		elif mode == 'test':

			return search.search_insider

		elif mode == 'test2':

			return search.search_test



	def search_user(food, c = 'safeway'):

		qwertyui = "UPC [0-9]+"
		punct_re = r'[^\w ]|  +'
		food = re.sub(punct_re," ",food.lower())
		fil_re =  '|'.join(food.split()) if len(food.split()) > 1 else food.lower()

		data = requests.get(search.nd_url , params = (('q', food),('api_key', HelperFucClass.api_key),('max',search.maxx)))

		tempx =  np.array([i for i in data.json()['list']['item'] if re.findall(fil_re, re.sub(punct_re ," ",i['name'].lower()) ) ]) if HelperFucClass._exact_word else np.array([i for i in data.json()['list']['item'] if len( re.sub(punct_re ," ",i['name'].lower())) == len(fil_re.split('|')) ])
	
		#print (len(tempx))
		#print (tempx)
		if GodMode == True:
			print (ind[0])
			qwe = [i for i,j in zip(tempx,range(len(tempx))) if  j == ind[0] ]

			ind.remove(ind[0])


			return qwe

		#temp2 = [   (' '.join(i['name'].split()[:[k for j,k in zip(i['name'].split(), range(len(i['name'].split()))) if 'UPC' in j][0]])) for i in tempx]
		pprint.pprint([ str(j) + ': '+i['name'] for i,j in zip(tempx,range(len(tempx)))][:300])
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



	def search_insider(food, c = 'safeway'):


		punct_re = r'[^\w ]'
		temp_raw = 'raw ' + re.sub(punct_re," ",food)
		#abcd = re.sub(punct_re," ",'Broccoli raab, raw'.lower())
		#print (len(abcd.split()))

		if not cache_ndb._boolean_exist('ndbno','raw ' + food, index = True):

			

			data2 = requests.get(search.nd_url , params = (('q', temp_raw),('api_key', HelperFucClass.api_key),('max',search.maxx), ('ds','Standard Reference'))).json()['list']['item']
			data1 = requests.get(search.nd_url , params = (('q', temp_raw),('api_key', HelperFucClass.api_key),('max',search.maxx))).json()['list']['item']

			cache_ndb._update('ndbno', {temp_raw.lower(): data1}, index = 0)
			cache_ndb._update('ndbno', {temp_raw.lower(): data2}, index = 1)



		else:

			data1 = cache_ndb._caches['ndbno'][0][temp_raw.lower()]
			data2 = cache_ndb._caches['ndbno'][1][temp_raw.lower()]
	
		if HelperFucClass._exact_word:
			temp_list2 =  [i for i in data2 if len(re.findall( 'raw|'+food.lower(),re.sub(punct_re," ",i['name'].lower()) )) == len(temp_raw.split()) and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split())]
			temp_list = None

	
		else:
			temp_list = [i if len(re.findall( 'raw|'+food.lower(),re.sub(punct_re," ",i['name'].lower()) )) == len(temp_raw.split()) and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split())  else None if not len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split()) + 2 or not 'UPC' in i['name'] else i for i in data1]
			temp_list = [i for i in temp_list if i != None] 

			#temp_list = None
			temp_list2 =  [i for i in data2 if len(re.findall( 'raw|'+food.lower(),re.sub(punct_re," ",i['name'].lower()) )) == len(temp_raw.split()) and len(re.sub(punct_re," ",i['name'].lower()).split()) == len(temp_raw.split())]

		

		if temp_list or temp_list2:
	
			return temp_list2 if temp_list2 else temp_list


		print ('Errorrrrrrrrrrrrrrrrrrrrrrrrr')
		"""else:
		
			if not cache_ndb._boolean_exist('ndbno',food):

				data = requests.get(search.nd_url , params = (('q', food),('api_key', HelperFucClass.mykey),('max',search.maxx))).json()['list']['item']
				cache_ndb._update('ndbno', {food.lower(): [i for i in data]})

			else:

				data = cache_ndb._caches['ndbno'][food]

			return [1,2]"""


	def search_test(food,c = 'safeway',lst_index=[]):

		qwertyui = "UPC [0-9]+"
		punct_re = r'[^\w ]|  +'
		food = re.sub(punct_re," ",food.lower())
		fil_re =  '|'.join(food.split()) if len(food.split()) > 1 else food.lower()

		if not cache_ndb._boolean_exist('ndbno',food, index = True):


			

			data = requests.get(search.nd_url , params = (('q', food),('api_key', HelperFucClass.api_key),('max',search.maxx))).json()['list']['item']

			cache_ndb._update('ndbno', {food: data}, index = 0)




		else:

			data = cache_ndb._caches['ndbno'][0][food]



		tempx =  np.array([i for i in data if re.findall(fil_re, re.sub(punct_re ," ",i['name'].lower()) ) ]) if HelperFucClass._exact_word else np.array([i for i in data.json()['list']['item'] if len( re.sub(punct_re ," ",i['name'].lower())) == len(fil_re.split('|')) ])

		qwe = [i for i,j in zip(tempx,range(len(tempx))) if  j == lst_index[0] ]
		
		return qwe



class cache_ndb:

	if os.path.isfile('caches.json'):

		with open('caches.json') as file:
			_caches = json.load(file)

	else:
		_caches = {'ndbno':[{},{}], 'nd':{}}

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

		return food in cache_ndb._caches[type] if index == None else food.lower() in cache_ndb._caches[type][0] or food.lower() in cache_ndb._caches[type][1]






