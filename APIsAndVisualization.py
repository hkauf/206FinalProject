#Hallie Kaufman 
#SI 206 
#Data-Oriented Programming with APIs and Visualization Final Project

#Below are the necessary import statements for the project
import json
import pprint
#setting up cache:
CACHE_FNAME = "APIsAndVisualization_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}
