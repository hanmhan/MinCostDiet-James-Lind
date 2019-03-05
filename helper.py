
import pandas as pd
import numpy as np
import json
import requests
import re
import pprint
import os


mode = 'm'

def foods_spreadsheet(local = None, spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVh0_LyaOHQdxv_iYMqJGgLVZ9qAkH0FTJBiltXTSB86KeanGtIpeghO4S09sSPyAtqlh_mHXJAV9K/pub?output=csv'):


	return pd.read_csv(spreadsheet_url)
	


class search:

	punct_re = r"[^\w ]|  +"
	se_url = 'https://api.nal.usda.gov/ndb/search?format=json&sort=n'
	maxx = 1500

	def __init__(self):
		pass


	def FoodNDB(self):

		if mode == 'm':

			return self.search_user



		elif mode == 'index':

			return self.search_test



	def search_user(self, food):

		def display_results(x, switch = 0):


			if switch == 0:

				pprint.pprint([ str(j) + ': '+i['name'] for i,j in zip(x,range(len(x)))][:20])

			if switch == 0 or switch == 1:
				print ('========================================================================')
				print ('please input the products you want following the next line ')
				print ('For instance:')
				print ('1. index(0,1,2,3)')
				print ('2. more')
				print ('3. cancel')

			_input = input('>>>>> ')

			if _input == 'more' and len(x) > 0:

				return display_results(x[20:], switch = 1)

			elif _input == 'cancel':
				raise Exception("It's canceled")

			elif re.search('^index\\((?:[0-9 ]+,?)*[0-9]\\)$', _input):

				return [   i.split(',') for i in re.sub('index|\(|\)| +','',_input)]

			else:
				print ("unknown inputs, please try it again")
				return display_results(x[20:], switch = 2)


		fil_re = "UPC[^0-9a-zA-Z]+[0-9]+"
		punct_re = r'[^\w ]|  +'

		food = re.sub(punct_re," ",food.lower())
		food_re =  '|'.join(food.split()) if len(food.split()) > 1 else food.lower()
		if not cache_ndb._boolean_exist('ndbno',food, index = True):

			data = np.array(requests.get(self.se_url , params = (('q', food),('api_key', self.api_key),('max',self.maxx))).json()['list']['item'])
			cache_ndb._update('ndbno', {food: list(data)}, index = 0)
		else:
			data = np.array(cache_ndb._caches['ndbno'][0][food])


		data = data[sorting_result(food,data)]

		return display_results(data)



	def index_searching(self,food,lst_index=[]):


		punct_re = r"[^\w ]|  +"
		food = re.sub(punct_re," ",food.lower())
		food_re =  '|'.join(food.split()) if len(food.split()) > 1 else food.lower()

		if not cache_ndb._boolean_exist('ndbno',food, index = True):

			data = requests.get(self.se_url , params = (('q', food),('api_key', self.api_key),('max',self.maxx))).json()['list']['item']

			cache_ndb._update('ndbno', {food: data}, index = 0)

		else:

			data = cache_ndb._caches['ndbno'][0][food]



		tempx =  np.array([i for i in data if re.findall(food_re, re.sub(punct_re ," ",i['name'].lower()) ) ]) if self._exact_word else np.array([i for i in data.json()['list']['item'] if len( re.sub(punct_re ," ",i['name'].lower())) == len(food_re.split('|')) ])

		qwe = [i for i,j in zip(tempx,range(len(tempx))) if  j == lst_index[0] ]
		
		return qwe



class NutritionDataLibrary(search):

	profkey = 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'
	mykey = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2'
	mykey2 = 'qKtE5wujwySVB2sCbwQEpNkCt3r3i2BrIU23F6TL'
	api_key = mykey2
	nd_url = 'https://api.nal.usda.gov/ndb/V2/reports?format=json&type=b'
	mode = 'm'
	oraora = []
	_exact_word = 0
	ndbno = None

	def _helper1(x):
		return x.replace("'", "").replace('"', "").replace(",", "").replace("&", "").replace(" ", "").replace("-","").lower()


	def nutrition_dataframe(self, foods = None, **kwargs  ):

		if self.mode == 'ndbno':
			df = pd.DataFrame(self._retrieving_nutrition_data(self, foods, **kwargs),columns = ['Food Name','Nutrients','Nutritional value'], dtype = float).set_index(['Nutrients' ]).pivot(columns = 'Food Name')
			
			df.columns  = df.columns.droplevel(level=0)


		else:
			df = pd.DataFrame(self._retrieving_nutrition_data( foods,  **kwargs),columns = ['Food Name','Nutrients','Nutritional value'],dtype = float).set_index(['Nutrients' ]).pivot(columns = 'Food Name')
			df.columns  = df.columns.droplevel(level=0)
			print ( "[" + ", ".join(self.oraora) + ']  do/does not exist'  if len(self.oraora) != 0 else '')


		gc.collect()
		return df



	def _retrieving_nutrition_data(self, foods,**kwargs):
		
		def recursive_helper(foods_nd_lst):

			if len(foods_nd_lst) == 0:
				return []

			return [ [foods[0],i['name'] , i['value']] for i in  foods_nd_lst[0]['food']['nutrients']]  + recursive_helper(foods_nd_lst[1:])



		if len(foods) == 0:
			return []



		try:

			data1 = self.FoodNDB()( foods[0],**kwargs )


			if not cache_ndb._boolean_exist('nd',foods[0]):

				data1 = requests.get(self.nd_url , params = tuple(( ('ndbno',i['ndbno']) for i in data1)) + (('api_key', self.api_key),)    ).json()

				cache_ndb._update('nd', {foods[0]: data1})

			else:

				data1 = cache_ndb._caches['nd'][foods[0]]

					

			if 'lst_index' in kwargs:
				
				kwargs.update({ 'lst_index' :kwargs[1:] })

			return recursive_helper(data1['foods']) + self._retrieving_nutrition_data(foods[1:],c , **kwargs)


		except KeyError:

			self.oraora += [foods[0]]
			return self._retrieving_nutrition_data(self,foods[1:],c ,**kwargs)


	def _retrieving_nutrition_data_ndbno(self,foods,ndbno=None,**kwargs):

		def recursive_helper(foods_nd_lst):

			if len(foods_nd_lst) == 0:
				return []


			return [ [foods[0],i['name'] , i['value']] for i in  foods_nd_lst[0]['food']['nutrients']]  + recursive_helper(foods_nd_lst[1:])


		if ndbno == None:
			ndbno = self.ndbno.copy()

		if len(foods) == 0:
			return []

		data1 = requests.get(self.nd_url , params = (('api_key', self.api_key), ('ndbno',ndbno[0])) ).json()
		return recursive_helper(data1['foods']) + self._retrieving_nutrition_data_ndbno(foods[1:],ndbno[1:])




	def min_cost():
		pass


class FoodLibrary(NutritionDataLibrary):




	def __init__(self, foods = None, **kwargs):

		for i in kwargs:
			self.i = kwargs[i]

		self.foods = foods
		self.foods_spreadsheet = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVh0_LyaOHQdxv_iYMqJGgLVZ9qAkH0FTJBiltXTSB86KeanGtIpeghO4S09sSPyAtqlh_mHXJAV9K/pub?output=csv'

	def change_foods_spreadsheet(spreadsheet_local_url = None):

		self.foods_spreadsheet = spreadsheet_local_url if spreadsheet_local_url != None else  self.foods_spreadsheet

		print (self.foods_spreadsheet)

	def processing_kwargs(**kwargs):
		for i in kwargs:
			self.i = kwargs[i]


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




def sorting_result(foodname, x):
	regx = "(?:UPC[^0-9a-zA-Z]*[0-9]+)|(?:[^\w ]|  +)|(?:[0-9]+)"
	foodname1 = re.sub(regx,"",foodname.lower()).split()
	foodname1 = "|" + "|".join(foodname1) + "| "

	temp1 = np.array([ (j,re.sub(regx ,"",i['name'].lower() ), len(re.sub(regx+foodname1,"", i['name'])) ) for i,j in zip(x,range(len(x)))], dtype=[('index', int),('name','U70') ,('leng', int)])
	temp1.sort(order='leng',kind='mergesort')

	temp1 = np.append(temp1[np.char.find(temp1['name'], foodname) != -1], temp1[np.char.find(temp1['name'], foodname) == -1])



	#print (temp1[np.char.find(temp1['name'], foodname) == -1][:30])
	#print (temp1)
	#temp1 = temp1[np.argsort(np.char.find(temp1['name'], foodname) * -1)]


	return temp1['index']

abcd = [{'name':'test'},{'name':'testtest'},{'name':'tesst'},{'name':'asdaf'},{'name':'testhgdsfgdasdst'},{'name':'tesqweqwt'},{'name':'testqwt'}   ]
#print (sorting_result('test',abcd ))

