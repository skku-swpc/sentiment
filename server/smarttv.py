#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import Response
from functools import wraps
from flask import json
from flask import request
from flask import jsonify
import MySQLdb
import urllib

import tweepy
import codecs
import sys

# for twitter api
consumer_key="TWITTER_CONSUMER_KEY"
consumer_secret="TWITTER_SECRET"

access_token="TWITTER_ACCESS_TOKEN"
access_token_secret="TWITTER_ACCESS_TOKEN_SECRET"
# for twitter api end

app = Flask(__name__)

def check_auth(username, password):
    dic_username_password = dict()
    # password setup
    dic_username_password['test'] = 'test1'
    # password setup end
    
    if username in dic_username_password:
        if dic_username_password[username] == password:
            return True
    return False

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)
    
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

def gen_sql_query(title, days, onair, ch, casts):
    if title == "" and days == "" and onair == "":
        if ch == "" and casts == "":
            return ""
    list_casts = casts.split(",")
    
    sql_query = "SELECT * FROM TVprogram where "
    sql_query += "title like '%" + title + "%'"
    sql_query += " and days like '%" + days + "%'"
    if onair != "": 
        sql_query += " and onair like '" + onair + ":%'"
    if ch != "": 
        sql_query += " and ch = '" + ch + "'"
    if len(list_casts) != 0: 
        sql_query += " and " 
    for i in range(len(list_casts)):
        if i != 0:
            sql_query += " and"
        sql_query += " casts like '%" + list_casts[i] + "%'" 
    
    return sql_query

@app.route('/twitter', methods = ['GET'])
@requires_auth
def twitter():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    query = request.args.get('query')
    
    max_tweets = 100

    searched_tweets = [status._json for status in tweepy.Cursor(api.search,  q=query,lang="ko").items(max_tweets)]
    json_strings = [json.dumps(json_obj) for json_obj in searched_tweets]  

    list_tweets = []
    for i in range(len(json_strings)):
        if '"text": "RT' not in json_strings[i]:
            json_strings[i] = json_strings[i].encode('utf-8')
            json_strings[i] = json_strings[i].decode('unicode_escape')
            json_strings[i] = json_strings[i].replace('\n',' ')
            json_strings[i] = json_strings[i].replace('\r',' ')
            
            list_tweets.append(json_strings[i])
    js = json.dumps(list_tweets)
    
    resp = Response(js, status = 200, mimetype = 'application/json')
    resp.headers['Link'] = 'http://pcred.yonsei.ac.kr'

    return resp


@app.route('/program', methods = ['GET'])
@requires_auth
def program():
    title = request.args.get('title')
    days = request.args.get('days')
    onair = request.args.get('onair')
    ch = request.args.get('ch')
    casts = request.args.get('casts')
    
    db = MySQLdb.connect(host="localhost", 
            user="your_mysql_db_user", passwd="your_mysql_db_password", 
            db="tv", use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql_query = gen_sql_query(title, days, onair, ch, casts)


    list_info = []
    if sql_query != "":
        print sql_query

        cursor.execute(sql_query)
        db.commit()
        numrows = int(cursor.rowcount)
        for i in range(numrows):
            row = cursor.fetchone()
            program_info = dict()
            # id / title / birth / days / onair / ch / casts  
            program_info["id"] = row[0]
            program_info["title"] = row[1]
            program_info["days"] = row[3]
            program_info["onair"] = row[4]
            program_info["ch"] = row[5]
            program_info["casts"] = row[6]
            
            list_info.append(program_info) 
    
    db.close()

    js = json.dumps(list_info)

    resp = Response(js, status = 200, mimetype = 'application/json')
    resp.headers['Link'] = 'http://pcred.yonsei.ac.kr'

    return resp


