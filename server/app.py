#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles', methods = ['GET'])
def index_articles():
    articles = Article.query.all()

    articles_dict = articles.to_dict()
    return make_response(
        articles_dict, 200
    )

@app.route('/articles/<int:id>', methods = ['GET'])
def show_article(id):
    session['page_views'] = 1 if 'page_views' not in session else session['page_views'] + 1
    if session['page_views'] <= 3:
        # Retrieve the article from the database
        article = Article.query.filter(Article.id ==id).first()
        
        if article:
            return jsonify({
                'id': article.id,
                'author': article.author,
                'title': article.title,
                'content': article.content,
                'preview': article.preview,
                'minutes_to_read': article.minutes_to_read,
                'date': article.date,
                'page_views': session['page_views']
            })
        else:
            return {'message': 'Article not found'}, 404
    else:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    

if __name__ == '__main__':
    app.run(port=5555)
