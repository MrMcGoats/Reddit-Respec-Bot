import numpy
import praw

from os import environ
from sys import stderr

def respec(subreddit_name=environ['SUBREDDIT'],keyword=environ['FILTER']):
    
    try:
        bots=numpy.load("bots.npy",allow_pickle=True)
    except:
        bots=[{'id':'bot1','banned':False}]

    reddit=None
    subreddit=None
    new_bots=[]
    for i in bots:
        if not i['banned']:
            reddit=praw.Reddit(i['id'])
            subreddit=reddit.subreddit(subreddit)
            if subreddit.banned(redditor=reddit.user.me()):
                new_bots.append({'id':i['id'],'banned':True})
            else:
                new_bots.append({'id':i['id'],'banned':False})
                break
    bots=new_bots
    
    try:
        if subreddit.banned(redditor=reddit.user.me()):
            print("Cannot continue; all accounts have been banned", file=stderr)
            numpy.save("bots.npy",bots,allow_pickle=True)
            exit(1)
    except AttributeError as e:
        if str(e)=="'NoneType' object has no attribute 'banned'":
            print("Cannot continue; all accounts have been banned", file=stderr)
            numpy.save("bots.npy",bots,allow_pickle=True)
            exit(1)
        print("Unknown error. RIP.",file=stderr)
        exit(2)


    
    numpy.save("bots.npy",bots,allow_pickle=True)
    
    
    posts_replied=None
    try:
        posts_replied=numpy.load("posts_replied.npy")
    except:
        posts_replied=[]
    
    for i in subreddit.new(limit=5):
        if keyword.upper() in i.title.upper():
            if i.id not in posts_replied:
                done=False
                while not done: #This waits for the next allowed request. Reddit ratelimits
                    done=True
                    try:
                        i.reply("F")
                    except:
                        done=False
                        
                posts_replied.append(i.id)
    
    numpy.save("posts_replied.npy",posts_replied,allow_pickle=False)
    
if __name__=="__main__":
    while True:respec()
