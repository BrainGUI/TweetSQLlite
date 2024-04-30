import csv 
import html
import unidecode
import re
import sqlite3 as lite
import datetime

def decode2(s):
    t = unidecode.unidecode(s)
    if (t == '[?]'): 
        return '_'
    else:
        return(t)

def decodeStr(s):
    t =""
    for x in s:
      t = t+decode2(x)
    return t


def clean_work(s):
    s = html.unescape(s)
    s = decodeStr(s)  #convert foreign language to bad-english
    skips = re.compile(r"[^\x00-\x7F]")  #get rid of anything non-ascii
    s = re.sub(skips," ",s)
    s = re.sub('  ',' ',s)
    s = s.replace('\t',' ')
    s = s.replace('\n',' ')
    s = s.replace("'"," ")  #get rid of single quotes
    s = s.replace('"',' ')  #get rid of double quotes
    s = s.replace('  ',' ') #get rid of extra spaces
    return(s.strip())

def clean(s):
    s=clean_work(s)
    t=clean_work(s)
    while(s!=t):
        s=t
        t=clean_work(s)
    return(s)

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def isRetweet(tweet):
    return (left(tweet,3)=='rt ')

def convert_date_format(date1):
    parsed_date = datetime.datetime.strptime(date1, '%a %b %d %H:%M:%S %z %Y')
    formatted_date = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date

#Creates a DB if not created already
con = lite.connect(r'tweets.db') 
cur = con.cursor()

#create a tweets table
cur.execute('drop table if exists tweets')
cur.execute('create Table tweets(date1 TEXT, tweetID TEXT, TWEET TEXT, handle TEXT, isRetweet INT)')

with open(r"C:\Users\Bryan\Documents\Data_Warehousing\data\Tweets\randomTweets.txt") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for i, row in enumerate(csv_reader):
        date = convert_date_format(row[0])
        tweetID = row[1]
        tweet = clean(row[2]).lower()
        handle = row[4]
        if isRetweet(tweet):
            isRT = 1
        else:
            isRT = 0
        if (i % 20000 == 0):
            con.commit()
            print('committing row ' + str(i))
        try:
            cur.execute("INSERT INTO tweets VALUES (?,?,?,?,?)", (date, tweetID, tweet, handle, isRT))
        except lite.OperationalError as err:
            print("insert error:", err)
            break