from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'engage.db')
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "thisisasecretkey"

login_manager = LoginManager(app)
login_manager.login_view = 'index'

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.template_filter('time_since')
def time_since(delta):
    seconds = delta.total_seconds()
    
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)
    if years > 0:
        return "%dy" % years
    elif months > 0:
        return "%dm" % months
    elif days > 0:
        return "%dd" % days
    elif hours > 0:
        return "%dh" % hours
    elif minutes > 0:
        return "%dm" % minutes
    else:
        return "Just now!"
    
from views import *

if __name__ == "__main__":
    app.run(debug=True)