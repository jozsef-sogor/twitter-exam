from uuid import uuid4
import time
from g import _TWEETS, IMG_BASE_URL

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
        _TWEETS.append(tweet_obj)

    def delete_tweet(self):
        for tweet in range(len(_TWEETS)):
            if _TWEETS[tweet]['id'] == self.id:
                del _TWEETS[tweet]
                break

    def update_tweet(self, new_content):
        tweet_and_index = [(index, tweet) for index, tweet in enumerate(_TWEETS) if tweet["id"] == self.id]
        if tweet_and_index:
            index = tweet_and_index[0][0]
            new_tweet = tweet_and_index[0][1]
            new_tweet["tweet_content"] = new_content
            _TWEETS[index] = new_tweet
            return new_tweet
        else:
            raise Exception("Tweet could not be updated. Try again later")
        

    @classmethod
    def get_tweet_by_id(cls, tweet_id):
        tweet = [tweet for tweet in _TWEETS if tweet["id"] == tweet_id]
        if tweet:
            return cls(**tweet[0])
        else:
            return None
        #return cls(**tweet)

    @classmethod
    def get_tweets_by_user_id(cls, user_id):
        tweets = [cls(t**weet) for tweet in _TWEETS if tweet["author_id"] == user_id]
        return tweets

    @staticmethod
    def get_all_tweets():
        tweets = _TWEETS
        return tweets
