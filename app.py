import os

from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

from api_utils import translate_text
from forms import DeckForm, CardForm
from models import db, Deck, Card

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/img/cards'

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    decks = Deck.query.all()
    return render_template('index.html', decks=decks)


@app.route('/deck/new', methods=['GET', 'POST'])
def new_deck():
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck(title=form.title.data, description=form.description.data,
                    is_public=form.is_public.data, user_id=1)
        db.session.add(deck)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('deck_form.html', form=form)


@app.route('/deck/<int:deck_id>/add_card', methods=['GET', 'POST'])
def add_card(deck_id):
    form = CardForm()
    if request.method == 'POST' and not form.answer.data:
        form.answer.data = translate_text(form.question.data)

    if form.validate_on_submit():
        image_file = ""
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_file = filename

        card = Card(question=form.question.data, answer=form.answer.data,
                    image_path=image_file, deck_id=deck_id)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('card_form.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
