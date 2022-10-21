from urllib import response
from googleapiclient.discovery import build
import pandas as pd
import credentials
import csv


api_key = credentials.api_key
video_id = 'jV8IyoATXwA'

youtube = build('youtube', 'v3', developerKey=api_key)

comment_list = []

#Function to get video comments
def get_video_comments(youtube, vidId):
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=vidId
    )

    response = request.execute()
    total_results = response['pageInfo']['totalResults']
    print(total_results)
    counter = 0
    

    for comment in range(counter, total_results):
        author = response['items'][counter]['snippet']['topLevelComment']['snippet']['authorDisplayName']
        text = response['items'][counter]['snippet']['topLevelComment']['snippet']['textDisplay']
        comment = author + ':' + text
        comment_list.append(comment)
        counter = counter + 1
        
    print(comment_list)
    print(len(comment_list))

def generate_csv():
     #Some characters in comments like pics come through weird. This can be remedied with encoding=''. Different utf produce different results.
    with open('comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        thewriter = csv.writer(csvfile)

        for comment in comment_list:
            seperate = comment.split(':')
            author = seperate[0]
            cText = seperate[1]
            thewriter.writerow([author, cText])

get_video_comments(youtube, video_id)
generate_csv()
