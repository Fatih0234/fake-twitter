from app import db, login_manager
from flask_login import UserMixin


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followee_id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100))
    username = db.Column(db.String(30))
    image = db.Column(db.String(100))
    password = db.Column(db.String(100))
    join_date = db.Column(db.DateTime)
    
    # tweets = db.relationship('Tweet', backref='user', lazy='dynamic')
    # with this relationship, we can access the tweets of a user by using user.tweets
    # and we can access the user of a tweet by using tweet.user
    
    following = db.relationship('User', secondary=followers, # => middle table
        primaryjoin=(followers.c.follower_id == id), # from left table to middle
        secondaryjoin=(followers.c.followee_id == id), # from middle to right table
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') # user->followed->followers
    
    followed_by = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.followee_id == id), # from left table to middle
        secondaryjoin=(followers.c.follower_id == id), # from right table to middle
        backref=db.backref('followed', lazy='dynamic'), lazy='dynamic') # user->followers->followed
    
    

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('tweets', lazy='dynamic'))
    created_at = db.Column(db.DateTime)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))