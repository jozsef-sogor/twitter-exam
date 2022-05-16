from bottle import get, post, put, delete, request, response
from helpers.function_helpers import create_error_dict
from helpers import validation_helpers as v
from helpers.auth_helpers import requires_auth_or_admin
from models.user_model import User
from models.tweet_model import Tweet
import json

############################################################
@get("/tweets")
def _():
    tweets = Tweet.get_all_tweets()
    print(tweets)
    response.status = 200
    return json.dumps(tweets)

############################################################
@post("/tweets")
@requires_auth_or_admin
def _(access_level):
    session_id = request.get_cookie("token")
    is_in_session = User.is_in_session(session_id)
    if not is_in_session:
        error = create_error_dict(401, "Unathorized. You need to be logged in to tweet")
        return json.dumps(error)

    try:
        tweet_content = v.TweetValidation(request.forms.get("tweet_content")).validate()
        tweet_image = request.files.get("tweet_image")
        tweet_image_url = None
        tweeting_user = User.from_session_id(session_id)
        tweet_creator_id = tweeting_user.id

        if tweet_image:
            tweet_image_url = file_upload.upload_image(tweet_image)

        new_tweet = Tweet(tweet_creator_id, tweet_content, tweet_image_url = tweet_image_url)
        new_tweet.create_tweet()     
    except Exception as e:
        error = create_error_dict(400, str(e))
        response.status = 400
        return json.dumps(error)

    response.status = 200
    return json.dumps(new_tweet.__dict__)  

############################################################
@put("/tweets/<tweet_id>")
@requires_auth_or_admin
def _(access_level, tweet_id):
    session_id = request.get_cookie("token")
    user = User.from_session_id(session_id)
    tweet = Tweet.get_tweet_by_id(tweet_id)

    #if not own tweet and not admin
    if tweet.tweet_creator_id != user.id and access_level < 200:
        error = create_error_dict(401, "Unauthorized")
        response.status = 401
        return json.dumps(error)

    tweet_content = request.forms.get("tweet_content")
    try:
        new_tweet = tweet.update_tweet(tweet_content)
    except Exception as e:
        error = create_error_dict(400, str(e))
        response.status = 400
        return json.dumps(error)

    response.status = 200
    return json.dumps(new_tweet)

############################################################
@delete("/tweets/<tweet_id>")
@requires_auth_or_admin
def _(access_level, tweet_id):
    session_id = request.get_cookie("token")
    user = User.from_session_id(session_id)
    tweet = Tweet.get_tweet_by_id(tweet_id)

    #if not own tweet and not admin
    if tweet.tweet_creator_id != user.id and access_level < 200:
        error = create_error_dict(401, "Unauthorized")
        response.status = 401
        return json.dumps(error)

    try:
        tweet_to_delete = Tweet.get_tweet_by_id(tweet_id)
        tweet_to_delete.delete_tweet()
    except Exception as e :
        error = create_error_dict(400, str(e))
        response.status = 400
        return json.dumps(error)

    response.status = 200
    return json.dumps({"msg": "Tweet deleted succesfully"})