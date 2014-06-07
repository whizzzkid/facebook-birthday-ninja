#!/usr/bin/python

# Should automatically lookup my facebook page and handle all
# my birthday wishes.
# author: me@nishantarora.in
# version : 1.0

# logFile
logF = 'bdayLog.csv'

#reply messages
replies = [
  """Thanks for this... :):P

  ~ birthday ninja""",
  """Really appreciated... :);)

  ~ birthday ninja""",
  """Yayeee... :):)

  ~ birthday ninja""",
  """sweet... :):D

  ~ birthday ninja""",
  """rocking... :)B-)

  ~ birthday ninja"""
]

# repeat replies
repeatReply = """Thanks... I am not sure what to reply, but I'll notify Nishant regarding the repeat post... u rock!...

  ~ birthday ninja
  """

# fb security bypass... since i'll be the only user...
# get long validity coupon from facebook should be valid for 60 days
longValidityToken = ''

# user id
# my user id = 10203878055781614
myUserId = ''

# facebook api end point
fbAPI = 'https://graph.facebook.com/v2.0/'

# requreid fields to get api
fbReqFields = '&fields=type,message,actions,from'

# pulling the feeds as json
def getFeedsFromFacebook():
  import requests
  feedURL = fbAPI + myUserId + '/feed/?' + fbReqFields + '&since=' + getSinceTimeStamp() + '&limit=50' + '&access_token=' + longValidityToken
  feed = requests.get(feedURL)
  return feed.json()

# Getting time from past 12 hrs
def getSinceTimeStamp():
  import time
  return str(int(time.time() - (12*60*60)))

# Time stamp generator
def logTime():
  import datetime
  return datetime.datetime.now()

# cURL handler
def performCURL(fbObj, action, msg):
  endPoint = fbAPI + fbObj + "/" + action
  import urllib
  params = {}
  params["access_token"] = longValidityToken
  if msg:
    params["message"] = msg
  params = urllib.urlencode(params)
  fetch = urllib.urlopen(endPoint, params)
  return fetch.read()

# Searching for already done posts
def searchLogForId(fbObjid,col):
  import csv
  with open(logF, 'rt') as logFile:
    reader = csv.reader(logFile, delimiter=',')
    for row in reader:
      if fbObjid == row[col]:
        return False
  return True

# logger
def logToFile(postTS = '', postID = '', postBy = '', postByID = '', postCont = '', reply = '', lc = '', cc = '', link = ''):
  import csv
  cRow = [str(logTime()), postTS, postID, postBy, postByID, postCont, reply, lc, cc, link]
  f = open(logF, 'a+')
  r = csv.writer(f, dialect='excel')
  r.writerow(cRow)
  f.close()


# prepping logger
logToFile(postTS = "Ops Started")

# I need this in a repeated loop...
while True:
  import time, random, string
  fetch = getFeedsFromFacebook()
  #print fetch
  for post in fetch["data"]:
    # avoiding comments on my status
    # avoiding posts other than statuses on my wall
    # handling post only once
    # handling a user only once
    if post["from"]["id"] != '10203878055781614' and post["type"] == "status" and searchLogForId(post["id"],2):
      # logging to command line
      print str(logTime()) + " new post by " + post["from"]["name"]

      # liking
      like_code = performCURL(post["id"], "likes", "")

      # commenting on first post only
      if searchLogForId(post["from"]["id"],4):
        comment = random.choice(replies)
      else:
        comment = repeatReply

      #posting comment
      comment_code = performCURL(post["id"], "comments", comment)
      message = filter(lambda x:x in string.printable, post['message'])
      #logger
      logToFile(postTS = post["created_time"], postID = post["id"], postBy = post["from"]["name"], postByID =post["from"]["id"], postCont = message, reply = comment, lc = like_code, cc = comment_code, link = post["actions"][0]["link"])

  # I'd like to wait 5 seconds before hitting again...
  #time.sleep(5)
