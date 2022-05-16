FORGOT_PW_EMAIL ="22wbexamproject@gmail.com"
EMAIL_PASSWORD = "LampePoster2021!"
IMG_BASE_URL = "http://127.0.0.1:3333/"
JWT_SECRET = "c9fb2625-1779-42ff-a776-3916ed7db682"
PASSWORD_RESET_EXPIRY_TIME_SECONDS = 900 #15 minutes
SESSION_COOKIE_MAX_AGE_SECONDS = 3600 * 24 * 3 #3 days

##############################
_USERS = [
    {
        "id": "1",
        "user_name": "aa",
        "user_image": "/assets/img/default-profile-image.jpeg",
        "user_first_name": "a",
        "user_last_name": "a",
        "user_email": "a@a.com",
        "user_password": "aaaaaa",
        "access_level": 200,
    },
    {
        "id": "2",
        "user_name": "bb",
        "user_image": "/assets/img/default-profile-image.jpeg",
        "user_first_name": "b",
        "user_last_name": "b",
        "user_email": "b@b.com",
        "user_password": "bbbbbb"
    },
    {
        "id": "3",
        "user_name": "cc",
        "user_image": "/assets/img/default-profile-image.jpeg",
        "user_first_name": "c",
        "user_last_name": "c",
        "user_email": "c@c.com",
        "user_password": "cccccc"
    },
]

_TWEETS = [
    {
        "id": "10",
        "tweet_content": "testing content",
        "tweet_image_url": "",
        "tweet_creator_id": "1",
        "created_at": "1",
    },
    {
        "id": "11",
        "tweet_content": "testing content 2",
        "tweet_image_url": "",
        "tweet_creator_id": "1",
        "created_at": "3",
    },
    {
        "id": "12",
        "tweet_content": "testing content 3",
        "tweet_image_url": "",
        "tweet_creator_id": "2",
        "created_at": "2",
    },
]

_FOLLOWS = [
    {
        "id": "4",
        "follower": "1",
        "followee": "2"
    }
]

_USER_ROLES = [
    {
        "id": "6",
        "role_name": "user",
        "access_level": 100
    },
    {
        "id": "7",
        "role_name": "admin",
        "access_level": 200
    }
]

_SESSIONS = {}