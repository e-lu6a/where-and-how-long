import sys
import json
import datetime

import closestgeoname.closestgeoname as closestgeoname
# couldn't figure out how to get closestgeoname.py to read constants.py
# when operating as a submodule, so specifying DBFILENAME directly instead
DBFILENAME = './closestgeoname/geonames.sqlite'

# take command line input as a file (assumed to be json), open it, 
# read it, load it, and then close the file
with open(sys.argv[1], "r") as file:
    data = json.load(file)

timeline_objects = data["timelineObjects"]

places = {}

for i in timeline_objects:
    lat = ""
    long = ""
    # parse the object, depending on its type
    if "activitySegment" in i:
        entry = i["activitySegment"]

        lat = entry["endLocation"]["latitudeE7"]/(10**7)
        long = entry["endLocation"]["longitudeE7"]/(10**7)
    elif "placeVisit" in i:
        entry = i["placeVisit"]

        lat = entry["location"]["latitudeE7"]/(10**7)
        long = entry["location"]["longitudeE7"]/(10**7)

    # get the location
    localdb_response = closestgeoname.query_closest_city(DBFILENAME, lat, long)

    if localdb_response is not None:
        place = str(localdb_response[0]) + ", " + str(localdb_response[2])

        # find the time spent
        start_time = datetime.datetime.fromisoformat(entry["duration"]["startTimestamp"])
        end_time = datetime.datetime.fromisoformat(entry["duration"]["endTimestamp"])
        duration = end_time - start_time

        # add the entry
        if place in places:
            places[place] += duration
        else: 
            places[place] = duration
    else:
        print(f"could not find the location for {lat}, {long}; skipping entry")

for place in places:
    print(place, ":", places[place])

def years_months_weeks_hours_days_minutes(td):
    # check conversion code
    years, remainder = divmod(td.days, 365)
    months, remainder = divmod(remainder, 30.4)
    weeks, days = divmod(remainder, 7)

    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)