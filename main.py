import numpy
import praw

from os import environ

def main():
    
    #TODO: check if an account is banned
    try:
        bots=numpy.load("bots.npy")
    except:
        bots=[{'id':'bot1','banned':False}]

    reddit=None
    for i in bots:
        if not i['banned']:
            reddit=praw.Reddit(i['id'])
            
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
