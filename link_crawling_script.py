import requests
from bs4 import BeautifulSoup
import json

def desc_unwrapper(url):

	if (url.find("http") == -1):
		url = "https:" + url
	
	data = requests.get(url).text
	desc_start = data.find("Description:")
	desc_end = data[desc_start:].find("\n")
	
	description = str(data[desc_start+17:desc_start+desc_end])
	
	return description

#url_list = ['https://www.epa.gov/enviro/frs-physical-data-model','https://www.epa.gov/enviro/sems-model']
url_list = ['https://www.epa.gov/enviro/sems-model']

data_dic= {}
for url in url_list:
	url_sub_list=[url]
	for url in url_sub_list:
		print(url)
		# Get information for database URL
		text=requests.get(url).text
		soup=BeautifulSoup(text,'lxml')	
		areas=soup.findAll('area')
		areas

		# Find table names
		table_names = [a.attrs['alt'] for a in areas]
		table_links = [a.attrs['href'] for a in areas]

		data_dic[url] = {}
		table_name_index = 0

		# Find columns in all table names
		iteration = 0
		for table_link in table_links:
			columns_on_page = table_link.find("p_table_name=")
			if (columns_on_page != -1):
				print(iteration)
				iteration+=1
				text=requests.get(table_link).text
				data_dic[url][table_names[table_name_index]] = {}

				soup=BeautifulSoup(text,'lxml')
				links_list = soup.findAll('a')
				links_list = [links.attrs['href'] for links in links_list]

				column_link_list = [link for link in links_list if (link.find("/enviro/EF_METADATA_HTML") != -1)]
				column_names = [None]*len(column_link_list)
				column_descriptions = [None]*len(column_link_list)

				
				i = 0
				for column in column_link_list:
					start_column_index = column.find("p_column_name") + 14
					end_column_index = column.find("&p_table_name")
					column_name = column[start_column_index:end_column_index]
					column_names[i] = column_name
					column_descriptions[i] = desc_unwrapper(column)
					i+=1
				
				data_dic[url][table_names[table_name_index]]["columns"] = column_names
				data_dic[url][table_names[table_name_index]]["column descriptions"] = column_descriptions
				table_name_index += 1
			else:
				if (table_link.find("http") != -1):
					url_sub_list.append(table_link)
				else:
					url_sub_list.append("https://www.epa.gov"+table_link)

print(data_dic)

filename = "crawling_output.json"
with open(filename,'w') as f:
	json.dump(data_dic, f, ensure_ascii=False, indent=4, sort_keys=True)
