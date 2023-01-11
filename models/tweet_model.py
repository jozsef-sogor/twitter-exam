from uuid import uuid4
import time
from g import _TWEETS, IMG_BASE_URL
from .database import Database

class Tweet:
    def __init__(self, tweet_creator_id, tweet_content, id=None, tweet_image_url = None, created_at=None, updated_at=None):
        self.id = id if id else str(uuid4())
        self.tweet_content = tweet_content
        self.tweet_image_url = f"{IMG_BASE_URL}{tweet_image_url}"
        self.tweet_creator_id = tweet_creator_id
        self.updated_at = time.time()
        self.created_at = created_at if created_at else time.time()

    def create_tweet(self):
        tweet_obj = self.__dict__
        _TWEETS.append(tweet_obj) #add tweet to an in memory list
        ##add tweet to db
        db = Database()
        #creating a new tweet user table 
        db.execute("CREATE TABLE IF NOT EXISTS tweets (id VARCHAR(255) PRIMARY KEY, tweet_content VARCHAR(255), tweet_image_url VARCHAR(255), tweet_creator_id VARCHAR(255), created_at VARCHAR(255), updated_at VARCHAR(255))")
        if(db):
            print("tweet table is created successfully........")
        #If db exist then insert tweet data into tweets table TODO:(Vulnerable to SQL injection)
        db.execute("INSERT INTO tweets (id, tweet_content, tweet_image_url, tweet_creator_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", (self.id, self.tweet_content, self.tweet_image_url, self.tweet_creator_id, self.created_at, self.updated_at))
        db.commit()
        db.close()
        return tweet_obj

    def delete_tweet(self):
        db = Database()
        db.execute("DELETE FROM tweets WHERE id = %s", (self.id,)) 
        db.commit()
        db.close()
        return "Tweet deleted successfully"

    def update_tweet(self, new_content):
        #Update tweet in db
        db = Database()
        if new_content:
            db.execute("UPDATE tweets SET tweet_content = %s WHERE id = %s", (new_content, self.id))
            db.commit()
            db.close()
            return new_content
        else:
            raise Exception("Tweet could not be updated. Try again later")    
        

    @classmethod
    def get_tweet_by_id(cls, tweet_id):
        #Get tweet from db
        db = Database()
        db.execute("SELECT * FROM tweets WHERE id = %s", (tweet_id,))
        tweet = db.fetchone()
        db.close()
        return tweet

    @classmethod
    def get_tweets_by_user_id(cls, user_id):
        #Get tweets from db
        db = Database()
        db.execute("SELECT * FROM tweets WHERE tweet_creator_id = %s", (user_id,))
        tweets = db.fetchall()
        db.close()
        return tweets

    @staticmethod
    def get_all_tweets():
        #Get all tweets from db
        db = Database()
        db.execute("SELECT * FROM tweets")
        tweets = db.fetchall()
        db.close()
        return tweets
