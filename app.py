from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.q7dgkca.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


#대문 페이지
@app.route('/')
def home():
   return render_template('index.html')

# index.html line 90에서  /movie로 보낸것을 받음
@app.route("/movie", methods=["POST"]) #/movie로 받음

def movie_post():
   url_receive = request.form['url_give']
   comment_receive = request.form['comment_give']
   star_receive = request.form['star_give']

   headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
   data = requests.get(url_receive,headers=headers)
   soup = BeautifulSoup(data.text, 'html.parser')
 
   ogtitle = soup.select_one('meta[property="og:title"]')['content']
   ogdesc = soup.select_one('meta[property="og:description"]')['content']
   ogimage = soup.select_one('meta[property="og:image"]')['content']

   doc = {
      'title' : ogtitle,
      'desc' : ogdesc,
      'image' : ogimage,
      'comment' : comment_receive,
      'star' : star_receive
   }

   db.movies.insert_one(doc)

   return jsonify({'msg':'저장완료!'})


#글보기(메인) 페이지
@app.route('/main')
def main():
   return render_template('main.html')

@app.route("/movie", methods=["GET"])
def movie_get():
    all_movies = list(db.movies.find({},{'_id':False}))
    return jsonify({'result':all_movies})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5002, debug=True)