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
CACHE_FNAME = "206FinalProject.json" #Names the cache
try: #try
    cache_file = open(CACHE_FNAME, 'r') #open the cache file to read
    cache_contents = cache_file.read() #read the cache cache file
    cache_file.close() #close the file
    CACHE_DICTION = json.loads(cache_contents) #load the content of the cache in the form of a string
except: #except
    CACHE_DICTION = {} #empty dictionary

#Facebook API
print ("Facebook Data Collection\n") #print statement letting you know the Facebook Data is beginning

def get_facebook_data(access_token_in): #new function to make Facebook data request, takes in the access token
    if access_token_in in CACHE_DICTION: #check if the access token is in the cache file
        print ('using cache...') #print this statement to let user know the information was cached
        pictures = CACHE_DICTION[access_token_in] #index for the token
    else: #if the code is not in the cache
        print('fetching data...') #print this statement to let user know that the function is fetching data
        graph_api = facebook.GraphAPI(access_token = access_token_in, version= '2.1') #get information from Facebook API
        pictures = graph_api.request('me?fields=id,name,photos.limit(100){created_time,picture,likes{id}}') #making request for this specific information

        CACHE_DICTION[access_token_in] = pictures #index for the information
        wfile = open(CACHE_FNAME, 'w') #open the file in writing mode
        wfile.write(json.dumps(CACHE_DICTION)) #write the file as a string
        wfile.close() #close the file

    return pictures #return the pictures requested

data = get_facebook_data(Facebook.access_token) #call the function
pprint (data) #pretty print the data from the function above

#SQL
conn = sqlite3.connect('FBData.sqlite') #creating database
cur = conn.cursor() #connecting cursor

cur.execute('DROP TABLE IF EXISTS Facebook') #if the table Facebook exists drop it
cur.execute('CREATE TABLE Facebook (user_id VARCHAR(128), created_time TIMESTAMP, PictureWebsite VARCHAR(128), Likes VARCHAR(128), Day VARCHAR(128))') #create the table Facebook with columns user_id, created_time, PictureWebsite, Likes, and Day

#Pairing Data into a List of Tuples
print('\n Pairing Data \n') #print this statement to let the user know the data is being paired

def pairing_data(data): #new function that takes the input data (the output from the previous function)
    user_id = data['id'] #establishing the user_id from the data
    if user_id in CACHE_DICTION: #if the user_id is cached
        print('using cache...') #let the user know that they are using cached data
        list_of_data = CACHE_DICTION[user_id] #output the cached data
    else: #if not in cache
        print('fetching data...') #let the user know the data is not cached and it is being fetched
        list_of_data = [] #empty list
        user_id_num = data['id'] #index through data to find the id
        post_photos = data['photos']['data'] #finding data for photos in the original api request
        for photo in post_photos: #for loop to access individual photo information
            if 'likes' in photo: #if the photo has likes
                lst_likes = photo['likes'] #get the likes information
                numlikes = len(lst_likes['data']) #go through the length of data for all the photos and add the likes from each photo
            else: #otherwise
                numlikes = 0 #the number of likes for that photo is 0 if there is no 'likes' in the photo information
            print('Number of Likes: ' + str(numlikes)) #print the number of likes: and then the number that was calculated

            print('Photo Website: '+ str(photo['picture'])) #print the website of each individual photo

            print('Time Created: ' + str(photo['created_time'])) #print the timestamp

            split_stamp = photo['created_time'].split('-') #split the time stamp by the '-'
            year = split_stamp[0] #get the year for the timestamp
            month = split_stamp[1] #get the month from the timestamp
            day_time_split = split_stamp[2].split('T') #getting the day
            day = day_time_split[0] #day from timestamp

            days_tup= (year, month, day) #tuple for year month day
            weekday = datetime.date(int(year), int(month), int(day)).weekday() #getting specific weekday

            weekdays_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'} #dictionary of weekdays and their corresponding number in the datetime module
            weekday = weekdays_dict[weekday] putting the data together with the weekday dict

            print ('Weekday: ' + str(weekday)) #printing the weekday that the post was posted
            print ('\n') #space

            list_of_data.append((user_id_num, numlikes, photo['picture'], photo['created_time'], weekday)) #creating a list of tuples

            CACHE_DICTION[user_id] = list_of_data # adding to the cache
            wfile = open(CACHE_FNAME, 'w') #opening the cache making it able to write
            wfile.write(json.dumps(CACHE_DICTION)) #writing into the cache in a string form
            wfile.close() #closing the file

    return list_of_data #returning the list of tuples

show_list = pairing_data(data) #calling the function
print(show_list) #printing the function

#Adding Information into SQL Table
for item in show_list: #for each specific photo in the function
    cur.execute('INSERT INTO Facebook (user_id, created_time, PictureWebsite, Likes, Day) VALUES(?, ?, ?, ?, ?)', (item[0], item[3], item[2], item[1], item[4])) #insert the data into the SQL DB
conn.commit() #commit the posts

#Social Media Report counting how many times I posted photos on Facebook based on day
print('\nSOCIAL MEDIA REPORT: SHOWS THE FREQUENCY OF HOW OFTEN I POST PICTURES ONTO FACEBOOK BASED ON DAY \n') #print this to let the user know what is under
cur.execute('SELECT Day FROM Facebook') #selecting the days in the Facebook db
weekday_freq = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0} #frequency counter dictionary, numbers set to 0
for day in cur: #for each day in the database
    weekday_freq[day[0]] += 1 #add a 1 to the dictionary value for that day

print(weekday_freq) #printing the frequency counter

cur.close() #close the cursor
conn.close() #close the connection
