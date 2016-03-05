import json
import csv
import sys
from sets import Set
import collections

def createSingleItem(row):
    single_item = []
    single_item.append(row.get("County"))
    single_item.append(row.get("Office"))
    single_item.append(row.get("Dist"))
    single_item.append(row.get("First Name"))
    single_item.append(row.get("Last Name"))
    single_item.append(row.get("Party"))
    single_item.append(row.get("URL"))
    single_item.append("")
    return single_item

#Get the name of the csv file from the command line
csv_filename = sys.argv[-1]

#open the csv with DictReader
csvfile = open(csv_filename, 'rU')
reader = csv.DictReader(csvfile)

#Create an empty counties, upper, and lower dictionaries
counties_dict = collections.OrderedDict()
upper_dict = collections.OrderedDict()
lower_dict = collections.OrderedDict()

counties_dict = {"counties" : {}}
upper_dict = {"upper" : {}}
lower_dict = {"lower" : {}}

#Create sets to store the lists of unique counties, upper, and lower districts from the csv
counties = Set()
upper_districts = Set()
lower_districts = Set()

#Create the statewide_dict and the unique lists of counties
statewide_dict = {"statewide" : []}
for row in reader:
    if row.get("Office") == "Senate":
        upper_districts.add(row.get("Dist").lower())
    if row.get("Office") == "House of Delegates":
        lower_districts.add(row.get("Dist").lower())
    if row.get("County") == "Statewide":
        single_item = createSingleItem(row)
        statewide_dict["statewide"].append(single_item)
    elif row.get("First Name") != "":
        lc_county = row.get("County").lower()
        counties.add(lc_county)

counties = sorted(list(counties))
upper_districts = sorted(list(upper_districts))
lower_districts = sorted(list(lower_districts))

#Add keys for each county to counties_dict
for county in counties:
    counties_dict["counties"][county] = []

#Add keys for each upper district to upper_dict
for upper_district in upper_districts:
    upper_dict["upper"][upper_district] = []

#Add keys for each lower district to lower_dict
for lower_district in lower_districts:
    lower_dict["lower"][lower_district] = []

#Add county items to the county lists, which are the values of each counties_dict dictionary item
csvfile.seek(0)
next(reader, None)
for row in reader:
    if row.get("County") != "Statewide" and row.get("Office") not in ("Senate", "House of Delegates") and row.get("First Name") != "":
        single_item = createSingleItem(row)
        counties_dict["counties"][row.get("County").lower()].append(single_item)

#Add upper items to the upper lists, which are the values of each upper_dict dictionary item
csvfile.seek(0)
next(reader, None)
for row in reader:
    if row.get("Office") == "Senate" and row.get("First Name") != "":
        single_item = createSingleItem(row)
        upper_dict["upper"][row.get("Dist").lower()].append(single_item)

#Add lower items to the lower lists, which are the values of each lower_dict dictionary item
csvfile.seek(0)
next(reader, None)
for row in reader:
    if row.get("Office") == "House of Delegates" and row.get("First Name") != "":
        single_item = createSingleItem(row)
        lower_dict["lower"][row.get("Dist").lower()].append(single_item)


print json.dumps(statewide_dict)
print json.dumps(counties_dict)
print json.dumps(upper_dict)
print json.dumps(lower_dict)
