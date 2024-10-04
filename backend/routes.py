from flask import Flask, redirect, request, url_for, render_template, session, jsonify
import flask
from functools import wraps
import requests
import os
import base64
from app import app, oauth, google
from src.services.upload_services import open_multi_upload_s3, upload_parts_s3, complete_multi_part_s3

order_upload = {}
count = 0

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'google_token' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    
    videos = {
        "0":{
            "title": "Title 1",
            "thumbnail":"thumb",
            "id":123
        },
        "1":{
            "title": "Title 2",
            "thumbnail":"thumb 2",
            "id":124
        }
    }
    return jsonify(videos) #"Hello <a href=/login><button>Login</button></a>"

@app.route("/login")
def login():      
    # try:
    #     redirect_uri = url_for("callback", _external=True)
    #     response = google.authorize(callback=redirect_uri)
    #     return response
    # except Exception as e:
    #     app.logger.error(f"Erro during login:{str(e)}")
    #     return jsonify({"msg":"Error occurred during login", "status":500})

    videos = {
        "url":f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=869701619623-domqc7vkcm6ue7d1tnmbc5ovmmddo7vn.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fcallback&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+openid&service=lso&o2v=1&ddm=0&flowName=GeneralOAuthFlow"
    }
    return jsonify(videos)

@app.route("/callback")
def callback():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Login failed.'
    session['google_token'] = (response['access_token'], '')
    return jsonify(session['google_token'])

@app.route("/upload", methods=['POST'])
@login_required
def upload():
    data = request.json
    print(data)

@app.route("/upload_parts", methods=['POST'])
def upload_parts():
    data = request.json
    imgdata = base64.b64decode(data["chunk"])
    order_upload[int(data["chunk_index"])] = {"chunk": imgdata,
                                                "filename":data["filename"],
                                                "total_chunks":data["total_chunks"],
                                                "upload_id":data["upload_id"]
                                              }
    return jsonify({"status":200})

@app.route("/upload_end", methods=['GET'])
def upload_end():
    total_chunks = order_upload[1]["total_chunks"]
    open_multi_upload_s3(filename=order_upload[1]["filename"])
    
    for i in range(1, total_chunks+1):
        imgdata = order_upload[i]["chunk"]
        upload_parts_s3(chunk=imgdata, part_number=i)
    complete_multi_part_s3()
    return jsonify({"status":200})

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))
