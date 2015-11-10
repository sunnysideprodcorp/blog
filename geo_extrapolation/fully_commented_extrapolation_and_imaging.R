############ Interpolate air temperature maps for Estonia (12/05/2010 & 19/05/2010) 
############create thematic map of differences #################

# ggmap is spatial visualization with ggplot2
library(ggmap)

# ggplot2 can plot just about anything, including maps
library(ggplot2) 

# gstat is designed to do statistics operations specifically designed for geographic data
# for example it provides methods to determine whether trends are directional (estimate the spatio-temporal anisotropy)
library(gstat)

# according to its own catalog, this provides "classes and methods for spatial data"
# as well as utility functions for plotting data as maps
# also methods for retrieving coordinates
# we will use the following methods: coordinates() & gridded()
library(sp)

# fairly generic sounding description again
# "set of tools for manipulating and reading geographic data, in particular ESRI shapefiles"
# we use it for readShapePoly()
library(maptools)

#http://www.geo.ut.ee/aasa/LOOM02331/R_idw_interpolation.html
setwd("D:/data/Others'UsefulProjects/geo_extrapolation")

# geode weather staions
# geocode finds latitude and longitude using the Data Science Toolkit or Google Maps
# if using Google Maps you are limited to the API 2500 query/day limit
# you can check your remaining quota using geocodeQueryCheck
# returns a data frame with 'lon' and 'lat' columns
est_weather_stat <- geocode(c('Harku, Estonia', 'Jogeva, Estonia', 'Johvi, Estonia', 'Kihnu, Estonia', 'Kunda, Estonia', 'Kuusiku, Estonia', 'Narva-Joesuu, Estonia', 'Laane-Nigula, Estonia', 'Pakri, Estonia', 'Parnu, Estonia', 'Ristna, Estonia', 'Ruhnu, Estonia', 'Sorve, Estonia', 'Toravere, Estonia', 'Tiirikoja, Estonia', 'Turi, Estonia', 'Valga, Estonia', 'Viljandi, Estonia', 'Vilsandi, Estonia', 'Virtsu, Estonia', 'Vaike-Maarja, Estonia', 'Voru'))

# Create data vector with the names of weather stations
# Since original names were not retained in dataframe (too bad, that would be a nice feature
# Now instead we have to bind back the original names
est_weather_stat_list <- c('Harku, Estonia', 'Jogeva, Estonia', 'Johvi, Estonia', 'Kihnu, Estonia', 'Kunda, Estonia', 'Kuusiku, Estonia', 'Narva-Joesuu, Estonia', 'Laane-Nigula, Estonia', 'Pakri, Estonia', 'Parnu, Estonia', 'Ristna, Estonia', 'Ruhnu, Estonia', 'Sorve, Estonia', 'Toravere, Estonia', 'Tiirikoja, Estonia', 'Turi, Estonia', 'Valga, Estonia', 'Viljandi, Estonia', 'Vilsandi, Estonia', 'Virtsu, Estonia', 'Vaike-Maarja, Estonia', 'Voru')
est_weather_stat_2 <- cbind(est_weather_stat_list, est_weather_stat)

# Now we get the air temperature as it corresponds to each of the weather stations (for which we already have location)
# So we can match air temperature to position on a map
estonia_air_temperature <- read.csv("estonia_air_temperature.csv", sep=";")
estonia_air_temperature_2 <- cbind(est_weather_stat_2, estonia_air_temperature)
write.csv(estonia_air_temperature_2, file="estonia_air_temperature_2.csv")

#INTERPOLATION
# first we need columns of x and y rather than longitude and latitude
estonia_air_temperature_2_test <- estonia_air_temperature_2 # duplicate air temp. data file
estonia_air_temperature_2_test$x <- estonia_air_temperature_2_test$lon # define x & y as longitude and latitude
estonia_air_temperature_2_test$y <- estonia_air_temperature_2_test$lat

