from pandas import DataFrame, read_csv
import urllib2
import urllib
import json
from time import sleep

# first get the data into a dataframe so we can geocode each neighborhood
geo = read_csv("neighborhoods.csv")

#geocode each neighborhood
API_KEY = "AIzaSyBYfImi6ROypgOCGbqUtvmALENLLzx-5kU"

def get_coords(data):
        try:
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
        except:
                return None
        else:
                return(lat, lng)

def geo_code(geo_vec):
    address_list = []
    PARTIAL_API = "https://maps.googleapis.com/maps/api/geocode/json?key="+API_KEY+"&"
    for g in geo_vec:
        url = PARTIAL_API + urllib.urlencode({"address" : g+", New York"})
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')]
        response = opener.open(url)
        data = json.load(response)
        coords = get_coords(data)
        address_list.append([g, coords])
        sleep(.3)
    return address_list


coords = geo_code(geo['Descriptive Name'])
coords_df = DataFrame(coords, columns=["Name", "Coords"])
coords_df.to_csv("coords.csv")
