from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)
    screenshot = Column(String)
    url = Column(String)
    owner_id = Column(Integer)

    
    def get_json(self):
        return {
            "id":self.id,
            "title":self.title,
            "screenshot":self.screenshot,
            "url":self.url,
            "owner_id":self.owner_id
        }
    