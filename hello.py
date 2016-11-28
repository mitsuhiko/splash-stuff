import click
import random
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('hello.cfg')
db = SQLAlchemy(app)

from raven.contrib.flask import Sentry
sentry = Sentry(app, dsn='https://6a7935a211ef47efa902125bb86174f5:3165dde52f6545d4826c02e896d5cb74@sentry.io/117852')

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    contents = db.Column(db.String)
    pub_date = db.Column(db.DateTime)

@app.cli.command()
def initdb():
    """Initialize database"""
    db.create_all()

@app.cli.command()
@click.confirmation_option(help='Are you sure you want to drop the db?')
def dropdb():
    """Drop database"""
    db.drop_all()

@app.route('/')
def index():
    return render_template('index.html', name=random.choice(
        ['Warchest', 'Fireteam', 'Splash Damage']))

@app.route('/new', methods=['GET', 'POST'])
def new_paste():
    if request.method == 'POST':
        paste = Paste(title=request.form['title'],
                      contents=request.form['contents'])
        db.session.add(paste)
        db.session.commit()
        1/0
        return redirect(url_for('show_paste', paste_id=paste.id))
    return render_template('new.html')

@app.route('/paste/<int:paste_id>')
def show_paste(paste_id):
    paste = Paste.query.get_or_404(paste_id)
    return render_template('show.html', paste=paste)

@app.errorhandler(404)
def not_found(error):
    return Response(render_template('not_found.html'), status=404)
