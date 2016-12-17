import requests
from bs4 import BeautifulSoup

url='https://www.epa.gov/enviro/sems-model'


text=requests.get(url).text
soup=BeautifulSoup(text,'lxml')

areas=soup.findAll('area')
areas

table_names = [a.attrs['alt'] for a in areas]
#print(table_names)
table_links = [a.attrs['href'] for a in areas]
#print(table_links)

data_dic= {}

table_name_index = 0
for table_link in table_links:
	text=requests.get(table_link).text
	data_dic[table_names[table_name_index]] = {}

	soup=BeautifulSoup(text,'lxml')
	links_list = soup.findAll('a')
	links_list = [links.attrs['href'] for links in links_list]

	column_link_list = [link for link in links_list if (link[0:23] == "//oaspub.epa.gov/enviro")]
	#print(column_link_list)
	column_names = [None]*len(column_link_list)
	i = 0

	for column in column_link_list:
		start_column_index = column.find("p_column_name") + 14
		end_column_index = column.find("&p_table_name")
		column_name = column[start_column_index:end_column_index]
		column_names[i] = column_name
		i+=1
		#print(column_name)
	# In[ ]:
	data_dic[table_names[table_name_index]]["columns"] = column_names
	#print(data_dic)
	table_name_index += 1

print(data_dic)