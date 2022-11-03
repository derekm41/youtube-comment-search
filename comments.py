from urllib import response
from googleapiclient.discovery import build
import pandas as pd
import credentials
import csv

#global variables
api_key = credentials.api_key
video_id = 'e6cV0X6gQg0'
# 'jV8IyoATXwA'
comment_list = []

youtube = build('youtube', 'v3', developerKey=api_key)

#Function to get video comments
def get_video_comments(youtube, vidId, token=''):

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=vidId,
        maxResults=100,
        pageToken=token
    )
    response = request.execute()
    #For loop variables
    for item in response['items']:
        Tauthor = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        Ttext = item['snippet']['topLevelComment']['snippet']['textDisplay']
        hour, min = extractHrsMins(Ttext)
        comment_list.append([Tauthor, hour, min])
    # Watch for recurrsion limits
    if "nextPageToken" in response:
        return get_video_comments(youtube, vidId, response['nextPageToken'])

def extractHrsMins(commentText):
    time = [char for char in commentText if char.isdigit()]
    time_format = ""
    time_length = len(time)
    if time_length == 3:
        hour = time[0]
        min = time[1] + time[2]
        time_format = time[0] + 'hrs ' + time[1] + time[2] + 'mins'
    elif time_length == 1: 
        hour = time[0]
        min = 0
        time_format = time[0] + 'hrs 0mins'
    else:
        hour = 0
        min = 0
        time_format = 'NA'
    return hour, min


def generate_csv():
     #Some characters in comments like pics come through weird. This can be remedied with encoding=''. Different utf produce different results.
    with open('comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        thewriter = csv.writer(csvfile)

        for comment in comment_list:
            author = comment[0]
            hour = comment[1]
            min = comment[2]
            thewriter.writerow([author, hour, min])

get_video_comments(youtube, video_id)
generate_csv()
