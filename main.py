import numpy
import praw

from os import environ
from sys import stderr

def main():
    
    try:
        bots=numpy.load("bots.npy",allow_pickle=True)
    except:
        bots=[{'id':'bot1','banned':False}]

    reddit=None
    iterator=0
    for i in bots:
        if not i['banned']:
            reddit=praw.Reddit(i['id'])
            if reddit.subreddit(environ['SUBREDDIT']).banned(redditor=reddit.user.me()):
                bots[iterator]['banned']==True
            else:
                break
        iterator+=1
        
    if reddit.subreddit(environ['SUBREDDIT']).banned(redditor=reddit.user.me()):
        print("Cannot continue; all acounts have been banned", file=stderr)
        exit(1)

    numpy.save("bots.npy",bots,allow_pickle=True)
    
    subreddit=reddit.subreddit(environ['SUBREDDIT'])
    
    posts_replied=None
    try:
        posts_replied=numpy.load("posts_replied.npy")
    except:
        posts_replied=[]
    
    for i in subreddit.new(limit=5):
        if "M4F" in i.title.upper():
            if i.id not in posts_replied:
                try:
                    i.reply("F")
                except:
                    break
                posts_replied.append(i.id)
    
    numpy.save("posts_replied.npy",posts_replied,allow_pickle=False)
    
if __name__=="__main__":
    main()
