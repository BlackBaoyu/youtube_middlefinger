#pip install google-api-python-client 
from googleapiclient.discovery import build

#API&頻道網址
youTubeApiKey = 'AIzaSyC1NJDvSwt1eAzzYWhZvwY2uTOLwT-nr1M'
youtube = build('youtube','v3',developerKey = youTubeApiKey)
channelId = 'UCYjB6uufPeHSwuHs8wovLjg'

#統計資料
statdata = youtube.channels().list(part = 'statistics',id = channelId).execute()
stats = statdata['items'][0]['statistics']
#stats

#影片數
videoCount = stats['videoCount']
#videoCount

#觀看次數
viewCount = stats['viewCount']
#viewCount

#訂閱人數
suscriberCount = stats['subscriberCount']
#suscriberCount

snippetdata = youtube.channels().list(part = 'snippet', id=channelId).execute()
#snippetdata 

#頻道營稱
title = snippetdata['items'][0]['snippet']['title']
#title

#描述
description = snippetdata['items'][0]['snippet']['description']
#description

#頻道圖案
logo = snippetdata['items'][0]['snippet']['thumbnails']['default']['url']
#logo


contentdata = youtube.channels().list(id=channelId,part='contentDetails').execute()
playlist_id = contentdata['items'][0]['contentDetails']['relatedPlaylists']['uploads']
videos = [ ]
next_page_token = None

while 1:
  res = youtube.playlistItems().list(playlistId=playlist_id, part='snippet', maxResults=50, pageToken=next_page_token).execute()
  videos += res['items']
  next_page_token = res.get('nextPageToken')

  if next_page_token is None:
    break
#print(videos) #這裡要做抓時間

#找出video網址
video_ids = list(map(lambda x:x['snippet']['resourceId']['videoId'], videos))
#print(video_ids)

#影片統計資料
stats = []
for i in range(0, len(video_ids), 40):
  res = (youtube).videos().list(id=','.join(video_ids[i:i+40]),part='statistics').execute()
  stats += res['items']
#print(stats)

#製作list
title = []
time = []
liked = []
disliked = []
views = []
comment = []
sequence = []

#把資料裝進list
for i in range(len(videos)):
  title.append((videos[i])['snippet']['title'])
  sequence.append(int(i))
  liked.append(int((stats[i])['statistics']['likeCount']))
  disliked.append(int((stats[i])['statistics']['dislikeCount']))
  views.append(int((stats[i])['statistics']['viewCount']))
  comment.append(int((stats[i])['statistics']['commentCount']))
  time.append((videos[i])['snippet']['publishedAt'])

#把list顛倒
n_title = title[::-1]
n_time = time[::-1]
n_liked = liked[::-1]
n_disliked = disliked[::-1]
n_views = views[::-1]
n_comment = comment[::-1]

#製作dataframe
import pandas as pd
data = {'title' : n_title, 'time' : n_time, 'liked' : n_liked, 'disliked' : n_disliked, 'views' : n_views, 'comment' : n_comment}
df = pd.DataFrame(data)

#視覺化視覺化
#import matplotlib.pyplot as plt
#plt.plot(sequence, n_views)
#plt.xlabel('videos')
#plt.ylabel('views')
#plt.show

#df以csv形式上傳雲端
from google.colab import drive
drive.mount('/gdrive')
write_csv = df.to_csv(index = False)
f = open('/gdrive/My Drive/中指通.csv', 'w')
f.write(write_csv)
f.close()
!cat '/gdrive/My Drive/中指通.csv'
