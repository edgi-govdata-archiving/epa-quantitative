import requests
from bs4 import BeautifulSoup


url_list=['https://www.epa.gov/enviro/frs-physical-data-model']
for url in url_list:
	# Get information for database URL
	text=requests.get(url).text
	soup=BeautifulSoup(text,'lxml')	
	areas=soup.findAll('area')
	areas

	# Find table names
	table_names = [a.attrs['alt'] for a in areas]
	table_links = [a.attrs['href'] for a in areas]

	data_dic= {}
	table_name_index = 0

	# Find columns in all table names
	iteration = 0
	for table_link in table_links:
		columns_on_page = table_link.find("p_table_name=")
		if (columns_on_page != -1):
			print(iteration)
			iteration+=1
			text=requests.get(table_link).text
			data_dic[table_names[table_name_index]] = {}

			soup=BeautifulSoup(text,'lxml')
			links_list = soup.findAll('a')
			links_list = [links.attrs['href'] for links in links_list]

			column_link_list = [link for link in links_list if (link.find("/enviro/EF_METADATA_HTML") != -1)]
			column_names = [None]*len(column_link_list)
			
			i = 0
			for column in column_link_list:
				start_column_index = column.find("p_column_name") + 14
				end_column_index = column.find("&p_table_name")
				column_name = column[start_column_index:end_column_index]
				column_names[i] = column_name
				i+=1
			data_dic[table_names[table_name_index]]["columns"] = column_names
			table_name_index += 1
		else:
			if (table_link.find("http") != -1):
				url_list.append(table_link)
			else:
				url_list.append("https://www.epa.gov"+table_link)

	print(data_dic)