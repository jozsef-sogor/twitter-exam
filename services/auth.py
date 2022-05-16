from bottle import get, post, request, response
from helpers import validation_helpers as v
from helpers.function_helpers import is_user_data_already_in_use, create_error_dict
from g import _SESSIONS, FORGOT_PW_EMAIL, JWT_SECRET, PASSWORD_RESET_EXPIRY_TIME_SECONDS, SESSION_COOKIE_MAX_AGE_SECONDS, IMG_BASE_URL
from models.user_model import User
from models.email_model import Email
from datetime import datetime, timezone, timedelta
from services import file_upload
import json
import jwt

##############################
@post("/login")
def _():
    #get sesion token if any
    existing_session_id = request.get_cookie("token")
    print(existing_session_id)
    #check if token already in session
    if existing_session_id:
        is_already_logged_in = User.is_in_session(existing_session_id)
        if is_already_logged_in:
            user = User.from_session_id(existing_session_id)
            #error = create_error_dict(401, "User already logged in")
            return json.dumps(user.get_client_user())

    #get user inputs from login form and validate
    try:
        user_email = v.EmailValidation(request.forms.get("user_email")).validate()
        user_password = v.PasswordValidation(request.forms.get("user_password")).validate()
    except Exception as e:
        error = create_error_dict(401, str(e))
        response.status = 401
        return json.dumps(error)

    #create User isntance from email
    user = User.from_email(user_email)

    #check credentials and return errors if any
    if not user:
        error = create_error_dict(401, f"User with email {user_email} not found. Try registering instead")
        response.status = 401
        return json.dumps(error)
    if user.user_password != user_password:
        error = create_error_dict(401, "Wrong password")
        response.status = 401
        return json.dumps(error)

    #if everythings matches add user to session
    session_id = user.add_to_session()
    #create and set session_id cookie
    cookie_opts = {
        'max_age': SESSION_COOKIE_MAX_AGE_SECONDS,
        'httponly': True,
        'samesite': 'Lax'
    }
    response.set_cookie("token", session_id, **cookie_opts)
    response.status = 200
    #return the user stripped from sensitive data like password
    return json.dumps(user.get_client_user())

##############################
@post("/logout")
def _():
    session_id = request.get_cookie("token")
    #check if user is in session
    is_in_session = User.is_in_session(session_id)
    #if yes, remove it and delete cookie
    if is_in_session:
        User.remove_from_session(session_id)
        response.delete_cookie("token")
        response.status = 200
        return
    else:
        error = create_error_dict(message="User not logged in")
        return json.dumps(error)

##############################
@post("/register")
def _():
    try:
        user_email = v.EmailValidation(request.forms.get("user_email")).validate()
        user_name = v.UserNameValidation(request.forms.get("user_name")).validate()
        user_first_name = v.UserNameValidation(request.forms.get("user_first_name")).validate()
        user_last_name = v.UserNameValidation(request.forms.get("user_last_name")).validate()
        user_image = request.files.get("user_image")
        user_image_url = None
        user_password = v.PasswordValidation(request.forms.get("user_password")).validate()
        user_password_again = v.PasswordValidation(request.forms.get("user_password_again")).validate()
        print(user_image)

        if user_image:
            user_image_url = file_upload.upload_image(user_image)
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
        return json.dumps(error)

    #create User instance
    new_user = User(user_name, user_first_name, user_last_name, user_email, user_password, user_image=f"{IMG_BASE_URL}{user_image_url}")
    #save user/ create user entry
    new_user.create_user()
    #create the session for user
    session_id = new_user.add_to_session()
    #create and set session_id cookie
    cookie_opts = {
        'max_age': SESSION_COOKIE_MAX_AGE_SECONDS,
        'httponly': True,
        'samesite': 'Lax'
    }
    response.set_cookie("token", session_id, **cookie_opts)
    response.status = 200
    #return user dict without sensitive information
    return json.dumps(new_user.get_client_user())

##############################
@post("/forgot-password")
def _():
    try:
        user_email = v.EmailValidation(request.forms.get("user_email")).validate()
        print(user_email)
    except Exception as e:
        error = create_error_dict(401, str(e))
        response.status = 401
        return json.dumps(error)

    #check if email is infact in use
    if is_user_data_already_in_use("user_email", user_email):
        #get user by email
        user = User.from_email(user_email)
        # generate JWT with user inside
        exp_time = datetime.now(tz=timezone.utc) + timedelta(seconds=PASSWORD_RESET_EXPIRY_TIME_SECONDS)
        encoded_jwt = jwt.encode({**user.get_client_user(), "exp": exp_time}, JWT_SECRET, algorithm="HS256").decode('utf-8')

        #create email tempalte with JWT in link
        email_as_text = """\
            Hi,
            To reset your password visit the link below. The link is valid for 15 minutes, after that you need to request a new email.

            """ + f"{IMG_BASE_URL}?token={encoded_jwt}#ResetPasswordModal"

        email_as_html = """\
            <html>
                <body>
                <p>
                    Hi,<br>
                    To reset your password visit the link below. The link is valid for 15 minutes, after that you need to request a new email.
                </p>
            """ + f'<a target="_blank" href="{IMG_BASE_URL}?token={encoded_jwt}#ResetPasswordModal">{IMG_BASE_URL}?token={encoded_jwt}#ResetPasswordModal</a>' + """\
                </body>
            </html>
            """
        #send email
        new_email = Email(FORGOT_PW_EMAIL, user_email, f"Forgot password for email {user_email}", email_as_text, email_as_html)
        is_sent = new_email.send_email()
    else:
        print("email isn't used")

    #always send back success respond if there were no server erros
    #to prevent people gessing what emails might othet people use
    token_to_send = str(encoded_jwt) if encoded_jwt else None
    response.status = 200
    return json.dumps({"msg": "If the email has associted account and email was sent with instructions on how to reset your password.", "token_for_testing": token_to_send})

##############################
@post("/reset-password")
def _():
    jwt_token = request.query.token
    #if valid token, get email from token and update user with new password
    try:
        #validate token
        client_user_dict = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
        #validate user inputs
        user_password = v.PasswordValidation(request.forms.get("user_password")).validate()
        user_password_again = v.PasswordValidation(request.forms.get("user_password_again")).validate()
        if user_password != user_password_again: raise Exception("Passwords don't match")
    except Exception as e:
        error = create_error_dict(401, str(e))
        response.status = 401
        return json.dumps(error)

    user_email = client_user_dict["user_email"]
    user = User.from_email(user_email)
    user.user_password = user_password

    try:
        user.update_user(user.__dict__)
    except Exception as e:
        error = create_error_dict(400, str(4))
        response.status = 400
        return json.dumps({error})

    #create the session for user
    session_id = user.add_to_session()
    #create and set session_id cookie
    cookie_opts = {
        'max_age': SESSION_COOKIE_MAX_AGE_SECONDS,
        'httponly': True,
    }
    response.set_cookie("token", session_id, **cookie_opts)
    response.status = 200
    #return user dict without sensitive information
    return json.dumps(user.get_client_user())

##############################
@get("/get-users")
def _():
    users = User.get_all_users()
    return json.dumps(users)

##############################
@get("/get-sessions")
def _():
    return json.dumps(_SESSIONS)


