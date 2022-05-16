import re

############################################################
class EmailValidation:
    def __init__(self, email = None):
        self.email = email

    def validate(self):
        #Check if exists, if not raise Exception
        if not self.email: raise Exception("Email is required")
        
        #Check for right pattern
        email_regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        if not re.match(email_regex, self.email): raise Exception("Email is required and must be a valid email address")

        #if everything is correct, return the value
        return self.email

############################################################
class UuidValidation:
    def __init__(self, uuid = None):
        self.uuid = uuid

    def validate(self):
        #Check if exists, if not raise Exception
        if not self.uuid: raise Exception("uuid is required")
        
        #Check if right pattern, if not raise Exception
        regex_uuid4 = "^[0-9a-f]{8}-[0-9a-f]{4}-[4][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
        if not re.match(regex_uuid4, self.uuid): raise Exception("Invalid uuid formatting. uuid must follow the standard formatting")

        #if everything is correct, return the value
        return self.uuid

############################################################
class UserNameValidation:
    def __init__(self, name = None):
        self.name = name

    def validate(self):
        #Check if exists, if not raise Exception
        if not self.name: raise Exception("Names are required")

        min_length, max_length = 2, 25
        #Check min length
        if not len(self.name) >= min_length: raise Exception(f"Names must be at lest {min_length} charachters long")

        #Check max length
        if not len(self.name) <= max_length: raise Exception(f"Names must be maximum {max_length} charachters long")

        #Check if includes not unicode charachters (numbers, punctuations etc but allow special charachters like accented letters)
        name_regex = "[^\W\d_]"
        if not re.match(name_regex, self.name): raise Exception("Names must only include letters. No numbers or punctiations allowed")

        #if everything is correct, return the value
        return self.name
        
############################################################
class PasswordValidation:
    def __init__(self, password):
        self.password = password

    def validate(self):
        #Check if exists, if not raise Exception
        if not self.password: raise Exception("Password required")

        #Check for length (allowing long input to accomodate password manager passwords)
        min_length, max_length = 1, 120

        #Check min length
        if not len(self.password) >= min_length: raise Exception(f"Password must be at lest {min_length} charachters long")

        #Check max length
        if not len(self.password) <= max_length: raise Exception(f"Password must be maximum {max_length} charachters long")

        #if everything is correct, return the value
        return self.password

############################################################
class TweetValidation:
    def __init__(self, tweet):
        self.tweet = tweet

    def validate(self):
        #Check if exists, if not raise Exception
        if not self.tweet: raise Exception("Tweet description is requried")

        #Check for length (allowing very short input to accomodate short tweet descriptions fx 1 emoji)
        min_length, max_length = 1, 240

        #Check min length
        if not len(self.tweet) >= min_length: raise Exception(f"Tweet descripitons must be at lest {min_length} charachters long")

        #Check max length
        if not len(self.tweet) <= max_length: raise Exception(f"Tweet descriptions must be maximum {max_length} charachters long")

        #If everything is correct, return the value
        return self.tweet

##might not need it
class JWTTokenValidation:
    def __init__(self, token):
        self.token = token