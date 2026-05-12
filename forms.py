from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Создать аккаунт')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class DeckForm(FlaskForm):
    title = StringField('Название колоды', validators=[DataRequired()])
    description = TextAreaField('Описание (необязательно)')
    is_public = BooleanField('Сделать публичной')
    submit = SubmitField('Сохранить')

class CardForm(FlaskForm):
    question = StringField('Слово или вопрос', validators=[DataRequired()])
    answer = StringField('Перевод или ответ', validators=[DataRequired()])
    image = FileField('Добавить картинку', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Готово')