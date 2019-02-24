
import pandas as pd
import numpy as np
import json
import requests

import pprint

class HelperFucClass:

	profkey = 'inIyO1begWSRqsYtxS7m6p09PSyq7Qiw7fxzV2qN'
	mykey = 'JPk6gFJ2IAI7YNFQuXQ7wIwUyPXTMxoKAriLzZU2'


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

		#print (tl)
		return col


	def ndhelper1(x,c, url = 'https://api.nal.usda.gov/ndb/V2/reports?format=json'):
		import nd_m
		tl = {}
		col = {}
		for i in x:
			temp1 = nd_m.search(i,c) 
			for q in temp1:
				
				data = requests.get(url , params = (('api_key', HelperFucClass.mykey),('ndbno',q['ndbno']))).json()['foods'][0]['food']['nutrients']


			tl[i] = {}
			for j in data:
				if j['name'] not in col:
					col[j['name']] = 0
				tl[i][j['name']] = j['value']

		for i in col:


			col[i] = [tl[j][i] if i in tl[j] else None for j in tl]

		#print (tl)
		return col