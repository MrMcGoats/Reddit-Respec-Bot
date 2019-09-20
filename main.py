import numpy
import praw

from os import environ

def main():
    reddit=praw.Reddit('bot1')
    subreddit=reddit.subreddit(environ['SUBREDDIT'])
    
    posts_replied=None
    try:
        posts_replied=numpy.load("posts_replied.npy")
    except:
        posts_replied=[]
    
    for i in subreddit.new(limit=5):
        if "M4F" in i.title.upper():
            if i.id not in posts_replied:
                i.reply("F")
                posts_replied.append(i.id)
    
    numpy.save("posts_replied.npy",posts_replied,allow_pickle=False)
    
if __name__=="__main__":
    main()
