from bottle import get, post, put, request, response
from helpers.function_helpers import create_error_dict, create_client_user_dict, get_user_by_id
from helpers import validation_helpers as v
from helpers.auth_helpers import requires_auth_or_admin
from models.user_model import User
from g import _USERS
import uuid
import json

############################################################
@get("/users")
def _():
    try:
        users = User.get_all_client_users()
    except Exception as e:
        error = create_error_dict(400, str(e))
        response.status = 400
        return json.dumps(error)

    response.status = 200
    return json.dumps(users)

############################################################
@get("/users/<user_id>")
def _(user_id):
    user = User.from_user_id(user_id)
    if user:
        client_user = user.get_client_user()
        response.status = 200
        return json.dumps(client_user)
    else:
        error = create_error_dict(400, "User not found")
        response.status = 400
        return json.dumps(error)

############################################################
@get("/users/<user_id>/tweets")
def _(user_id):
    user = User.from_user_id(user_id)
    if user:
        tweets = user.get_tweets()
        response.status = 200
        return json.dumps(tweets)
    else:
        error = create_error_dict(400, "User not found")
        response.status = 400
        return json.dumps(error)
    
############################################################
@get("/users/<user_id>/feed")
@requires_auth_or_admin
def _(access_level, user_id):
    user = User.from_user_id(user_id)
    if user:
        tweets = user.get_feed()
        response.status = 200
        return json.dumps(tweets)
    else:
        error = create_error_dict(400, "User not found")
        response.status = 400
        return json.dumps(error)
   
############################################################
@post("/users")
def _():
    try:
        user_email = v.EmailValidation(request.forms.get("user_email")).validate()
        user_name = v.UserNameValidation(request.forms.get("user_name")).validate()
        user_first_name = v.UserNameValidation(request.forms.get("user_first_name")).validate()
        user_last_name = v.UserNameValidation(request.forms.get("user_last_name")).validate()
        user_password = v.PasswordValidation(request.forms.get("user_password")).validate()
        user_password_again = v.PasswordValidation(request.forms.get("user_password_again")).validate()
    except Exception as e:
        error = create_error_dict(401, str(e))
        response.status = 401
        return json.dumps(error)
    ###
    #Validate inputs

    if is_user_data_already_in_use("user_email", user_email):
        error = create_error_dict(message=f"{user_email} is already in use. Try resetting your password")
        response.status = 401
        return json.dumps(error)

    if is_user_data_already_in_use("user_name", user_name):
        error = create_error_dict(message=f"{user_name} is already in use.")
        response.status = 401
        return json.dumps(error)
    
    if user_password != user_password_again:
        response.status = 401
        error = create_error_dict(message="Passwords don't match. Try entering them again")
    
    #create User instance
    new_user = User(user_name, user_first_name, user_last_name, user_email, user_password)
    #save user/ create user entry
    new_user.create_user()
    response.status = 200
    #return user dict without sensitive information
    return json.dumps(new_user.get_client_user())

############################################################
@put("/users/<user_id>")
@requires_auth_or_admin
def _(access_level):
    #get and validate user inputs
    try:
        user_email = v.EmailValidation(request.forms.get("user_email")).validate()
        user_name = v.UserNameValidation(request.forms.get("user_name")).validate()
        user_first_name = v.UserNameValidation(request.forms.get("user_first_name")).validate()
        user_last_name = v.UserNameValidation(request.forms.get("user_last_name")).validate()
        user_password = v.PasswordValidation(request.forms.get("user_password")).validate()
        user_password_again = v.PasswordValidation(request.forms.get("user_password_again")).validate()
    except Exception as e:
        error = create_error_dict(401, str(e))
        response.status = 401
        return json.dumps(error)

    if is_user_data_already_in_use("user_email", user_email):
        error = create_error_dict(message=f"{user_email} is already in use. Try resetting your password")
        response.status = 401
        return json.dumps(error)

    if is_user_data_already_in_use("user_name", user_name):
        error = create_error_dict(message=f"{user_name} is already in use.")
        response.status = 401
        return json.dumps(error)
    
    if user_password != user_password_again:
        response.status = 401
        error = create_error_dict(message="Passwords don't match. Try entering them again")
    
    try:
    #create User instance
        new_user = User(user_name, user_first_name, user_last_name, user_email, user_password)
        #save user/ create user entry
        new_user.create_user()
    except Exception as e:
        error = create_error_dict(400, str(e))
        response.status = 400
        return json.dumps(error)

    #return user dict without sensitive information
    response.status = 200
    return json.dumps(new_user.get_client_user())

