from flask import Flask, redirect, request, url_for, render_template, session, jsonify
import flask
from functools import wraps
import requests
import os
import base64
from app import app, oauth, google
from src.services.upload_services import open_multi_upload_s3, upload_parts_s3, complete_multi_part_s3, save_to_postgres
from src.services.watch_services import get_all_videos

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
    return jsonify(get_all_videos())

@app.route("/login")
def login():      
    try:
        redirect_uri = url_for("callback", _external=True)
        response = google.authorize(callback=redirect_uri)
        print("--------1------------",response.location)
        print("--------2------------",response.headers)
        print("--------3------------",response.get_json())
        
    except Exception as e:
        app.logger.error(f"Erro during login:{str(e)}")
        return jsonify({"msg":"Error occurred during login", "status":500})
    
    return jsonify({"response":response.location})

@app.route("/callback")
def callback():
    print("olaaaa2024")
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Login failed.'
    session['google_token'] = (response['access_token'], '')
    return jsonify({"session":session['google_token']})

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
    
    public_url = complete_multi_part_s3()
    save_to_postgres(filename=order_upload[1]["filename"], url=public_url)
    
    return jsonify({"status":200})

@app.route("/logout", methods=["GET"])
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))
