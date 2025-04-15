from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Article {self.id}>'
@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/create_article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При додаванні статті виникла помилка"
    else:
        return render_template("create_article.html")
@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'Hello {name}! your id is {id}'

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del')
def delete_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При видаленні виникла помилка"


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редагуванні статті виникла помилка"
    else:
        return render_template("post_update.html", article=article)









@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)
