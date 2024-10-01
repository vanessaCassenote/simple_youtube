from s3_access import S3
import os
import tracemalloc

def save_to_s3():
    filename = "videoplayback.mp4"
    s3 = S3()
    s3.create_multipart_upload(bucket="simple-youtube", object_name=filename)
    
    filesize = os.path.getsize(filename)
    chunk_size = 1024*1024*10 # 10MB
    num_chunks = filesize // chunk_size # 10MB
    
    etags = []

    with open(filename, "rb") as f:        
        for i in range(1,num_chunks+2):
            print(f"Chunck: {i}")
            if i == num_chunks+1:
                chunk = f.read()
            else:
                chunk = f.read(chunk_size)
            response = s3.upload_part(file_to_upload=chunk, part_number=i)
            etags.append(response)
    
    public_url = s3.complete_multipart_upload(etags)
    print(public_url)
    
    
    
    




if __name__ == "__main__":
    save_to_s3()