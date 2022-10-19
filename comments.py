from urllib import response
from googleapiclient.discovery import build
import pandas as pd
import credentials

api_key = credentials.api_key
video_id = 'jV8IyoATXwA'

youtube = build('youtube', 'v3', developerKey=api_key)

#Function to get video comments
def get_video_comments(youtube, vidId):
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=vidId
    )

    response = request.execute()
    total_results = response['pageInfo']['totalResults']
    counter = 0
    comment_list = []
    for comment in range(counter, total_results):
        author = response['items'][counter]['snippet']['topLevelComment']['snippet']['authorDisplayName']
        text = comment_text = response['items'][counter]['snippet']['topLevelComment']['snippet']['textDisplay']
        comment = author + ' : ' + text
        comment_list.append(comment)
        counter = counter + 1
        
    print(comment_list)

    # return response

get_video_comments(youtube, video_id)
