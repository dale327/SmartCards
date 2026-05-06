from flask import Flask
from models import db, User, Deck, Card

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartcards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "База данных и модели успешно инициализированы"

if __name__ == '__main__':
    app.run(debug=True)