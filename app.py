import os

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from api_utils import translate_text
from forms import RegisterForm, LoginForm, DeckForm, CardForm
from models import db, User, Deck, Card

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartcards.db'
app.config['UPLOAD_FOLDER'] = 'static/img/cards'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Пожалуйста, войдите, чтобы получить доступ к этой странице."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('base.html', content="Ошибка 404: Страница не найдена"), 404


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        flash('Неверный логин или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
def index():
    if current_user.is_authenticated:
        decks = Deck.query.filter_by(user_id=current_user.id).all()
    else:
        decks = Deck.query.filter_by(is_public=True).all()
    return render_template('index.html', decks=decks)


@app.route('/deck/new', methods=['GET', 'POST'])
@login_required
def new_deck():
    form = DeckForm()
    if form.validate_on_submit():
        deck = Deck(title=form.title.data, description=form.description.data,
                    is_public=form.is_public.data, user_id=current_user.id)
        db.session.add(deck)
        db.session.commit()
        flash('Колода создана!', 'success')
        return redirect(url_for('index'))
    return render_template('deck_form.html', form=form, title="Новая колода")


@app.route('/deck/<int:deck_id>')
def view_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if not deck.is_public and (not current_user.is_authenticated or deck.user_id != current_user.id):
        abort(403)
    return render_template('view_deck.html', deck=deck)


@app.route('/deck/<int:deck_id>/add_card', methods=['GET', 'POST'])
@login_required
def add_card(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        abort(403)
    form = CardForm()
    translate_word = request.args.get('question')
    if request.args.get('auto_translate') and translate_word:
        form.question.data = translate_word
        form.answer.data = translate_text(translate_word)
    if form.validate_on_submit():
        image_name = None
        if form.image.data:
            f = form.image.data
            image_name = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        card = Card(question=form.question.data, answer=form.answer.data,
                    image_path=image_name, deck_id=deck_id)
        db.session.add(card)
        db.session.commit()
        return redirect(url_for('view_deck', deck_id=deck_id))

    return render_template('card_form.html', form=form, deck=deck)


@app.route('/card/<int:card_id>/delete')
@login_required
def delete_card(card_id):
    card = Card.query.get_or_404(card_id)
    if card.deck.user_id != current_user.id:
        abort(403)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('view_deck', deck_id=card.deck_id))


@app.route('/api/v1/my_decks')
@login_required
def api_my_decks():
    decks = Deck.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        "id": d.id,
        "title": d.title,
        "cards_count": len(d.cards),
        "created_at": d.created_at.isoformat()
    } for d in decks])


@app.route('/deck/<int:deck_id>/delete', methods=['POST'])
@login_required
def delete_deck(deck_id):
    deck = Deck.query.get_or_404(deck_id)
    if deck.user_id != current_user.id:
        abort(403)
    db.session.delete(deck)
    db.session.commit()
    flash(f'Колода "{deck.title}" успешно удалена', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        db.create_all()
    app.run(debug=True)
