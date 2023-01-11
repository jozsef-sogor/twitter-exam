from uuid import uuid4
from g import _USERS, _SESSIONS, _FOLLOWS, _TWEETS, IMG_BASE_URL
from helpers.function_helpers import create_error_dict
from .database import Database

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
        _USERS.append(user_obj) #add user to an in memory list
        
        db = Database()
        #Creating a new user table
        db.execute("CREATE TABLE IF NOT EXISTS users ( id SERIAL PRIMARY KEY NOT NULL, user_name varchar(255) NOT NULL, user_first_name varchar(255), user_last_name varchar(255), user_email varchar(255), user_password varchar(255), access_level varchar(255), user_image varchar(255))")
        if(db):
            print("user table is created successfully........")
        #If db exist then insert user data into user table TODO:(Vulnable to SQL injection)
        db.execute("INSERT INTO users (user_name, user_first_name, user_last_name, user_email, user_password, access_level, user_image) VALUES ( %s, %s, %s, %s, %s, %s, %s)", 
                                        (self.user_name, self.user_first_name, self.user_last_name, self.user_email, self.user_password, self.access_level, self.user_image))    
        db.commit()
        db.close()
        return user_obj
        

    def delete_user(self):
        #delete user from database
        db = Database()
        db.execute("DELETE FROM users WHERE id = %s", (self.id,))
        db.commit()
        db.close()
        return "User deleted successfully"

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
        db = Database()
        #Create a session table in db
        db.execute("CREATE TABLE IF NOT EXISTS sessions ( id SERIAL PRIMARY KEY NOT NULL, session_id varchar(255) NOT NULL)")
        if(db):
            print("session table is created successfully........")
        else:
            print("session table is not created successfully........")    
        session_id = str(uuid4())
        session_id = self.id
        db.execute("INSERT INTO sessions (session_id) VALUES ( %s)", (self.id))
        print("seesion id: "+session_id)
        db.commit()
        db.close()
        return session_id

    def get_client_user(self):
        #Login a user and return a client user from the database with password removed
        db = Database()
        db.execute("SELECT * FROM users WHERE user_email = %s", (self.user_email,))
        user = db.fetchone()
        db.close()
        return user


        # user_obj = self.__dict__

        # #get dictionary from class and make a copy to mutate
        # user_obj = self.__dict__
        # client_user = user_obj.copy()
        # del client_user["user_password"]
        # print(IMG_BASE_URL)
        # #client_user["user_image"] = IMG_BASE_URL+client_user['user_image']
        # print(client_user)
        # return client_user

    def follow_other_user(self, followee_id):
        pass

    def unfollow_other_user(self, followee_id):
        pass

    def get_feed(self):
        #get all tweets from users that the user follows
        db = Database()
        db.execute("SELECT * FROM tweets WHERE tweet_creator_id = %s", (self.id,))
        user_tweets = db.fetchall()
        db.close()
        return user_tweets

    def get_tweets(self):
        #get all tweets from user
        db = Database()
        db.execute("SELECT * FROM tweets WHERE tweet_creator_id = %s", (self.id))
        user_tweets = db.fetchall()
        db.close()
        return user_tweets

    @classmethod
    def from_email(cls, email):
        #get user from db by email
        db = Database()
        db.execute("SELECT * FROM users WHERE user_email = %s", (email,))
        user = db.fetchone()
        db.close()
        return user

    @classmethod
    def from_user_id(cls, user_id):
        #get user from db by id
        db = Database()
        db.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = db.fetchone()
        db.close()
        return user

    @classmethod
    def from_session_id(cls, session_id):
        #get user id from session
        db = Database()
        #get user id from session
        db.execute("SELECT * FROM sessions WHERE session_id = %s", (session_id))
        user_id = db.fetchone()
        db.close()
        if user_id:
            user_id = user_id[0]
            #get user from db
            db = Database()
            db.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = db.fetchone()
            db.close()
            if user:
                return cls(**user)
            else:
                return None
        else:
            return create_error_dict(400, "User not logged in")
        

    @classmethod
    def get_all_client_users(cls):
        users = [cls(**user).get_client_user() for user in _USERS]
        return users

    @staticmethod
    def get_all_users(): #can be called like: User.get_all_users()
        #get users from db
        users = []
        # find all users in the database
        db = Database()
        db.execute("SELECT * FROM users")
        users = db.fetchall()
        db.close()
        return users
            

    @staticmethod
    def is_in_session(session_id):
        print("from user_model")
        print(session_id)
        print(list(_SESSIONS))
        #check if session id is in session list
        db = Database()
        #get user id from session
        db.execute("SELECT * FROM sessions WHERE session_id = %s", (session_id))
        user_id = db.fetchone()
        db.commit()
        db.close()
        print(user_id)
        if user_id:
            return True
        else:
            return False


    @staticmethod
    def remove_from_session(session_id):
        #remove session id from session list
        db = Database()
        db.execute("DELETE FROM sessions WHERE session_id = %s", (session_id))
        db.commit()
        db.close()
