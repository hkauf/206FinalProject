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
print ("Facebook Data Collection\n")
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
    if access_token_in in CACHE_DICTION:
        print ('using cache...')
        results = CACHE_DICTION[access_token_in]
    else:
        print('fetching data...')
        results = []
        graph_api = facebook.GraphAPI(access_token = access_token_in, version= '2.1')
        pictures = graph_api.request('me?fields=photos.limit(100){created_time,picture,likes{id}}')
        # posts = graph_api.request('me?fields=posts.limit(100){status_type,created_time,likes{id}}')
        results.append(pictures)
        # results.append(posts)

        CACHE_DICTION[access_token_in] = results
        wfile = open(CACHE_FNAME, 'w')
        wfile.write(json.dumps(CACHE_DICTION))
        wfile.close()

    return results
   

data = pprint(get_facebook_data(Facebook.access_token))
    
print('\n LIKES\n')

def get_likes(data):
    likes = data['photos']['data']['likes']
    likes_id= likes['data']['id']
    likescount = 0
    for numlikes in likes:
        if likes_id in likes:
            likescount+=1
    return likescount
    
show_likes = print(get_likes(data))


#SQL
conn = sqlite3.connect('FBData.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (user_id TEXT, created_at TIMESTAMP, Photos TEXT, Likes INTEGER, Day TEXT)')

