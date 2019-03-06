
import pandas as pd
import numpy as np
import json
import requests
import re
import pprint
import os
import ndb
from  scipy.optimize import linprog as lp

mode = 'm'

def foods_spreadsheet(local = None, spreadsheet_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVh0_LyaOHQdxv_iYMqJGgLVZ9qAkH0FTJBiltXTSB86KeanGtIpeghO4S09sSPyAtqlh_mHXJAV9K/pub?gid=410630770&single=true&output=csv'):


	return pd.read_csv(spreadsheet_url)
	


class search:

	punct_re = r"[^\w ]|  +"
	se_url = 'https://api.nal.usda.gov/ndb/search?format=json&sort=n'
	maxx = 1500

	def __init__(self):
		pass


	def FoodNDB(self):

		if self.mode == 'm':

			return self.search_user



		elif self.mode == 'index':

			return self.index_searching



	def search_user(self, food,**kwargs):

		def display_results(x, scope =[0,20] ,switch = 0):
			print (len(x))

			if switch == 0:

				pprint.pprint([ str(j) + ': '+i['name'] for i,j in zip(x[:20],range(scope[0],scope[1]))])

			if switch == 0 or switch == 1:
				print ('========================================================================')
				print ('please input the products you want following the next line ')
				print ('For instance:')
				print ('1. index(0,1,2,3)')
				print ('2. more')
				print ('3. cancel')

			_input = input('>>>>> ')

			if _input == 'more' and len(x) > 0:

				return display_results(x[20:],[scope[1] , scope[1] + 20] ,switch = 0)

			elif _input == 'cancel':
				raise Exception("It's canceled")

			elif re.search('^index\\((?:[0-9 ]+,?)*[0-9]\\)$', _input):

				print (re.sub('index|\(|\)| +','',_input).split())

				return np.array(re.sub('index|\(|\)| +','',_input).split())

			else:
				print ("unknown inputs, please try it again")
				return display_results(x[20:], [scope[0],scope[1]],switch = 2)


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

		temp1 = display_results(data)

		data = [ data[int(i)] for i in temp1]

		del temp1

		return data



	def index_searching(self,food,lst_index=[],**kwargs):


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
		qwe = [i for i,j in zip(data,range(len(data))) if  j == lst_index[0] ]
		
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
	ndbno = []

	def _helper1(x):
		return x.replace("'", "").replace('"', "").replace(",", "").replace("&", "").replace(" ", "").replace("-","").lower()


	def nutrition_dataframe(self, foods = None, **kwargs  ):
		print(self.mode)
		if 'mode' in kwargs:

			self.mode = kwargs['mode']
			print(self.mode)


		if self.mode == 'ndbno':
			df = pd.DataFrame(self._retrieving_nutrition_data(self, foods, **kwargs),columns = ['Food Name','Nutrients','Nutritional value'], dtype = float).set_index(['Nutrients' ]).pivot(columns = 'Food Name')
			
			df.columns  = df.columns.droplevel(level=0)


		else:
			df = pd.DataFrame(self._retrieving_nutrition_data( foods,  **kwargs),columns = ['Food Name','Nutrients','Nutritional value'],dtype = float).set_index(['Nutrients' ]).pivot(columns = 'Food Name')
			df.columns  = df.columns.droplevel(level=0)
			print ( "[" + ", ".join(self.oraora) + ']  do/does not exist'  if len(self.oraora) != 0 else '')



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
			self.ndbno += [ i['ndbno'] for i in data1]

			if not cache_ndb._boolean_exist('nd',foods[0]):

				data1 = requests.get(self.nd_url , params = tuple(( ('ndbno',i['ndbno']) for i in data1)) + (('api_key', self.api_key),)    ).json()

				cache_ndb._update('nd', {foods[0]: data1})

			else:

				data1 = cache_ndb._caches['nd'][foods[0]]

					

			if 'lst_index' in kwargs:
				
				kwargs.update({ 'lst_index' :kwargs['lst_index'][1:] })


			

			return recursive_helper(data1['foods']) + self._retrieving_nutrition_data(foods[1:] , **kwargs)


		except KeyError:

			self.oraora += [foods[0]]
			return self._retrieving_nutrition_data(self,foods[1:] ,**kwargs)


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




class FoodLibrary(NutritionDataLibrary):




	def __init__(self, foods = None, **kwargs):

		for i in kwargs:
			self.i = kwargs[i]

		self.foods = foods
		self.foods_spreadsheet = 'p2s.csv'

	def change_foods_spreadsheet(spreadsheet_local_url = None):

		self.foods_spreadsheet = spreadsheet_local_url if spreadsheet_local_url != None else  self.foods_spreadsheet

		print (self.foods_spreadsheet)

	def processing_kwargs(**kwargs):
		for i in kwargs:
			self.i = kwargs[i]


	def min_cost(self):
		group = "F 19-30"
		diet_min = pd.read_csv('diet_minimums.csv')
		diet_max = pd.read_csv('diet_maximums.csv')
		bmin = pd.read_csv('./diet_minimums.csv').set_index('Nutrition')[group]
		bmax = pd.read_csv('./diet_maximums.csv').set_index('Nutrition')[group]
		def test1(ndf):

			ndf['Quantity'] = [float(i)for i in ndf['Quantity']]

			ndf['Price'] = [float(i[1:])for i in ndf['Price']]

			ndf['NDB Quantity'] = ndf[['Quantity','Units']].T.apply(lambda x : ndb.ndb_units(x['Quantity'],x['Units']))

			ndf['NDB Price'] = ndf['Price']/ndf['NDB Quantity']

			return ndf

		muda1 = pd.read_csv(self.foods_spreadsheet).iloc[:20,:]
		muda2 = test1(muda1)
		df = muda2
		print (df[['NDB Quantity','NDB Price']])


		D = self.nutrition_dataframe( list(df['Food']) ,mode='index',lst_index = [ int(re.findall('[0-9]+',i)[0]) for i in df['NDB']])


		df.dropna(how='any') 
		Prices = muda2.groupby('Food')['NDB Price'].min()


		#print (Prices)
		tol = 1e-6 # Numbers in solution smaller than this (in absolute value) treated as zeros

		c = Prices.apply(lambda x:x.magnitude).dropna()

		# Compile list that we have both prices and nutritional info for; drop if either missing
		# Drop nutritional information for foods we don't know the price of,
		# and replace missing nutrients with zeros.
		Aall = D[c.index].fillna(0)


		# Drop rows of A that we don't have constraints for.
		Amin = Aall.loc[bmin.index]
		Amax = Aall.loc[bmax.index]

		# Minimum requirements involve multiplying constraint by -1 to make <=.
		A = pd.concat([-Amin,Amax])
		b = pd.concat([-bmin,bmax]) # Note sign change for min constraints


		# Now solve problem!
		result = lp(c, A, b, method='simplex',options = {"presolve":False,'maxiter':5000.0})
		#result = lp(c, A_ub= -A, b_ub = -b, method='simplex',options = {"presolve":False,'maxiter':5000.0})
		#result.x = result.x.astype(np.int64)
		print (len([int(i) for i in result.x]))
		print ('==============================')
		print (result.message)
		print ('==============================')
		# Put back into nice series
		diet = pd.Series(result.x,index=c.index)




		print("Cost of diet for %s is $%4.2f per day." % (group,result.fun))
		print("\nYou'll be eating (in 100s of grams or milliliters):")
		print(diet[diet >= tol])  # Drop items with quantities less than precision of calculation

		tab = pd.DataFrame({"Outcome":np.abs(A).dot(diet),"Recommendation":np.abs(b)})

		print("\nWith the following nutritional outcomes of interest:")
		print(tab)
		print("\nConstraining nutrients are:")

		excess = tab.diff(axis=1).iloc[:,1]

		print(excess.loc[np.abs(excess) < tol].index.tolist())


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
	foodname1 = "|" + "|".join(foodname1) + "| +"

	temp1 = np.array([ (j,re.sub(regx ,"",i['name'].lower() ), ((len(re.sub(regx+foodname1,"", i['name'].lower())))**2)**0.5 ) for i,j in zip(x,range(len(x)))], dtype=[('index', int),('name','U70') ,('leng', int)])
	
	temp1.sort(order='leng',kind='mergesort')

	temp1 = np.append(temp1[np.char.find(temp1['name'], foodname) != -1], temp1[np.char.find(temp1['name'], foodname) == -1])


	return temp1['index']

abcd = [{'name':'test'},{'name':'testtest'},{'name':'tesst'},{'name':'asdaf'},{'name':'testhgdsfgdasdst'},{'name':'tesqweqwt'},{'name':'testqwt'}   ]
#print (sorting_result('test',abcd ))

