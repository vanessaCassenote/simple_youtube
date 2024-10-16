from flask import Flask
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

app = Flask(__name__)
app.secret_key = "supersecretkey"
oauth = OAuth(app)
cors = CORS(app)


# Initialize JWTManager
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key
jwt = JWTManager(app)

ALLOWED_EXTENSIONS = {'mp4'}
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


with app.app_context():
    from routes import *





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
