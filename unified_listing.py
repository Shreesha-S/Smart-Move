import requests
import json

"""
print ("Enter the locality frequently visited.")
inp_str = raw_input().strip()

"""
print "Enter three frequently visited locations."
totlat = 0
totlng = 0
location = []
for i in range(3):
    area = raw_input()
    location.append(area)
    geocode = "https://maps.googleapis.com/maps/api/geocode/json?address=" + area
    gresp = requests.get(geocode)
    gresp = json.loads(gresp.content)
    #arr.append(area)
    """
    gresp -> results -> 0 -> geometry ->bounds, location ->lat, long
    """
    latlng = []
    totlat += gresp["results"][0]["geometry"]["location"]["lat"]
    totlng += gresp["results"][0]["geometry"]["location"]["lng"]

avglat = totlat/3.0
avglng = totlng/3.0

revsgeo = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng="+str(avglat)+","+str(avglng))
revsgeo = json.loads(revsgeo.content)
inp_str = str(revsgeo["results"][-6]["address_components"][0]["long_name"])

area_resph = requests.get("https://regions.housing.com/api/v1/polygon/suggest?input="\
                        +inp_str+"&service_type=rent&cursor=8&source=web")
area_parseh = json.loads(area_resph.content)

area_respc = requests.get("https://www.commonfloor.com/autosuggest.php?c=Bangalore&\
                        item=locationbuilderproject&str="+inp_str+"&res_type=json")
area_respc = json.loads(area_respc.content)

area = []
for area_count in range(area_respc["count"]):
    if area_respc["data"][area_count]["type"] == "area":
        area_codec = area_respc["data"][area_count]["id"]
        area_codec = "area_"+str(area_codec)
        area.append(area_codec)
for area_codec in area:
    url = 'https://www.commonfloor.com/nitro/search/search-results'
    payload = {"search_intent":"rent","property_location_filter":[area_codec],"city":"Bangalore"}
    respc = requests.post(url, data=json.dumps(payload))
    resp_parsec = json.loads(respc.content)

    for houses in range(resp_parsec["result_count"]):
        try:
            print resp_parsec["data"][houses]["children"][0]["title"],
            print resp_parsec["data"][houses]["children"][0]["lat"],
            print resp_parsec["data"][houses]["children"][0]["lng"],
            print resp_parsec["data"][houses]["children"][0]["price"]
        except:
            break


area_codeh = []
for index in range(10):
    try:
        #print area_parseh[index]['uuid']
        if len(area_parseh[index]['uuid']) <= 7:
            area_codeh.append(str(area_parseh[index]['uuid']))
        else:
            None
    except:
        break

for iterat in area_codeh:
    resph = requests.get("https://rails.housing.com//api/v3/rent/filter?&est="\
                    +iterat+"&radius=500&details=true&sort_key=relevance&\
                    sort_order=ASC&personalisation_status=on")
    resp_parseh = json.loads(resph.content)

    for i in range(50):
        try:
            print resp_parseh['hits']['hits'][i]['_source']['locality'],
            if i == 0:
                latitude = resp_parseh['hits']['hits'][i]['_source']['latitude']
                longitude = resp_parseh['hits']['hits'][i]['_source']['longitude']
            print resp_parseh['hits']['hits'][i]['_source']['latitude'],
            print resp_parseh['hits']['hits'][i]['_source']['longitude'],
            print resp_parseh['hits']['hits'][i]['_source']['formatted_rent'],
            print resp_parseh['hits']['hits'][i]['_source']['lifestyle_rating']
        except:
            break

geomatrix = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(latitude)+","+str(longitude)+"&destinations="+location[0]+"|"+location[1]+"|"+location[2]+"|"+"kempegowda+International+Airport+Bangalore")
geomatrix = json.loads(geomatrix.content)
print ""
for i in range(3):
    print "DISTANCE TO ",
    print location[i],
    print ":  ",
    print geomatrix["rows"][0]["elements"][i]["distance"]["text"]

