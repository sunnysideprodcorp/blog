from pandas import DataFrame, read_csv
import urllib2
import urllib
import json
from time import sleep

# note DON'T DO This
# use geopy instead
# https://github.com/geopy/geopy

# first get the data into a dataframe so we can geocode each neighborhood
geo = read_csv("neighborhoods.csv")

#geocode each neighborhood
API_KEY = "YOUR_KEY_HERE"

def get_coords(data):
        '''get coordinates from json data parsed into a dictionary as returned by Google geocoding API'''
        
        # ask forgiveness not permission
        try:
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
        except:
                return None
        else:
                return(lat, lng)

def geo_code(neighborhood_vec):
    '''cycle through neighborhood_vec and call Google geocoding API for each neighborhood, returning results in a list of lists, 
    each sublist containing neighborhood name and coordinates'''
        
    address_list = []
    PARTIAL_API = "https://maps.googleapis.com/maps/api/geocode/json?key="+API_KEY+"&"

    for neighborhood in neighborhood_vec:
        try:
                url = PARTIAL_API + urllib.urlencode({"address" : neighborhood +", New York"})
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36')]
                response = opener.open(url)
                data = json.load(response)
                coords = get_coords(data)
                address_list.append([neighborhood, coords]) # keep track of the neighborhood so we can join coordinates back to original data set and verify matches
                sleep(.3) # keep below API rate limit
        except:
                pass

    
    return address_list



coords = geo_code(geo['Descriptive Name'])
coords_df = DataFrame(coords, columns=["Name", "Coords"])
coords_df.to_csv("coords.csv")
