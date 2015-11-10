from pandas import DataFrame, read_csv, concat, merge
from geopy.distance import great_circle
from itertools import combinations
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import sys

# Get the neighborhood names from the original data
codes = read_csv("neighborhoods.csv")
# And get the coordinates we recorded from our Google API calls
coords = read_csv("coords.csv")

# calculate distances between all sensor pairs
result = merge(codes, coords, left_on = 'Descriptive Name', right_on = 'Name')
coords = result['Coords']
combos = combinations(coords, 2)
distance_in_miles = []
for c in combos:
    distance_in_miles.append(great_circle(c[0], c[1]).miles)

# HISTOGRAM
# Histogram those distances to look for evidence of geometrically structured sensor patterns
binwidth = 1
# All values hist
plt.hist(distance_in_miles, bins=np.arange(min(distance_in_miles), max(distance_in_miles) + binwidth, binwidth))
plt.show()

# 'Good' values hist
plt.hist([d for d in  distance_in_miles if d < 50], bins=np.arange(min(distance_in_miles), max(distance_in_miles) + binwidth, binwidth))
plt.xlim([0, 40])
plt.show()

# Identify what went wrong in the histogram above by seeing which neighborhoods are most often producing unrealistic values

# First create a dataframe with the pairs of coordinates and the distance between them
# Notice you have to get a new combinations iterator because the old one has been 'used up'
# by iterating through it
combos = combinations(coords, 2)
c1 = []
c2 = []
for c in combos:
    print c
    c1.append(c[0])
    c2.append(c[1])
c = DataFrame({"c1":c1, "c2":c2, "distance":distance_in_miles})

# Now you've got the coordinates (c1 and c2) and distance between them
# Match the coordinates to their neighborhood names
result2 = merge(c, result.ix[:,['Name', 'Coords']], left_on = 'c1', right_on = 'Coords')
result3 = merge(result2, result.ix[:,['Name', 'Coords']], left_on = 'c2', right_on = 'Coords')
result4 = result3.sort(['distance'], ascending = [0])

# Record which pairs are bad in that they give distances that can't possibly be correct
# Here indicated as > 50 miles
bad_pairs = result4[result4['distance']>50][['distance', 'Name_x', 'Name_y']]
bad_pairs.to_csv("bad_pairs.csv")

# When we count the occurrence of neighborhoods in these bad pairs, only one neighborhood shows up repeatedly. Its geocoding is wrong
bad_pairs.groupby('Name_y').count()
bad_pairs.groupby('Name_x').count()


# MAP
#Create NYC map
map = Basemap(llcrnrlon=-74.3,llcrnrlat=40.5,urcrnrlon=-73.6,urcrnrlat=40.9,
              resolution='i', projection='lcc', lat_0 = 40.5, lon_0 = -74 )
fig = plt.figure()
ax = plt.axes()

# Add points to map via their coordinates
points_with_annotation = []
for i in range(60):
    try:
        c = coords[i]
        s = c[1:-1]
        s = [float(n) for n in  s.split(",")]   
        x, y = map(s[1], s[0])
        point, = map.plot(x, y, 'ro', markersize=4)

        annotation = ax.annotate(result['Name'][i],
                                 xy=(x, y), xycoords='data',
                                 xytext=(i + 1, i), textcoords='data',
                                 horizontalalignment="left",
                                 arrowprops=dict(arrowstyle="simple",
                                                 connectionstyle="arc3,rad=-0.2"),
                                 bbox=dict(boxstyle="round", facecolor="w", 
                                           edgecolor="0.5", alpha=0.9)
                             )
        annotation.set_visible(False)

        points_with_annotation.append([point, annotation])

    except:
        print i
        break

# Adding a mouseover event
def on_move(event):
    visibility_changed = False
    for point, annotation in points_with_annotation:
        should_be_visible = (point.contains(event)[0] == True)

        if should_be_visible != annotation.get_visible():
            visibility_changed = True
            annotation.set_visible(should_be_visible)

    if visibility_changed:        
        plt.draw()

on_move_id = fig.canvas.mpl_connect('motion_notify_event', on_move)

map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()
map.drawcountries()
map.drawstates()
map.drawmapboundary() 
plt.show()

# looking at these things, obviously wrong neighborhood locations are:
# Astoria/Long Island City, Washington Heights/Inwood
# also Jackson Heights and Elmhurst should be swapped
