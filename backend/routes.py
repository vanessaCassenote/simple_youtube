from flask import Flask, redirect, request, url_for, session, jsonify
from functools import wraps
import base64
from app import app, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
from google.oauth2 import id_token
from google.auth.transport import requests
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, unset_jwt_cookies
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


@app.route("/login", methods=["POST"])
def login(): 
    
    token = request.json["token"]
    
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        user_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If the request specified a Google Workspace domain
        # if idinfo['hd'] != DOMAIN_NAME:
        #     raise ValueError('Wrong domain name.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = user_info['sub']
    except ValueError:
        # Invalid token
        pass

    access_token = create_access_token(identity=user_info['email'])
    return jsonify(access_token=access_token)

@app.route("/upload_start", methods=['POST'])
@jwt_required()
def upload_start():
    data = request.json
    open_multi_upload_s3(filename=data["filename"])
    return jsonify({"Upload Started":200})

@app.route("/upload_parts", methods=['POST'])
@jwt_required()
def upload_parts():
    data = request.json
    imgdata = base64.b64decode(data["chunk"])
    upload_parts_s3(chunk=imgdata, part_number=data["chunk_index"])
    return jsonify({f"Upload {data["chunk_index"]}/{data["total_chunks"]}":200})

@app.route("/upload_end", methods=['POST'])
@jwt_required()
def upload_end():
    data = request.json     
    public_url = complete_multi_part_s3()
    save_to_postgres(title=data["title"], 
                     filename=data["filename"], 
                     screenshot=data["screenshot"], 
                     url=public_url)
    return jsonify({"Upload Ended":200})

@app.route("/logout", methods=["GET"])
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200
