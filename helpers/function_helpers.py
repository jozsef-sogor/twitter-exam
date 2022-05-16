from bottle import request
import uuid
from g import _USERS, _SESSIONS

#not needed anymore
def is_authenticated():
    session_id = request.get_cookie("token")
    if session_id:
        user = _SESSIONS[session_id]
        if user:
            return True
        else:
            return False
    else:
        return False

#not needed anymore
def get_user_from_session():
    session_id = request.get_cookie("token")
    if is_authenticated():
        return _SESSIONS[session_id], session_id
    else:
        return None, None

#not needed anymore
def get_user_by_id(user_id):
    for user in _USERS:
        if user["id"] == user_id:
            return user
    return None

def is_user_data_already_in_use(user_data_key, user_data_value):
    for user in _USERS:
        print(user_data_key)
        print(user[user_data_key])
        print("printing user data key")
        print(user[user_data_key])
        if user[user_data_key] == user_data_value:
            return True
    return False

#not needed anymore
def create_new_session(user_id):
    session_id = str(uuid.uuid4())
    _SESSIONS[session_id] = user_id
    return str(session_id)

#not needed anymore
def copy_dict(data, strip_values=False, remove_keys=[]):
    if type(data) is dict:
        out = {}
        for key, value in data.items():
            if key not in remove_keys:
                out[key] = copy_dict(value, strip_values=strip_values, remove_keys=remove_keys)
        return out
    else:
        return [] if strip_values else data

#not needed anymore
def create_client_user_dict(user):
    return copy_dict(user, False, ["user_password",])

def create_error_dict(code=None, message=""):
    error = {
        "code": code,
        "message": message
    }
    return error

def is_valid_names(string):
    min_length = 1
    max_length = 20
    
    if min_length <= len(string) <= max_length:
        return True
    else: 
        return False