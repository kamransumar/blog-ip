from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
# from wtforms.validators import Required, Email, EqualTo
from ..models import User
from wtforms import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class UpdateProfile(FlaskForm):
    username = TextAreaField('enter username')
    submit = SubmitField('Submit')


class BlogForm(FlaskForm):
    title = TextAreaField('enter title')
    content = TextAreaField('type your blog')

    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    content = TextAreaField('comment')
    submit = SubmitField('Submit')
