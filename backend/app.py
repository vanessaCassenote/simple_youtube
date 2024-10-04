from flask import Flask
from flask_cors import CORS
from flask_oauthlib.client import OAuth
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

app = Flask(__name__)
app.secret_key = "supersecretkey"
oauth = OAuth(app)

# const corsOptions = {
#   origin: '*',
#   methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
#   allowedHeaders: 'Content-Type, Authorization',
# };

cors = CORS(app)

ALLOWED_EXTENSIONS = {'mp4'}
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

google = oauth.remote_app(
    'google',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={
            'scope': 
                ["https://www.googleapis.com/auth/userinfo.profile", 
                "https://www.googleapis.com/auth/userinfo.email", 
                "openid"]
    },
    base_url=os.getenv("BASE_URL"),
    request_token_url=None,
    access_token_method=os.getenv("ACCESS_TOKEN_METHOD"),
    access_token_url=os.getenv("ACCESS_TOKEN_URL"),
    authorize_url=os.getenv("AUTHORIZE_URL"),
)


with app.app_context():
    from routes import *





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
    #from src.services.upload_services import save_to_s3, save_to_postgres,send_to_kafka
    
    #save_to_s3()
    #save_to_postgres()
    #send_to_kafka()
    
    
    
    
