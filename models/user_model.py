from uuid import uuid4
from g import _USERS, _SESSIONS, _FOLLOWS, _TWEETS, IMG_BASE_URL
from helpers.function_helpers import create_error_dict

class User:
    def __init__(self, user_name, user_first_name, user_last_name, user_email, user_password, id = None, access_level = 100, user_image = "/assets/img/default-profile-image.jpeg"):
        self.id = id if id else str(uuid4())
        self.user_name = user_name
        self.user_image = user_image
        self.user_first_name = user_first_name
        self.user_last_name = user_last_name
        self.user_email = user_email
        self.user_password = user_password
        self.access_level = access_level

    def create_user(self):
        user_obj = self.__dict__
        _USERS.append(user_obj)

    def delete_user(self):
        del _USERS[self]

    def update_user(self, new_user):
        user_and_index = [(index, user) for index, user in enumerate(_USERS) if user["id"] == self.id]
        if user_and_index:
            index = user_and_index[0][0]
            user = user_and_index[0][1]
            _USERS[index] = new_user
            return user
        else:
            raise Exception("User could not be updated. Try again later")
        

    def add_to_session(self):
        session_id = str(uuid4())
        _SESSIONS[session_id] = self.id
        return session_id

    def get_client_user(self):
        #get dictionary from class and make a copy to mutate
        user_obj = self.__dict__
        client_user = user_obj.copy()
        del client_user["user_password"]
        print(IMG_BASE_URL)
        #client_user["user_image"] = IMG_BASE_URL+client_user['user_image']
        print(client_user)
        return client_user

    def follow_other_user(self, followee_id):
        pass

    def unfollow_other_user(self, followee_id):
        pass

    def get_feed(self):
        #for now same as own tweets
        print('#')
        user_tweets = [tweet for tweet in _TWEETS if tweet["tweet_creator_id"] == self.id] + [tweet for tweet in _TWEETS if tweet["tweet_creator_id"] != self.id]
        return user_tweets

    def get_tweets(self):
        user_tweets = [tweet for tweet in _TWEETS if tweet["tweet_creator_id"] == self.id]
        return user_tweets

    @classmethod
    def from_email(cls, email):
        #get user from db by email
        user = [user for user in _USERS if user["user_email"] == email]
        if user: 
            return cls(**user[0]) 
        else: 
            return None
        #return cls(**user)

    @classmethod
    def from_user_id(cls, user_id):
        user = [cls(**user) for user in _USERS if user["id"] == user_id]
        if user:
            return user[0]
        else:
            return None
        #return user

    @classmethod
    def from_session_id(cls, session_id):
        #get user id from session
        #get user from db/list
        #return the class with the data from the db
        user_id = _SESSIONS[session_id]
        if user_id:
            user = None
            for u in _USERS:
                if u["id"] == user_id:
                    user = u
                    break
            return cls(**user)
        
        return create_error_dict(400, "User not logged in")

    @classmethod
    def get_all_client_users(cls):
        users = [cls(**user).get_client_user() for user in _USERS]
        return users

    @staticmethod
    def get_all_users(): #can be called like: User.get_all_users()
        #get users from db
        users = []
        for user in _USERS:
            new_image_url =  IMG_BASE_URL + user["user_image"]
            user["user_image"] = new_image_url
            users.append(user)
            
        return users

    @staticmethod
    def is_in_session(session_id):
        print("from user_model")
        print(session_id)
        print(list(_SESSIONS))
        if session_id in list(_SESSIONS):
            return True
        else:
            return False

    @staticmethod
    def remove_from_session(session_id):
        del _SESSIONS[session_id]
