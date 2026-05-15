from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(message="Введите логин"),
        Length(min=3, max=20, message="Логин должен быть от 3 до 20 символов")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Введите адрес электронной почты"),
        Email(message="Некорректный формат почты")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль"),
        Length(min=6, message="Пароль должен быть не менее 6 символов")
    ])
    confirm_password = PasswordField('Повторите пароль', validators=[
        DataRequired(message="Подтвердите пароль"),
        EqualTo('password', message="Пароли должны совпадать")
    ])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(message="Введите логин")
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Введите пароль")
    ])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DeckForm(FlaskForm):
    title = StringField('Название колоды', validators=[
        DataRequired(message="Название обязательно для заполнения"),
        Length(max=100, message="Слишком длинное название")
    ])
    description = TextAreaField('Описание')
    is_public = BooleanField('Сделать колоду доступной всем')
    submit = SubmitField('Сохранить колоду')


class CardForm(FlaskForm):
    question = StringField('Слово / Вопрос', validators=[
        DataRequired(message="Введите вопрос или слово")
    ])
    answer = StringField('Перевод / Ответ', validators=[
        DataRequired(message="Введите ответ или перевод")
    ])
    image = FileField('Изображение', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message="Допускаются только изображения (jpg, png)")
    ])
    submit = SubmitField('Сохранить карточку')
