from bottle import request, response
from models.user_model import User
from helpers.function_helpers import create_error_dict
import json

##############################
def requires_auth_or_admin(func): #func param is the function that's after the decorator
    #Creates authetication decorator for routes, requires authentication token in "Authorization" header
    def decorated(*args, **kwargs):        
        #get auth cookie from request
        session_id = request.get_cookie("token")
        #check if user is in session
        is_in_session = User.is_in_session(session_id)
        #return error if not in session
        if not is_in_session:
            error = create_error_dict(401, "Unauthorized, login and try again")
            response.status = 401
            return json.dumps(error)

        #if authenticated get user access level
        user = User.from_session_id(session_id)
        access_level = user.access_level
        #pass the access_level to the function that's wrapper by the decorator (the anonym function handling the route logic)
        kwargs['access_level'] = access_level
        return func(*args, **kwargs)
 
    return decorated