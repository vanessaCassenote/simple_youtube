from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.video_model import Video
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

class Postgres:
    
    def __init__(self) -> None:
        engine = create_engine(f"postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/simple_youtube")
        Session = sessionmaker(bind=engine)
        self.session = Session()
    
    def insert_video(self, Video):
        self.session.add(Video)
        self.session.commit()
    
    def select_videos(self):
        return self.session.query(Video).all()
        
    def select_video(self, id):
        return self.session.query(Video).filter_by(id=id).one_or_none()
    
    def update_video(self,Video):
        self.session.commit()
    
        
    def delete_video(self, Video):
        self.session.delete(Video)
        self.session.commit()
    
    