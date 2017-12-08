#Hallie Kaufman
#SI 206
#Data-Oriented Programming with APIs and Visualization Final Project

#Below are the necessary import statements for the project
import requests
import json
import sqlite3
import datetime
from pprint import pprint
import Facebook
import facebook

#Setting up cache:
CACHE_FNAME = "APIsAndVisualization_cache.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

#Facebook API
print ("Facebook\n")
# def FB_Time_Frame():
#     days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     time_list = ['12:00 am - 5:59 am', '6:00 am - 11:59 am', '12:00 pm - 5:59 pm', '6:00 pm - 11:59pm']
#     sort_day_time = []
#     for time in time_list:
#     	for day in days_list:
#     		sort_day_time.append(day + ' ' + time)
# 	return (sort_day_time)
# print (sort_day_time)
# pass

def get_facebook_data(access_token_in):
    graph_api = facebook.GraphAPI(access_token = access_token_in, version= '2.1')
    posts = graph_api.request('me?fields=posts.limit(100)')
    return posts
pprint(get_facebook_data(Facebook.access_token))
