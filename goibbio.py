import requests
import json
import csv
# get city id https://voyager.goibibo.com/api/v1/hotels_search/find_node_by_name/?params={%22search_query%22:%22ban%22,%22limit%22:10,%22qt%22:%22N%22,%22city_id%22:%226771549831164675055%22,%22inc_ggl_res%22:true}
page = requests.get('https://hermes.goibibo.com/hotels/v7/search/data/v3/6771549831164675055/20181113/20181114/1-2-0?s=popularity&cur=INR&f={%22tags%22:[%22ALL%22]}&sb=0&pid=0&im=true')

response_data=json.loads(page.text)
print(response_data['data'])
jsondata=response_data['data']
extracted_data=[]
for data in jsondata:
	data = {
                'HotelName':data['hn'],
                'orginal_price': data['opr'],
                'save_price': data['svg'],
                'currunt_price': data['spr'],
                'g_rating': data['gr'],
                'location': data['l']
     }
	extracted_data.append(data)
	
with open('names.csv', 'w') as csvfile:
	fieldnames = ['HotelName','orginal_price', 'save_price', 'currunt_price', 'g_rating', 'location']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()
	for d in extracted_data:
		writer.writerow(d)

	