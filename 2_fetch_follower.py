# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

#Import the necessary packages
from twitter import *
import re
import pandas as pd
import tweepy
import os
# Variables that contains the user credentials to access Twitter API


ACCESS_TOEKN = '298895919-sZSRQi67wIogm33GPZ3ZuGWjWRlp9aEfa6Teqrbn'
ACEESS_KEY = 'TmmVLRxV2NF9ALVrKsjhYLc1TOmgGvkJJ0sH5dLGWELEG'
CONSUMER_KEY = '298895919-4PJOOc0U2RSCa1bZy7LrzKWfk4gMlCLfzj2LLTAM'
CONSUMER_SECRET = 'qAhQaO2goXfxZRPGR93oZxitClXKaBQ12n6Hpqj0Ff1Pc'

auth=tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOEKN, ACEESS_KEY)
api = tweepy.API(auth, wait_on_rate_limit=True)

def getFollowers(names):
    twt_id=[]
    twt_name=[]
    twt_ids=[]
    twt_names=[]
    for name in names:
        count=0
        for user in tweepy.Cursor(api.followers, screen_name=name).items():
            count+=1
            if count > 100:
                break
            twt_id=user.id
            twt_name=user.screen_name
            twt_ids.append(twt_id)
            twt_names.append(twt_name)
        df_v = pd.DataFrame()
        df_v['Follower_ID']=twt_ids
        df_v['User_ID']=twt_names   
        df_e = pd.DataFrame()
        ego=api.get_user(screen_name='1e0na')
        df_e['Follower_ID']=twt_ids
        df_e.insert(0,'Ego_ID',ego.id)
    return df_v, df_e, twt_names;
   
    
    

#set subnetwork ego's screen name
isu.name='IowaStateU'
isu.csv_path_v='isu_verts.csv'
isu.csv_path_e='isu_edges.csv'


member1.name='1e0na'
member1.csv_path_v='member1_verts.csv'
member1.csv_path_e='member1_edges.csv'


egos=['IowaStateU','1e0na']

#-------------------------------------
#----create verts for each subnetwork
#-------------------------------------

dir = "C:/Users/leona/Documents/Leona_Python/MIS544/HW_2"
for ego in egos:
    #get 1st hop of follower list
    hop1_names=[]
    hop1_names=getFollowers('1e0na')[2]
    df_verts=pd.DataFrame()
    df_verts = getFollowers(ego)[0]
    #get 2nd hop of follower list
    df_verts.append(getFollowers(hop1_names)[0], ignore_index = True)
    file_name_v="Ego_" + str(ego) + "_verts.csv"
    df_verts.to_cvs(os.path.join(dir,file_name_v))
    #create edges(relationship) dataset
    df_edges=pd.DataFrame()
    df_edges = getFollowers(member1)[1]
    file_name_e="Ego_" + str(ego) + "edges.csv"
    df_edges.to_cvs(os.path.join(dir,file_name_e))

