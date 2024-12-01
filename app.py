from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  #создаём приложение
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/test'  #ссылка для подключения
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  #передаём приложение


# Таблицы для базы данных
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    post = db.relationship('Post', backref=db.backref('comments', lazy=True))


with app.app_context():
    db.create_all()


@app.route('/') #создаем главную страницу
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])  #добавление пользователя в таблицу
def add_post():
    if request.method == 'POST':
        title_form = request.form['title']
        content_form = request.form['content']
        new_post = Post(title=title_form, content=content_form)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_post.html')


@app.route('/post/<int:post_id>', methods=['GET', 'POST']) #ввод данных, если не верные выводится 404
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        comment_text = request.form['content']
        new_comment = Comment(content=comment_text, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('view_post.html', post=post)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')