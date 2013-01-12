from google.appengine.ext import db

class TwitterUser(db.Model):
    handle = db.StringProperty(required=True)
    oauth_token = db.StringProperty(required=True)
    oauth_token_secret = db.StringProperty(required=True)

