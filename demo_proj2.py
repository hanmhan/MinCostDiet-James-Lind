from helper import *






demo = FoodLibrary()
df = pd.read_csv(demo.foods_spreadsheet)
lst = list(df['Food'])
#demo.nutrition_dataframe(lst)


