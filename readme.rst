Twitter Times - Authenticated Timeline Access
=============================================

Login:
------
http://tlinkstimeline.appspot.com/login 
use this link within the official "Sign in with Twitter"-Button
if user has not yet granted access to the Twitter Times App, he'll get redirected to a Twitter authorization page

Logout:
-------
http://tlinkstimeline.appspot.com/logout
use this link within a "logout from Twitter Times"-Button
This will clear the User session, and user must Login again (it is not necessary to grant access again)

Already Logged In?:
-------------------
http://tlinkstimeline.appspot.com/loggedin?callback=xyz
use this call to figure out if a user already has a valid session. (e.g. for presenting proper "signIn/signOut"-Buttons)

Statuses:
---------
http://tlinkstimeline.appspot.com/statuses/*
All Twitter API GET Requests that require User Context such as e.g. home_timeline
http://tlinkstimeline.appspot.com/statuses/home_timeline.json

pass the same options as described in https://dev.twitter.com/docs/api/1.1

Limited to Twitter API GET Requests at the moment



Example:
--------
.. code-block:: javascript

  var isAuthorized = false;
  $.getJSON("http://tlinkstimeline.appspot.com/loggedin?callback=?", function(isLoggedIn){
    if (isLoggedIn) {
      isAuthorized = true;
      // show logout button <a href="http://tlinkstimeline.appspot.com/logout">Sign out</a>
    } else {
      isAuthorized = false;
      // show login button <a href="http://tlinkstimeline.appspot.com/login">Sign in with Twitter</a>
    }
  });

  $("#fetchHomeTimelineButton").click(function() {
    if (isAuthorized) {
      var params = {
        'screen_name': myInput,
        'include_entities': true,
        'include_rts': false,
        'since_id': 1,
        'count' : tweetsToFetch,
      };
      $.getJSON("http://tlinkstimeline.appspot.com/statuses/home_timeline.json", params, function(data) {
        // processData(data);
      });
    } else {
      // tell the user to login
    }
  });
