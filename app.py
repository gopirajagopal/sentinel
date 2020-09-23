# coding: utf-8

from datetime import datetime, timedelta
from flask import Flask
from flask import session, request
from flask import render_template, redirect, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider
from werkzeug.utils import cached_property
import os
from datetime import date
import re

app = Flask(__name__, template_folder='templates')
app.debug = True
app.secret_key = 'secret'
app.config["MONGO_URI"] = "mongodb://122.164.172.238:27017/SentinelInterview"
mongo = PyMongo(app)
oauth = OAuth2Provider(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/loaddata')
def upload(): 
    for file in os.listdir("C:/Gopi/video"):
        with open("C:/Gopi/video/"+file,  "rb") as f:
            mongo.save_file(file,f)
            mongo.db.VideoInfo.insert({'title': 'Trump Speaking about star wars','CreatedBy':'Gopinath','fileName':file,'description':'Trump was speaking about star wars and and darth vador','source':'instagram','source_url':'https://www.instagram.com/p/CEUlGY4DdWA/','CreatedDt':str(date.today())})
    return render_template('home.html'), 200




@app.route('/')
def index():   
    return render_template('home.html'), 200

    

@app.route('/search', methods = ['post'])
def search_videos():   
    parameter = request.get_json()
    queryParam={}
    if(parameter['searchDate']!=''):
        queryParam['CreatedDt'] = parameter['searchDate']
    if(parameter['createdBy'] != ''):
         queryParam['CreatedBy'] = parameter['createdBy']
    if(parameter['title'] != ''):
         pattern = re.compile(parameter['title'], re.I)
         queryParam['title'] = pattern
    if(parameter['description'] != ''):
         pattern = re.compile(parameter['description'], re.I)
         queryParam['description'] = pattern
    info = mongo.db.VideoInfo.find(queryParam)
    video_object =[]
    for file in info:
        video={}
        video['title']=file['title']
        video['description']=file['description']
        video['source_url']=file['source_url']
        video['source']=file['source']
        video['CreatedDt']=file['CreatedDt']
        video['CreatedBy']=file['CreatedBy']
        video['fileName']=file['fileName']
        video['url']='http://localhost:5000/streamvideo/'+file['fileName']
        video_object.append(video)
    return jsonify(video_object), 200




@app.route('/streamvideo/<filename>')
def stream_file(filename):   
    return mongo.send_file(filename)




@app.route('/getvideos/<date>')
def get_videos(date):   
    info = mongo.db.VideoInfo.find({'CreatedDt':date})
    video_object =[]
    for file in info:
        video={}
        video['title']=file['title']
        video['description']=file['description']
        video['source_url']=file['source_url']
        video['source']=file['source']
        video['CreatedDt']=file['CreatedDt']
        video['CreatedBy']=file['CreatedBy']
        video['fileName']=file['fileName']
        video['url']='http://localhost:5000/streamvideo/'+file['fileName']
        video_object.append(video)
    return jsonify(video_object), 200


if __name__ == '__main__':
    app.run()
