import os
import pathlib
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from google.oauth2 import id_token
import requests
from pip._vendor import cachecontrol
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

class Authentication:
    def __init__(self) -> None:
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

        self.flow = Flow.from_client_secrets_file(
            client_secrets_file=client_secrets_file,
            scopes=["https://www.googleapis.com/auth/userinfo.profile", 
                    "https://www.googleapis.com/auth/userinfo.email", "openid"],
            redirect_uri="http://127.0.0.1:5000/callback"
        )
        
    def login(self):
        authorization_url, state = self.flow.authorization_url()
        return authorization_url, state
    
    def callback(self, request, cached_session):
        self.flow.fetch_token(authorization_response=request)
        
        credentials = self.flow.credentials

        token_request = google.auth.transport.requests.Request(session=cached_session)

        id_info = id_token.verify_oauth2_token(
            id_token=credentials._id_token,
            request=token_request,
            audience=GOOGLE_CLIENT_ID
        )
        print(GOOGLE_CLIENT_ID)
        return id_info
