from flask import render_template, request, redirect, url_for, abort 
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, photos
from models import User, Tweet, followers
from forms import LoginForm, RegisterForm, TweetForm
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


@app.route('/', methods= ['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form, logged_in_user = current_user)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    
    if request.method == "GET":
        return redirect(url_for('index'))
   
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user:
            return render_template('index.html', form=form, message="Invalid username or password")
        if check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('profile'))
        
        return "<h1>Invalid username or password</h1>"
    
    return redirect(url_for('index'))
        
        
        
@app.route("/profile/", defaults={"username": None})
@app.route("/profile/<username>")
def profile(username):
    
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
    else:
        user = current_user
    user_id = user.id
    current_time = datetime.now()
    tweets = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.created_at.desc()).all()
    
    followed_by = user.followed_by.all()
    
    display_follow = True
    
    if  current_user == user:
        display_follow = False
    elif current_user in followed_by:
        display_follow = False
        
    # let's create who to follow
    
    who_to_watch = User.query.filter(User.id != user_id).order_by(db.func.random()).limit(4).all()
    
    return render_template('profile.html', current_user=user, current_time=current_time, tweets=tweets, followed_by=followed_by, display_follow=display_follow, who_to_watch=who_to_watch, logged_in_user = current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
@app.route("/timeline/", defaults={"username": None})
@app.route("/timeline/<username>")
def timeline(username):
    form = TweetForm()
    
    if username:
        user = User.query.filter_by(username=username).first()
        if not user:
            abort(404)
        user_id = user.id
        tweets = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.created_at.desc()).all()
        total_tweets = len(tweets)
    else: 
        user = current_user
        user_id = current_user.id
        tweets = Tweet.query.join(followers, (followers.c.followee_id == Tweet.user_id)).filter(followers.c.follower_id == user_id).order_by(Tweet.created_at.desc()).all()
    
    total_tweets = user.tweets.count()
    current_time = datetime.now()
    
    who_to_watch = User.query.filter(User.id != user_id).order_by(db.func.random()).limit(4).all()
    total_subscribers = user.followed_by.count()
    return render_template('timeline.html', form=form, current_user=user, tweets=tweets, current_time=current_time, total_tweets=total_tweets, who_to_watch=who_to_watch, logged_in_user = current_user, total_subscribers=total_subscribers)

@app.route("/post_tweet", methods=['POST'])
@login_required
def post_tweet():
    form = TweetForm()
    
    if form.validate():
        new_tweet = Tweet(text=form.text.data, user_id=current_user.id, created_at=datetime.now())
        db.session.add(new_tweet)
        db.session.commit()
        return redirect(url_for('timeline'))
        
    return redirect(url_for('timeline'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        image_filename = photos.save(form.image.data)
        image_url = photos.url(image_filename)
        new_user = User(name=form.name.data, username=form.username.data, password=generate_password_hash(form.password.data), image=image_url, join_date=datetime.now())
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        return redirect(url_for('profile'))
    
    return render_template('register.html', form=form, logged_in_user = current_user)


@app.route("/follow/<username>")
@login_required
def follow(username):
    user_to_follow = User.query.filter_by(username=username).first()
    current_user.following.append(user_to_follow)
    db.session.commit()
    return redirect(url_for('profile', username=username))