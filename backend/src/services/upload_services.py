import os
from src.config.aws.s3.s3_access import S3
from src.models.video_model import Video
from src.config.postgres.db_access import Postgres

s3 = S3()
ETAGS = []

def send_to_kafka():
    pass

def save_to_postgres(filename, url):
    vid = Video(title = filename.split(".")[0],
                url = url,
                owner_id = 3)
    db = Postgres()
    db.insert_video(Video=vid)

def open_multi_upload_s3(filename):
    s3.create_multipart_upload(bucket="simple-youtube", object_name=filename)

def upload_parts_s3(chunk, part_number):
    response = s3.upload_part(file_to_upload=chunk, part_number=part_number)
    ETAGS.append(response)

def complete_multi_part_s3():    
    public_url = s3.complete_multipart_upload(ETAGS)
    return public_url

# def save_to_s3():
    
#     filename = "videoplayback.mp4"
    
#     s3.create_multipart_upload(bucket="simple-youtube", object_name=filename)
    
#     filesize = os.path.getsize(filename)
#     chunk_size = 1024*1024*10 # 10MB
#     num_chunks = filesize // chunk_size # 10MB
    
#     etags = []

#     with open(filename, "rb") as f:        
#         for i in range(1,num_chunks+2):
#             print(f"Chunck: {i}")
#             if i == num_chunks+1:
#                 chunk = f.read()
#             else:
#                 chunk = f.read(chunk_size)
                
#             print("tipo do chunk: ", type(chunk))
#             response = s3.upload_part(file_to_upload=chunk, part_number=i)
#             etags.append(response)
    
#     public_url = s3.complete_multipart_upload(etags)
#     print(public_url)
    
    # Save metadata to postgres
    #save_to_postgres(filename, public_url)
    
    # Send to kafka for transcoding