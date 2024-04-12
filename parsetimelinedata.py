

import sys
import json
import datetime

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="e-lu6a", timeout=10)

# take command line input as a file (assumed to be json), open it, 
# read it, load it, and then close the file
with open(sys.argv[1], "r") as file:
    data = json.load(file)

timeline_objects = data["timelineObjects"]

cities = {}

for i in timeline_objects:
    lat = ""
    long = ""
    # parse the object, depending on its type
    if "activitySegment" in i:
        entry = i["activitySegment"]

        lat = str(entry["endLocation"]["latitudeE7"]/(10**7))
        long = str(entry["endLocation"]["longitudeE7"]/(10**7))
    elif "placeVisit" in i:
        entry = i["placeVisit"]

        lat = str(entry["location"]["latitudeE7"]/(10**7))
        long = str(entry["location"]["longitudeE7"]/(10**7))

    # get the location
    # we could theoretically get the location directly by parsing the address
    # instead of using geopy; also nominatim has a 1 request / second limit
    location = geolocator.reverse(lat + "," + long)
    city = location.raw["address"]["city"]

    # find the time spent
    start_time = datetime.datetime.fromisoformat(entry["duration"]["startTimestamp"])
    end_time = datetime.datetime.fromisoformat(entry["duration"]["endTimestamp"])
    duration = end_time - start_time

    # add the entry
    if city in cities:
        cities[city] += duration
    else: 
        cities[city] = duration

for city in cities:
    print(city, ": ", cities[city])