from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

app=FastAPI()

#step1 Ensure upload folder exists
upload_dir="uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

#step2 Static file set up
#url: HTTP://127.0.0.1:8080<Filename>
app.mount("/files",StaticFiles(directory=upload_dir),name="files")

#step 3 Upload file api
@app.post("/upload")
def upload_file(file:UploadFile=File(...)):
    filename=file.filename
    file_path=os.path.join(upload_dir,filename)
    if not filename:
        raise HTTPException(
            status_code=400,
            detail="file not found"
        )
    with open(file_path,"wb")as buffer:
        shutil.copyfileobj(file.file,buffer)
    return {
            "message":"file uploaded successfully",
            "file":f"HTTP://127.0.0.1:8080/files/{filename}"
        }

#step 4 gET FILE URL
@app.get("/files/{filename}")
def get_file(filename:str):
    file_path=os.path.join(upload_dir,filename)
    if not os.path.exists(file_path):
        raise HTTPException(
                    status_code=400,
                    detail="file not found"
                    )
    return {
        "file_url":f"HTTP://127.0.0.1:8080/files/{filename}"
    }

@app.get("/")
def home():
    return {
        "message":"file uploaded successfully"
    }