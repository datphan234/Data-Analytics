import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#Merging 12 months data
#df=pd.read_csv('./Sale_Data/Sales_April_2019.csv')
files=[file for file in os.listdir('./Sales_Data')]
all_months_data=pd.DataFrame()

for file in files:
	df=pd.read_csv('./Sales_Data/'+file)
	all_months_data=pd.concat([all_months_data,df])

all_months_data.to_csv('all_data.csv',index=False)

all_data=pd.read_csv('all_data.csv')
pd.set_option('max_columns', None)

#Cleanse the data (drop NA, drop 'Or', Convert to correct type)
nan_df=all_data[all_data.isna().any(axis=1)]
all_data=all_data.dropna(how='all')
all_data=all_data[all_data['Order Date'].str[0:2]!='Or']
all_data['Quantity Ordered']=pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])



#Analysis
#1 What was the best month for sale and How much?
#1.1 Add Month and Sale columns
all_data['Month']=all_data['Order Date'].str[0:2]
all_data['Month']=all_data['Month'].astype('int')
all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
month_results=all_data.groupby('Month').sum()
months=range(1,13)
#1.2 Visualize the analysis
'''plt.bar(months,month_results['Sales'])
plt.title('Total Sales per Month in 2019')
plt.xlabel('Month')
plt.ylabel('Sales in USD ($)')
plt.xticks(months)
plt.ticklabel_format(style='plain')
plt.show()'''

#2 Which city has the highest number of sales?
#2.1 Add a City column
def get_city(address):
	return address.split(',')[1]
def get_state(address):
	return address.split(',')[2].split(' ')[1]
all_data['City']=all_data['Purchase Address'].apply(lambda x:get_city(x)+' ('+get_state(x)+')')
city_results=all_data.groupby('City').sum()
cities=[city for city,df in all_data.groupby('City')]
#2.2 Visualize the analysis
'''plt.bar(cities,city_results['Sales'])
plt.title('Total Sales per City in 2019')
plt.xlabel('City')
plt.ylabel('Sales in USD ($)')
plt.xticks(rotation=45,size=8)
#plt.ticklabel_format(style='plain')
plt.show()'''

#3 Which time of a day customers likely to buy products?
#3.1 Convert datetime
all_data['Order Date']=pd.to_datetime(all_data['Order Date'])
all_data['Hour']=all_data['Order Date'].dt.hour
hour_results=all_data.groupby('Hour').sum()
hours=[hour for hour,df in all_data.groupby('Hour')]
#3.2 Visualize the analysis
'''plt.plot(hours,all_data.groupby('Hour').count())
plt.title('Total Sales per Hour in 2019')
plt.xlabel('City')
plt.ylabel('Number of Orders')
plt.xticks(hours)
plt.grid(alpha=0.3)
plt.show()'''

#4 Which products are often sold together?
'''df=all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df=df[['Order ID','Grouped']].drop_duplicates()

# Referenced: https://stackoverflow.com/questions/52195887/counting-unique-pairs-of-numbers-into-a-python-dictionary
count=Counter()
for row in df['Grouped']:
	row_list=row.split(',')
	count.update(Counter(combinations(row_list,3)))
for x,y in count.most_common(10):
	print(x,y)'''

#5 Which products are sold the most?
product_group=all_data.groupby('Product')
quantity_orderer=product_group.sum()['Quantity Ordered']

prices=all_data.groupby('Product').mean()['Price Each']

products=[product for product,df in product_group]

fig,ax1=plt.subplots()
ax2=ax1.twinx()

ax1.bar(products,quantity_orderer,color='steelblue')
ax2.plot(products,prices,color='green',linestyle='--')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered',color='steelblue')
ax2.set_ylabel('Price($)',color='green')
ax1.set_xticklabels(products,rotation=45,size=8)
plt.title('Products Sales and Price correlation')
plt.show()
