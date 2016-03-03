import json
import csv
import sys
from sets import Set

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

#Create an empty counties dictionary
countiesDict = {"counties" : {}}

#Create an empty set to store the list of unique counties from the csv
counties = Set()

#Create the statewideDict and the sorted list of counties
statewideDict = {"statewide" : []}
for row in reader:
    if row.get("County") == "Statewide":
        single_item = createSingleItem(row)
        statewideDict["statewide"].append(single_item)
    elif row.get("First Name") != "":
        lc_county = row.get("County").lower()
        counties.add(lc_county)
counties = sorted(list(counties))

#Add keys for each county to countiesDict
for county in counties:
    countiesDict["counties"][county] = []

#Add county items to the county lists, which are the values of each countiesDict dictionary item
csvfile.seek(0)
next(reader, None)
for row in reader:
    if row.get("County") != "Statewide" and row.get("Office") not in ("Senate", "House of Delegates") and row.get("First Name") != "":
        single_item = createSingleItem(row)
        countiesDict["counties"][row.get("County").lower()].append(single_item)

print json.dumps(statewideDict)
print json.dumps(countiesDict)

#Still need to order the dict
#print json.dumps(collections.OrderedDict(countiesDict))



"""def indexFunction(indexKey):


stateWideObject = indexFunction("statewide")

for row in reader:


print masterDictionary
"""
#Apend each dictionary item to masterDictionary
#for row in reader:


"""
1. Open the csv
2. Iterate through each csv row to build dictionary items following this schema:
    [
        "County",
        "Office Title",
        "District",
        "First Name",
        "Last Name",
        "Party",
        "URL",
        ""
    ]

3. Build new JSON object by reindexing the counties for statewide
    "statewide": {
        "county name" : [
            OBJECT INFO
            ],
    }


4. Build new JSON object by reindexing the counties
    counties: {
        "county name" : [
            OBJECT INFO
            ],
    }

5. Reindex the upper districts (assume office=senate)
    "upper": {
        "District" : [
            OBJECT INFO
        ]
    }

 6. Reindex the lower districts (assume office=House of Delegates)
    "lower": {
        "District" : [
            OBJECT INFO
        ]
    }

"""
