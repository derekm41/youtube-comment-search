from urllib import response
from googleapiclient.discovery import build
import pandas as pd
import credentials
import csv
from word2number import w2n

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
    counter = 0
    #For loop variables
    for item in response['items']:
        Tauthor = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
        Ttext = item['snippet']['topLevelComment']['snippet']['textDisplay']
        hour, min, sec, flag = getHoursMinSec(Ttext)
        comment_list.append([Tauthor, hour, min, sec, Ttext, flag])
    # Watch for recurrsion limits
    if "nextPageToken" in response:
        return get_video_comments(youtube, vidId, response['nextPageToken'])

# account for guess formatted like this: 3 1/2 hours, 3.19 hours?????
# I could check if length of the hour, min, or sec is greater than two then there is it can be split by something

def getHoursMinSec(commentText):

    #Separate the string between hours min and seconds.
    #We can assume that the digits before the word 'hour', 'min', 'sec' will be the digits guessed for corresponding time.
    #Algo Logic: 1. Find the index of our keywords for hour ie 'hour', 'hrs'
    #            2. iterate through each character of the comment from the left UP TO the index position to extract digits using getDigits() function.
    #            3. Remove checked substring from comment.
    #            4. Repeat for minutes and seconds
    #keywords: hours, hour, hrs, minutes, min, mins, seconds, second, sec
    #prepare commentText
        
    #Check to see if the text has any number words like 'twelve' using word2number library.
    #We will receive an error if there are no number words and except statement will fire
    commentText = commentText.lower()
    commentText = parseNumberWords(commentText)

    #variables to manipulate
    hours = ""
    minutes = ""
    seconds = ""

    #different keyword check to prevent similar words.
    hoursIndex = commentText.find('hour')
    if hoursIndex == -1:
        hoursIndex = commentText.find('hr')
        if hoursIndex == -1:
            #we have a lot of entries like this 1h20m
            hoursIndex = commentText.find('h')
    if hoursIndex >= 0:
        #Get digits from substring
        hours = getDigits(commentText[:hoursIndex])
        #delete the hour substring used
        commentText = commentText[hoursIndex:] 
     
    #Minutes
    minIndex = commentText.find('minute')
    if minIndex == -1:
        minIndex = commentText.find('min')
        if minIndex == -1:
            minIndex = commentText.find('m')
    if minIndex >= 0:
        minutes = getDigits(commentText[:minIndex])
        commentText = commentText[minIndex:]  
    
    #Seconds
    secIndex = commentText.find('second')
    if secIndex == -1:
        secIndex = commentText.find('sec')
        if secIndex == -1:
            secIndex = commentText.find('s')
    if secIndex >= 0:
        seconds = getDigits(commentText[:secIndex])

    #if there misspelling or any time of logic fallacy this should flag the comment
    flag = ""
    if any(char.isdigit() for char in commentText) and len(hours)==0 and len(minutes)==0 and len(seconds)==0:
        flag = 'Flag'
    
    return hours, minutes, seconds, flag

def getDigits(time):
    timeString= ""
    for char in time:
        if char.isdigit() == True:
            timeString += char
    if len(timeString)==3 and '0' in timeString:
         timeString = timeString.replace('0','')
    return timeString


# There might be more cleaning so may make sense to keep this function seperate
# def cleanCommentText(commentText):
#      # all to lowercase
#     commentText = commentText.lower()
#     # use dicts to parse out number words
#     commentText = parseNumberWords(commentText)
#     return commentText

def parseNumberWords(commentText):
    #explain this function
    units_dict = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
        'eleven': '11',
        'twelve': '12',
        'thirteen': '13',
        'fourteen': '14',
        'fifteen': '15',
        'sixteen': '16',
        'seventeen': '17',
        'eighteen': '18',
        'nineteen': '19'
    }
    tens_dict = {
        'twenty': '20',
        'thirty': '30',
        'forty': '40',
        'fifty': '50',
        'sixty': '60'
    }
    
    commentsplit = commentText.split()
    words = []
    for word in commentsplit:  
        if word in tens_dict:
            words.append(tens_dict[word])
        elif word in units_dict:
            words.append(units_dict[word])
        else: 
            words.append(word)

    commentText = " ".join(words)

    return commentText


#generate a csv file that can be used to filter entries by hour,min,sec to find the correct guess.
def generate_csv():
     #Some characters in comments like pics come through weird. This can be remedied with encoding=''. Different utf produce different results.
    with open('comments.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        thewriter = csv.writer(csvfile)

        for comment in comment_list:
            counter = comment[0]
            author = comment[1]
            hour = comment[2]
            min = comment[3]
            sec = comment[4]
            text = comment[5]
            flag = comment[6]
            thewriter.writerow([author, hour, min, sec, text, flag])

get_video_comments(youtube, video_id)
generate_csv()
# testText = 'hrs'
# getHoursMinSec(testText)


