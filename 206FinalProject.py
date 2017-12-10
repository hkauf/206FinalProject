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
  
#SQL
conn = sqlite3.connect('FBData.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (user_id VARCHAR(128), created_time TIMESTAMP, PictureID VARCHAR(128), Likes VARCHAR(128), Day VARCHAR(128))')

print('\n Pairing Data \n')

def pairing_data(data):
    list_of_data = []
    user_id_num = data['id']
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


        split_stamp = photo['created_time'].split('-')
        year = split_stamp[0]
        month = split_stamp[1]
        day_time_split = split_stamp[2].split('T')
        day = day_time_split[0]

        days_tup= (year, month, day)
        weekday = datetime.date(int(year), int(month), int(day)).weekday()

        weekdays_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
        weekday = weekdays_dict[weekday]

        print ('Weekday: ' + str(weekday))
        print ('\n')
        
        list_of_data.append((user_id_num, numlikes, photo['picture'], photo['created_time'], weekday))
    return list_of_data

show_list = pairing_data(data)
print(show_list)
for item in show_list:
    cur.execute('INSERT INTO Facebook (user_id, created_time, PictureID, Likes, Day) VALUES(?, ?, ?, ?, ?)', (item[0], item[3], item[2], item[1], item[4]))
conn.commit()


print('\nSOCIAL MEDIA REPORT: SHOWS THE FREQUENCY OF HOW OFTEN I POST PICTURES ONTO FACEBOOK BASED ON DAY \n')
cur.execute('SELECT Day FROM Facebook')
weekday_freq = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}
for day in cur:
    weekday_freq[day[0]] += 1
    
print(weekday_freq)


cur.close()
