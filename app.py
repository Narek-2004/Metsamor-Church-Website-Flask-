from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from time import sleep


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(40), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def posts():
    articles = Article.query.order_by(Article.date).all()
    return render_template('index.html', articles=articles)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        book = request.form['book-name']
        text = request.form['chapter']

        article = Article(book=book, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)