from bottle import app, default_app, run, route, get, static_file, post, request, response
from bottle_cors_plugin import cors_plugin
from services import auth, users, tweets
from g import IMG_BASE_URL
import json
import uuid 


##############################
#serve static images
@get("/assets/img/<image_name>")
def _(image_name):
    print(image_name)
    return static_file(image_name, root="./assets/img")

##############################
# @get("/views/vue_app/<file_name>")
# def _(file_name):
#     return static_file(file_name, root="./views/vue_app")


# ##############################
# @get("/views/vue_app/assets/<file_name>")
# def _(file_name):
#     return static_file(file_name, root="./views/vue_app/assets")

##############################
#route to catch all uncaught routes before and provide it 
#to the Vue FE application where the routing is handled client-side
# @route('<mypath:path>')
# def _(mypath):
#     return static_file("index.html", root="./views/vue_app")




##############################
@post("/test")
def _():
    my_name = request.forms.get("my_name")
    dict = {
        "id": str(uuid.uuid4()),
        "name": my_name
    }
    response.content_type = "application/json"
    return json.dumps(dict)

##############################
##############################
##############################
##############################
##############################
##############################
try:
    import production
    application = default_app()
except:
    #Enable cors for development
    #during development the Frontend app runs on different port, CORS has to be enabled
    #NOTE: CORS cookies might be disabled by the browser, to test POST, DELETE etc requests locally 
    #run npm run preview, this will create a dev build in the specified folder that is picked up by bottle and it returns the index.html (on bottle's port)
    from helpers.EnableCors import EnableCors
    app = app()
    app.install(EnableCors())
    
    run(host="127.0.0.1", port="3333", debug="True", reloader="True")