# this creates a spatial object
coordinates(estonia_air_temperature_2_test) = ~x + y # set spatial coordinates to create a Spatial object
# so far as I can tell from inspecting attributes(estonia_air_temperature_2_test) after running this line
# this has created a list that includes a $coords key within which x and y are stored, remember that x and y
# were originally created as columns that were simply copies of lon and lat respectively (these are unconfirmed guesses)
# some other interesting attributes I spotted: $bbox seems to indincate the x/y lon/lat values to use for an enclosing box
# everything in the original frame has been squashed inside $data
# there is also #coords.nrs...no idea what this is
plot(estonia_air_temperature_2_test)

# setting up these ranges is probably not necessary since they are quite close to the values I saw in $bbox
x.range <- as.numeric(c(21.76, 28.21)) 
y.range <- as.numeric(c(57.45, 59.72))

grd <- expand.grid(x = seq(from = x.range[1], to = x.range[2], by = 0.1), y = seq(from = y.range[1], to = y.range[2], by = 0.1)) # expand points to grid
# this is a base R function that creates a data frame from all combinations of the supplied vectors
# here the script is making a rectangular grid of points

coordinates(grd) <- ~x + y 
# again we turn out ordinary data frame into a 'spatial' object
# we see the same attributes with attributes(grd) though of course with different values

gridded(grd) <- TRUE
# from the help file: "in assignment promots a non-gridded structure to a gridded one"

plot(grd, cex = 1.5)
# clearly making grd gridded draws it now as a grid rather than as a set of points
# also the summary talks about "cellsize" rather than points

points(estonia_air_temperature_2_test, pch = 1, col = "red", cex = 1)
# now we add the original weather stations back onto the grid as points

# now we get to the actual geographic interpolation
# description in help files is that idw "performs just as krige without a model being passed but allows
# direct specification of the inverse distance weighting power
# I found a nice description under "What is Kriging" here http://people.ku.edu/~gbohling/cpe940/Kriging.pdf
# Kriging is optimal interpolation vased on regression against observed z values of surrounding data points, weighted
# according to spatial covariance values
# the slides also list some advantages of Kriging: compensates for effects of data clustering, gives error estimation
# so essentially we're getting some smoothing that weighs data based on where it came from in estimating values at unmeasured points
idw <- idw(formula = may12 ~ 1, locations = estonia_air_temperature_2_test, newdata = grd)
# presumably newdata are the points to be predicts, locations are known points
# regressing may 12 on a constant means we just want that average value, we are not looking to make it a function of anything

# put in picture here of krieging
# https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Example_of_kriging_interpolation_in_1D.png/400px-Example_of_kriging_interpolation_in_1D.png

idw.output = as.data.frame(idw)
names(idw.output)[1:3] <- c("long", "lat", "var1.pred") # give names to the modelled variables
# this puts the results of the fitting into a readable form
# here's what head(idw.output) looks like:
#long   lat var1.pred var1.var
#1 21.76 57.45  8.931248       NA
#2 21.86 57.45  8.886653       NA
#3 21.96 57.45  8.869074       NA
#4 22.06 57.45  8.890495       NA


# plot results
ggplot() + geom_tile(data = idw.output, aes(x = long, y = lat, fill=var1.pred)) + geom_point(data=estonia_air_temperature_2, aes(x=lon, y=lat), shape=21, colour="red")

#add Estonian contour lines:
est_contour <- readShapePoly("population_in_municipalities_2011_wgs84.shp")
est_contour <- fortify(est_contour, region = "name")
# the fortify method is a "method to convert generic R object into a data frame useful forplotting"
# perhaps shp files just take care of themselves?

ggplot() +
  # these geom tiles alone will give us a blocky heat map look 
  geom_tile(data = idw.output, alpha=0.75, aes(x = long, y = lat, fill=round(var1.pred, 0))) +
  # not surprisingly, these simply add points representing where we have the data
  geom_point(data=estonia_air_temperature_2, aes(x=lon, y=lat), shape=21, size = 10, colour="red") + 
  # this changes the heat map color away from the blueish default
  scale_fill_gradient(low="cyan", high="orange") + 
  # this actually adds the contour
  geom_path(data=est_contour, aes(long, lat, group=group), colour="grey")

# Hurray that wasn't so bad, but there's still a few handwavy things. May be better to leave it that way unless we want to author
# a geostats imaging package
