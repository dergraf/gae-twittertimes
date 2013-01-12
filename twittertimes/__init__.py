from flask import Flask
import settings

app = Flask('app')
app.config.from_object('twittertimes.settings')

import views
