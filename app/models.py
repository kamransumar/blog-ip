from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.column(db.String(30))
    username = db.Column(db.String(255))
    image = db.Column(db.String,  default='default.jpg')
    email = db.Column(db.String(30))
    pass_secure = db.Column(db.String(255))
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='comment', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.id}, {self.name}, {self.username}, {self.image}, {self.email}, {self.blogs}, {self.comment}'


class Comment(db.Model, UserMixin):
    __tablename__ = 'comments'

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    id = db.Column(db.Integer, primary_key=True)
    ratings = db.Column(db.Integer)
    like = db.Column(db.Integer)
    dislike = db.Column(db.Integer)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    def __repr__(self):
        return f'Comment {self.id}, {self.ratings}, {self.like}, {self.dislike}, {self.content}'


class Blog(db.Model, UserMixin):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    comments_id = db.relationship(
        'Comment', backref='comments', lazy='dynamic')
    time = db.Column(db.DateTime)

    def __repr__(self):
        return f'Blog {self.id}, {self.category}, {self.title}, {self.author}, {self.content}, {self.comment}'
