# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

#Import the necessary packages
import twitter
import pandas as pd
import time
# Variables that contains the user credentials to access Twitter API


ACCESS_TOEKN = '298895919-TmpdhVzps8vqEebqI5GyL9z6wJ4zjjrDTIlzAgZF'
ACEESS_KEY = '7kEwaMTaSVDOAZLpeT1P2VqNpsZcelJeMrPJXinNeLWvU'
CONSUMER_KEY = 'v1AxLf4SRzYPgQQFTJNNQbVES'
CONSUMER_SECRET = '88k4eaMuzPLfQ36MLLtLgiasM6DHOnl6WsGSpfmp0hexWsF7iu'

api=twitter.Api(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,access_token_key=ACCESS_TOEKN,access_token_secret=ACEESS_KEY)
api.sleep_on_rate_limit=True

def getFollowers(name):
    twt_id=[]
    twt_name=[]
    twt_ids=[]
    twt_names=[]
    for user in api.GetFollowers(screen_name=name, count=100):
        twt_id=user.id
        twt_name=user.screen_name
        twt_ids.append(twt_id)
        twt_names.append(twt_name)
        time.sleep(5.05)
    df_v = pd.DataFrame()
    df_v['Follower_ID']=twt_ids
    df_v['User_ID']=twt_names   
    df_e = pd.DataFrame()
    ego=api.GetUser(screen_name=name)
    df_e['Follower_ID']=twt_ids
    df_e.insert(0,'Ego_ID',ego.id)
    return df_v, df_e, twt_names;




member0='IowaStateU'    
member1='1e0na'
member2='error_on_line_8'
member3='KallolKapot'
member4='ricky00771'


#-------------------------------------
#----create verts for each subnetwork
#-------------------------------------
#----Ego1: ISU--------
#get 1st hop of follower list
data=getFollowers('IowaStateU')
hop1_names=[]
hop1_names=data[2]
df_verts=pd.DataFrame()
df_verts = data[0]
#create edges(relationship) dataset
df_edges=pd.DataFrame()
df_edges = data[1]
df_edges.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member0_e.json', orient='split')
df_edges.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member0_e.csv', index=False)
#get 2nd hop of follower list
for user in hop1_names:
    data=getFollowers(user)
    data_v=df_verts.append(data[0], ignore_index = True)



df_verts.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member0_v.json', orient='split')
df_verts.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member0_v.csv', index=False)



#----Ego2: Member1--------
#get 1st hop of follower list
data=getFollowers('1e0na')
hop1_names=[]
hop1_names=data[2]
df_verts=pd.DataFrame()
df_verts = data[0]
#create edges(relationship) dataset
df_edges=pd.DataFrame()
df_edges = data[1]
df_edges.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member1_e.json', orient='split')
df_edges.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member1_e.csv', index=False)
#get 2nd hop of follower list
for user in hop1_names:
    data=getFollowers(user)[0]
    df_verts=df_verts.append(data, ignore_index = True)
    time.sleep(5.05)
df_verts.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member1_v.json', orient='split')
df_verts.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member1_v.csv', index=False)


#----Ego3: Member2--------
#get 1st hop of follower list
data = getFollowers('error_on_line_8')
hop1_names=[]
hop1_names=data[2]
df_verts=pd.DataFrame()
df_verts = data[0]
#create edges(relationship) dataset
df_edges=pd.DataFrame()
df_edges = data[1]
df_edges.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member2_e.json', orient='split')
df_edges.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member2_e.csv', index=False)

#get 2nd hop of follower list
for user in hop1_names:
    data=getFollowers(user)
    df_verts=df_verts.append(data[0], ignore_index = True)
    time.sleep(5.05)
df_verts.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member2_v.json', orient='split')
df_verts.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member2_v.csv', index=False)


#----Ego4: Member3--------
#get 1st hop of follower list
data=getFollowers('KallolKapot')
hop1_names=[]
hop1_names=data[2]
df_verts=pd.DataFrame()
df_verts = data[0]
#create edges(relationship) dataset
df_edges=pd.DataFrame()
df_edges = data[1]
df_edges.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member3_e.json', orient='split')
df_edges.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member3_e.csv', index=False)
#get 2nd hop of follower list
for user in hop1_names:
    data=getFollowers(user)
    df_verts=df_verts.append(getFollowers(user)[0], ignore_index = True)
    time.sleep(5.05)
df_verts.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member3_v.json', orient='split')
df_verts.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member3_v.csv', index=False)



#----Ego5: Member4--------
#get 1st hop of follower list
data=getFollowers('ricky00771')
hop1_names=[]
hop1_names=data[2]
df_verts=pd.DataFrame()
df_verts = data[0]
#create edges(relationship) dataset
df_edges=pd.DataFrame()
df_edges = data[1]
df_edges.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member4_e.json', orient='split')
df_edges.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member4_e.csv', index=False)
#get 2nd hop of follower list
for user in hop1_names:
    data=getFollowers(user)
    df_verts=df_verts.append(getFollowers(user)[0], ignore_index = True)
    time.sleep(5.05)
df_verts.to_json('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member4_v.json', orient='split')
df_verts.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/member4_v.csv', index=False)
