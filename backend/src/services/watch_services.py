from src.config.postgres.db_access import Postgres

def get_all_videos():
    db = Postgres()
    videos = db.select_videos()
    
    list_of_videos = []
    for vid in videos:
        list_of_videos.append(vid.get_json())
    return list_of_videos