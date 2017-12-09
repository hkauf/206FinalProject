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
CACHE_FNAME = "206FinalProject.json"
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

#Facebook API
print ("Facebook Data Collection\n")

def get_facebook_data(access_token_in):
    if access_token_in in CACHE_DICTION:
        print ('using cache...')
        pictures = CACHE_DICTION[access_token_in]
    else:
        print('fetching data...')
        graph_api = facebook.GraphAPI(access_token = access_token_in, version= '2.1')
        pictures = graph_api.request('me?fields=id,name,photos.limit(100){created_time,picture,likes{id}}')
        # posts = graph_api.request('me?fields=posts.limit(100){status_type,created_time,likes{id}}')

        CACHE_DICTION[access_token_in] = pictures
        wfile = open(CACHE_FNAME, 'w')
        wfile.write(json.dumps(CACHE_DICTION))
        wfile.close()

    return pictures
   

data = get_facebook_data(Facebook.access_token)
pprint (data)
print('\n Pairing Data \n')

def pairing_data(data):
    list_of_data = []
    post_photos = data['photos']['data']
    for photo in post_photos:
        if 'likes' in photo:
            lst_likes = photo['likes']
            numlikes = len(lst_likes['data'])
        else:
            numlikes = 0
        print('Number of Likes: ' + str(numlikes))

        print('Photo Ids: '+ str(photo['picture']))

        print('Time Created: ' + str(photo['created_time']))

        print ('\n')

        day_time = get_day_time(photo)
        list_of_data.append((numlikes, photo['picture'], photo['created_time']))

    return list_of_data
show_tuples = pairing_data(data)

def get_day_time(photo):
    split_stamp = photo['created_time'].split('-')




#SQL
conn = sqlite3.connect('FBData.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (user_id TEXT, created_time TIMESTAMP, Photos TEXT, Likes INTEGER, Day TEXT)')
