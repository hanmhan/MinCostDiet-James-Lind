
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
import nd_m

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






muda1 = nd_m.gsheet().set_index('Food').loc[:'PASTA, UPC: 814553000406',:]
muda2 = test1(muda1)
ndataframe = nd_m.ora(nd_m.lst,mode='test2',lst_index = nd_m.ind)

Prices = muda2.groupby('Food')['NDB Price'].min()


tol = 1e-6 # Numbers in solution smaller than this (in absolute value) treated as zeros

c = Prices.apply(lambda x:x.magnitude).dropna()

'''print (ndataframe.columns.tolist())
print (c.index.tolist())
print (c)'''
# Compile list that we have both prices and nutritional info for; drop if either missing
# Drop nutritional information for foods we don't know the price of,
# and replace missing nutrients with zeros.
Aall = ndataframe.fillna(0)


# Drop rows of A that we don't have constraints for.
Amin = Aall.loc[bmin.index]
Amax = Aall.loc[bmax.index]


# Minimum requirements involve multiplying constraint by -1 to make <=.
A = pd.concat([-Amin,Amax])
b = pd.concat([-bmin,bmax]) # Note sign change for min constraints
# Now solve problem!

result = lp(c, A, b, method='interior-point')


# Put back into nice series
diet = pd.Series(result.x,index=ndataframe.columns)

print("Cost of diet for %s is $%4.2f per day." % (group,result.fun))
print("\nYou'll be eating (in 100s of grams or milliliters):")
print(diet[diet >= tol])  # Drop items with quantities less than precision of calculation.
tab = pd.DataFrame({"Outcome":np.abs(A).dot(diet),"Recommendation":np.abs(b)})
print("\nWith the following nutritional outcomes of interest:")
print(tab)
print("\nConstraining nutrients are:")
excess = tab.diff(axis=1).iloc[:,1]
print(excess.loc[np.abs(excess) < tol].index.tolist())








