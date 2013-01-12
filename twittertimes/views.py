from twittertimes import settings
from twittertimes import app
from twittertimes.decorators import jsonp
from models import TwitterUser
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import flash
from flask import session
from flask import Response


from flask_oauth import OAuth, OAuthException
from google.appengine.ext import db
from flask import request, current_app

oauth = OAuth()

twitter = oauth.remote_app('twitter',
        base_url='https://api.twitter.com/1/',
        request_token_url='https://api.twitter.com/oauth/request_token',
        access_token_url='https://api.twitter.com/oauth/access_token',
        authorize_url='https://api.twitter.com/oauth/authenticate',
        consumer_key=settings.TWITTER_CONSUMER_KEY,
        consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        )

@app.route('/')
def index():
    return render_template('index.html')


@twitter.tokengetter
def get_twitter_token(token=None):
    handle = session.get('twitter_handle')
    user = get_user(handle)
    if user:
        return (user.oauth_token, user.oauth_token_secret)
    else:
        return None

@app.route('/login')
def login():
    if not session.get('twitter_handle'):
        return twitter.authorize(callback=url_for('oauth_authorized',
            next=request.args.get('next') or request.referrer or None))
    else:
        next_url = request.args.get('next') or url_for('index')
        return redirect(next_url)

@app.route('/logout')
def logout():
    next_url = request.args.get('next') or url_for('index')
    session.clear()
    return redirect(next_url)

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    user = get_user(resp['screen_name'])
    if user:
        user.oauth_token=resp['oauth_token']
        user.oauth_token_secret=resp['oauth_token_secret']
    else:
        user = TwitterUser(
            handle=resp['screen_name'],
            oauth_token=resp['oauth_token'],
            oauth_token_secret=resp['oauth_token_secret'])

    user.put()
    session['twitter_handle'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route('/statuses/<resource>')
def timeline(resource='home_timeline.json'):
    next_url = request.args.get('next') or url_for('index')
    data = request.args.copy()
    try:
        del data['next']
    except KeyError:
        pass

    resp = twitter.get('statuses/' + resource, data=data)
    if resp.status == 200:
        tweets = resp.data
        resp = Response(tweets, status=200, mimetype='application/json')
        return resp
    else:
        return resp

@app.route('/loggedin')
@jsonp
def loggedin():
    if session.get('twitter_handle'):
        resp = Response("true", status=200, mimetype='application/json')
        return resp
    else:
        resp = Response("false", status=200, mimetype='application/json')
        return resp

@app.errorhandler(OAuthException)
def handle_oauth_exception(error):
    resp = Response(error, status=403)
    return resp


### UTILITY FUNCTIONS ###
def get_user(handle):
    query = db.GqlQuery("SELECT * FROM TwitterUser WHERE handle = :1", handle)
    return query.get()
