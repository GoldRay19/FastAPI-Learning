# FastAPI File Upload and Static File Serving

## 1. Project Overview

This project demonstrates how to:

* Create a FastAPI application
* Accept files from users
* Upload and save files on the server
* Create an `uploads` directory automatically
* Serve uploaded files using `StaticFiles`
* Generate a URL for an uploaded file
* Check whether a requested file exists
* Handle errors using `HTTPException`

The complete flow is:

```text
Client
  |
  | POST /upload
  | File
  v
FastAPI
  |
  | Save file
  v
uploads/
  |
  | StaticFiles
  v
/files/<filename>
  |
  v
Client can access/download the file
```

---

# 2. Complete Code

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# Step 1: Ensure upload folder exists
upload_dir = "uploads"

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Step 2: Static file setup
# URL: http://127.0.0.1:8080/files/<filename>
app.mount(
    "/files",
    StaticFiles(directory=upload_dir),
    name="files"
)

# Step 3: Upload file API
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    filename = file.filename

    file_path = os.path.join(upload_dir, filename)

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="file not found"
        )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "file uploaded successfully",
        "file": f"http://127.0.0.1:8080/files/{filename}"
    }


# Step 4: Get file URL
@app.get("/files/{filename}")
def get_file(filename: str):

    file_path = os.path.join(upload_dir, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=400,
            detail="file not found"
        )

    return {
        "file_url": f"http://127.0.0.1:8080/files/{filename}"
    }


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "file uploaded successfully"
    }
```

---

# 3. Importing FastAPI Components

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
```

This imports four important things.

## FastAPI

```python
FastAPI
```

`FastAPI` is used to create the web application.

Example:

```python
app = FastAPI()
```

Here, `app` becomes our FastAPI application.

---

## UploadFile

```python
UploadFile
```

`UploadFile` is used when we want to receive a file from the client.

For example:

```text
image.jpg
resume.pdf
document.docx
video.mp4
```

When the client uploads a file, FastAPI provides information about that file through `UploadFile`.

It provides useful properties such as:

```python
file.filename
file.file
file.content_type
```

### `file.filename`

Contains the original name of the uploaded file.

Example:

```python
file.filename
```

could return:

```text
resume.pdf
```

---

### `file.file`

This represents the underlying file object.

It can be read and copied to another location.

In our code:

```python
shutil.copyfileobj(file.file, buffer)
```

copies the uploaded file into our destination file.

---

## File

```python
File
```

`File()` tells FastAPI that the parameter should come from an uploaded file.

Example:

```python
file: UploadFile = File(...)
```

The `...` means the file is required.

Therefore:

```python
file: UploadFile = File(...)
```

means:

> Accept a required uploaded file from the request.

---

## HTTPException

```python
HTTPException
```

is used to return an HTTP error response.

Example:

```python
raise HTTPException(
    status_code=400,
    detail="file not found"
)
```

The client receives an error response instead of a normal response.

---

# 4. StaticFiles Import

```python
from fastapi.staticfiles import StaticFiles
```

`StaticFiles` is used to serve files that already exist on the server.

For example, suppose our server contains:

```text
uploads/
    photo.jpg
    resume.pdf
    document.txt
```

We can configure FastAPI to make those files accessible through URLs.

For example:

```text
/files/photo.jpg
/files/resume.pdf
/files/document.txt
```

---

# 5. OS Module

```python
import os
```

The `os` module allows Python to interact with the operating system.

We use it for:

* Checking whether a directory exists
* Creating directories
* Creating file paths

For example:

```python
os.path.exists()
```

checks whether a file or directory exists.

And:

```python
os.makedirs()
```

creates a directory.

---

# 6. Shutil Module

```python
import shutil
```

`shutil` provides high-level file operations.

We use:

```python
shutil.copyfileobj()
```

to copy the uploaded file into our destination file.

---

# 7. Creating the FastAPI Application

```python
app = FastAPI()
```

This creates the FastAPI application object.

The `app` object is then used to create routes.

For example:

```python
@app.get("/")
```

and:

```python
@app.post("/upload")
```

---

# 8. Creating the Upload Directory

```python
upload_dir = "uploads"
```

This stores the name of the directory where uploaded files will be saved.

Our project will look like:

```text
project/
│
├── main.py
│
└── uploads/
```

The `uploads` directory will contain uploaded files.

For example:

```text
project/
│
├── main.py
│
└── uploads/
    ├── image.jpg
    ├── resume.pdf
    └── document.txt
```

---

# 9. Checking Whether the Folder Exists

```python
if not os.path.exists(upload_dir):
```

This checks whether the `uploads` directory already exists.

### `os.path.exists()`

Returns:

```text
True
```

if the path exists.

Returns:

```text
False
```

if it doesn't exist.

The `not` reverses the result.

Therefore:

```python
if not os.path.exists(upload_dir):
```

means:

> If the `uploads` directory does not exist...

---

# 10. Creating the Directory

```python
os.makedirs(upload_dir)
```

This creates the directory.

So this:

```python
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)
```

means:

> Check whether the uploads folder exists. If it doesn't exist, create it.

This prevents errors when trying to save files.

---

# 11. Static File Configuration

```python
app.mount(
    "/files",
    StaticFiles(directory=upload_dir),
    name="files"
)
```

This is one of the most important parts of the application.

It tells FastAPI:

> Serve everything inside the `uploads` directory through the `/files` URL path.

---

## Understanding `app.mount()`

```python
app.mount("/files", ...)
```

The first argument is:

```text
/files
```

This becomes the URL prefix.

---

## Understanding `StaticFiles`

```python
StaticFiles(directory=upload_dir)
```

Since:

```python
upload_dir = "uploads"
```

this becomes conceptually:

```python
StaticFiles(directory="uploads")
```

FastAPI will serve files from:

```text
uploads/
```

---

# 12. How Static File URLs Work

Suppose the following file exists:

```text
uploads/photo.jpg
```

Because we mounted:

```python
/files
```

the file becomes available at:

```text
http://127.0.0.1:8080/files/photo.jpg
```

The relationship is:

```text
uploads/photo.jpg
       |
       v
/files/photo.jpg
       |
       v
http://127.0.0.1:8080/files/photo.jpg
```

Another example:

```text
uploads/resume.pdf
```

becomes:

```text
http://127.0.0.1:8080/files/resume.pdf
```

---

# 13. Upload API

```python
@app.post("/upload")
```

This creates a POST endpoint.

The endpoint URL is:

```text
/upload
```

Therefore the complete URL is:

```text
http://127.0.0.1:8080/upload
```

We use `POST` because the client is sending data to the server.

---

# 14. Upload Function

```python
def upload_file(file: UploadFile = File(...)):
```

This function handles the uploaded file.

The parameter:

```python
file
```

contains the uploaded file.

The type:

```python
UploadFile
```

tells FastAPI that this is an uploaded file.

And:

```python
File(...)
```

tells FastAPI to read the file from the multipart form-data request.

---

# 15. Why `File(...)` Is Used

File uploads are normally sent using:

```text
multipart/form-data
```

FastAPI needs to know that the parameter comes from a file upload.

That's why we write:

```python
file: UploadFile = File(...)
```

Without `File(...)`, FastAPI would not interpret this parameter as a file upload in the same way.

---

# 16. Getting the Filename

```python
filename = file.filename
```

This retrieves the original filename.

For example, if the user uploads:

```text
profile.jpg
```

then:

```python
filename
```

contains:

```text
profile.jpg
```

---

# 17. Creating the File Path

```python
file_path = os.path.join(upload_dir, filename)
```

This creates the complete path where the file should be saved.

Suppose:

```python
upload_dir = "uploads"
```

and:

```python
filename = "profile.jpg"
```

Then:

```python
os.path.join(upload_dir, filename)
```

produces:

```text
uploads/profile.jpg
```

This is better than manually writing:

```python
"uploads/" + filename
```

because `os.path.join()` handles path separators appropriately for the operating system.

---

# 18. Checking the Filename

```python
if not filename:
```

This checks whether a filename was provided.

If there is no filename, we return an error.

```python
raise HTTPException(
    status_code=400,
    detail="file not found"
)
```

---

# 19. Understanding `HTTPException`

```python
raise HTTPException(...)
```

stops normal execution and sends an HTTP error response.

Here:

```python
status_code=400
```

means:

```text
400 Bad Request
```

and:

```python
detail="file not found"
```

provides an explanation.

The response looks approximately like:

```json
{
    "detail": "file not found"
}
```

---

# 20. Opening the Destination File

```python
with open(file_path, "wb") as buffer:
```

This opens the destination file.

There are two important parts:

```python
file_path
```

and:

```python
"wb"
```

---

## What Does `"wb"` Mean?

`w` means:

```text
write
```

`b` means:

```text
binary
```

Therefore:

```text
"wb"
```

means:

> Open the file for writing binary data.

This is important because uploaded files can be:

* Images
* PDFs
* Videos
* ZIP files
* Documents
* Other binary files

---

# 21. Why `with open()` Is Used

```python
with open(...) as buffer:
```

The `with` statement automatically manages the file.

After the operation is finished, Python closes the file.

This is safer than manually doing:

```python
file = open(...)
# operations
file.close()
```

---

# 22. Copying the Uploaded File

```python
shutil.copyfileobj(file.file, buffer)
```

This copies data from:

```python
file.file
```

to:

```python
buffer
```

The flow is:

```text
Uploaded file
      |
      v
file.file
      |
      | shutil.copyfileobj()
      v
buffer
      |
      v
uploads/filename
```

For example:

```text
User uploads:
resume.pdf

        ↓

FastAPI receives:
file.file

        ↓

copyfileobj()

        ↓

Server saves:
uploads/resume.pdf
```

---

# 23. Upload Response

After the file is successfully saved:

```python
return {
    "message": "file uploaded successfully",
    "file": f"http://127.0.0.1:8080/files/{filename}"
}
```

FastAPI automatically converts this Python dictionary into JSON.

For example, if the user uploads:

```text
photo.jpg
```

the response will be:

```json
{
    "message": "file uploaded successfully",
    "file": "http://127.0.0.1:8080/files/photo.jpg"
}
```

---

# 24. Understanding the f-string

```python
f"http://127.0.0.1:8080/files/{filename}"
```

The `f` before the string allows us to insert variables.

If:

```python
filename = "photo.jpg"
```

then:

```python
f"http://127.0.0.1:8080/files/{filename}"
```

becomes:

```text
http://127.0.0.1:8080/files/photo.jpg
```

---

# 25. File URL Endpoint

```python
@app.get("/files/{filename}")
```

This creates another GET endpoint.

It accepts the filename dynamically.

For example:

```text
/files/photo.jpg
```

or:

```text
/files/resume.pdf
```

The part:

```text
{filename}
```

is called a **path parameter**.

---

# 26. Path Parameters

Consider:

```python
@app.get("/files/{filename}")
def get_file(filename: str):
```

If the client requests:

```text
/files/photo.jpg
```

then:

```python
filename
```

will contain:

```text
photo.jpg
```

If the client requests:

```text
/files/resume.pdf
```

then:

```python
filename
```

will contain:

```text
resume.pdf
```

---

# 27. Creating the File Path Again

```python
file_path = os.path.join(upload_dir, filename)
```

Suppose:

```python
filename = "resume.pdf"
```

Then:

```text
uploads/resume.pdf
```

is created as the file path.

---

# 28. Checking Whether the File Exists

```python
if not os.path.exists(file_path):
```

This checks whether the requested file exists on the server.

If:

```text
uploads/resume.pdf
```

doesn't exist, an error is returned.

---

# 29. Returning File Not Found

```python
raise HTTPException(
    status_code=400,
    detail="file not found"
)
```

This tells the client that the requested file could not be found.

A more semantically appropriate status code would normally be:

```python
status_code=404
```

because `404 Not Found` means that the requested resource doesn't exist.

So the improved version would be:

```python
raise HTTPException(
    status_code=404,
    detail="file not found"
)
```

---

# 30. Returning the File URL

If the file exists:

```python
return {
    "file_url": f"http://127.0.0.1:8080/files/{filename}"
}
```

For:

```text
resume.pdf
```

the response is:

```json
{
    "file_url": "http://127.0.0.1:8080/files/resume.pdf"
}
```

---

# 31. Important Difference Between the Two `/files` Routes

There are two things using `/files`.

First:

```python
app.mount("/files", StaticFiles(directory=upload_dir), name="files")
```

This actually **serves the files**.

Second:

```python
@app.get("/files/{filename}")
```

This returns a JSON object containing the URL.

So:

### StaticFiles

```text
/files/photo.jpg
```

actually gives access to:

```text
photo.jpg
```

### GET endpoint

```text
/files/photo.jpg
```

is intended to return:

```json
{
    "file_url": "..."
}
```

However, there is an important issue here.

Because `StaticFiles` is mounted at `/files`, the mounted application handles requests under `/files`. Therefore, using the same `/files/{filename}` path for your JSON endpoint is unnecessary and can lead to routing behavior you don't expect.

A cleaner design is to use something like:

```python
@app.get("/file-url/{filename}")
```

for the JSON URL lookup endpoint.

---

# 32. Home Endpoint

```python
@app.get("/")
def home():
```

This creates the root endpoint.

URL:

```text
http://127.0.0.1:8080/
```

It returns:

```python
{
    "message": "file uploaded successfully"
}
```

A better message would be:

```python
{
    "message": "File upload API is running"
}
```

because visiting `/` does not necessarily mean a file has been uploaded.

---

# 33. Complete Request Flow

Let's understand the entire application from beginning to end.

## Step 1 — Server starts

When the application starts:

```python
app = FastAPI()
```

creates the application.

Then:

```python
upload_dir = "uploads"
```

defines the upload directory.

---

## Step 2 — Upload directory is created

The application checks:

```python
os.path.exists(upload_dir)
```

If it doesn't exist:

```python
os.makedirs(upload_dir)
```

creates it.

---

## Step 3 — Static files are configured

```python
app.mount(
    "/files",
    StaticFiles(directory=upload_dir),
    name="files"
)
```

tells FastAPI that files in:

```text
uploads/
```

can be accessed through:

```text
/files/
```

---

## Step 4 — Client uploads a file

Client sends:

```text
POST /upload
```

with a file.

For example:

```text
photo.jpg
```

---

## Step 5 — FastAPI receives the file

FastAPI creates an:

```python
UploadFile
```

object.

Then:

```python
file.filename
```

returns:

```text
photo.jpg
```

---

## Step 6 — File path is created

```python
file_path = os.path.join(upload_dir, filename)
```

becomes:

```text
uploads/photo.jpg
```

---

## Step 7 — File is saved

```python
with open(file_path, "wb") as buffer:
    shutil.copyfileobj(file.file, buffer)
```

saves:

```text
photo.jpg
```

inside:

```text
uploads/
```

---

## Step 8 — URL is returned

The API returns:

```json
{
    "message": "file uploaded successfully",
    "file": "http://127.0.0.1:8080/files/photo.jpg"
}
```

---

## Step 9 — User opens the URL

The browser requests:

```text
/files/photo.jpg
```

`StaticFiles` finds:

```text
uploads/photo.jpg
```

and serves it.

---

# 34. Example Project Structure

After uploading a few files, your project might look like:

```text
FastAPI File Upload/
│
├── main.py
│
└── uploads/
    ├── photo.jpg
    ├── resume.pdf
    └── document.txt
```

---

# 35. How to Run the Application

Suppose your Python file is named:

```text
main.py
```

Run:

```bash
uvicorn main:app --reload --port 8080
```

Explanation:

```text
uvicorn
```

runs the ASGI server.

```text
main
```

means:

```text
main.py
```

```text
app
```

means the FastAPI object:

```python
app = FastAPI()
```

```text
--reload
```

automatically reloads the server when code changes.

```text
--port 8080
```

runs the server on port `8080`.

The application will be available at:

```text
http://127.0.0.1:8080
```

---

# 36. Opening Swagger UI

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8080/docs
```

You should see:

```text
GET  /
POST /upload
GET  /files/{filename}
```

You can test the APIs directly from Swagger UI.

---

# 37. Testing the Upload API

Open:

```text
http://127.0.0.1:8080/docs
```

Find:

```text
POST /upload
```

Click:

```text
Try it out
```

You will see a file upload field.

Choose a file.

For example:

```text
test.jpg
```

Then click:

```text
Execute
```

FastAPI sends the request to:

```text
POST /upload
```

---

# 38. Expected Upload Response

If the upload succeeds:

```json
{
    "message": "file uploaded successfully",
    "file": "http://127.0.0.1:8080/files/test.jpg"
}
```

The file will also appear in:

```text
uploads/
```

---

# 39. Accessing the Uploaded File

Copy the returned URL:

```text
http://127.0.0.1:8080/files/test.jpg
```

and open it in the browser.

FastAPI's `StaticFiles` will serve the file.

For an image:

```text
The image will be displayed.
```

For a PDF:

```text
The PDF may open in the browser.
```

For a downloadable file:

```text
The browser may download it depending on its type and headers.
```

---

# 40. Important Concept: Upload vs Static File Serving

These are two different operations.

## Upload

```python
@app.post("/upload")
```

is responsible for:

```text
Client
  ↓
File
  ↓
FastAPI
  ↓
uploads/
```

## Static serving

```python
app.mount(
    "/files",
    StaticFiles(directory=upload_dir),
    name="files"
)
```

is responsible for:

```text
uploads/
  ↓
StaticFiles
  ↓
Browser
```

Therefore:

```text
Upload API = saves files
StaticFiles = serves files
```

---

# 41. Why We Need `StaticFiles`

Without:

```python
StaticFiles
```

the uploaded file would exist on the server, but FastAPI would not automatically expose it through a URL.

For example:

```text
uploads/photo.jpg
```

exists physically on the server.

But users cannot simply access it through:

```text
/files/photo.jpg
```

unless we configure a route or static file server.

That's why:

```python
app.mount(...)
```

is useful.

---

# 42. `File(...)` vs `UploadFile`

These two are related but different.

### `File(...)`

Tells FastAPI:

> This parameter comes from a file upload.

### `UploadFile`

Represents:

> The uploaded file itself.

Therefore:

```python
file: UploadFile = File(...)
```

means:

> Receive a required uploaded file and represent it using FastAPI's `UploadFile` object.

---

# 43. Why Use `UploadFile` Instead of Reading Raw Bytes?

FastAPI's `UploadFile` is useful for file uploads because it provides a file-like interface and metadata such as:

```python
file.filename
file.content_type
file.file
```

This makes it convenient for handling uploaded files without manually parsing the multipart request.

---

# 44. Security Consideration: Filename

The current code does:

```python
filename = file.filename

file_path = os.path.join(upload_dir, filename)
```

For a learning project, this is easy to understand.

However, in a production application, you should **not blindly trust the original filename**.

A malicious client could potentially provide a filename containing path components.

A safer approach is to sanitize the filename, for example with:

```python
from pathlib import Path

filename = Path(file.filename).name
```

This removes directory components.

---

# 45. Security Consideration: Duplicate Filenames

Suppose the server already has:

```text
uploads/photo.jpg
```

and another user uploads another:

```text
photo.jpg
```

Then:

```python
open(file_path, "wb")
```

will overwrite the existing file.

This can be avoided by generating a unique filename.

For example:

```text
photo_12345.jpg
```

or using a UUID:

```text
550e8400-e29b-41d4-a716-446655440000.jpg
```

---

# 46. Security Consideration: File Types

The current application accepts essentially any uploaded file.

A production application should consider restricting file types.

For example:

```text
Allowed:
.jpg
.jpeg
.png
.pdf
```

You can inspect:

```python
file.content_type
```

For example:

```text
image/jpeg
image/png
application/pdf
```

However, MIME type alone should not be treated as a complete security check.

---

# 47. Security Consideration: File Size

A production application should also limit the maximum upload size.

Otherwise, someone could attempt to upload extremely large files and consume server storage or memory/bandwidth.

Possible limits include:

```text
Maximum image size: 5 MB
Maximum PDF size: 10 MB
Maximum video size: 100 MB
```

---

# 48. Better HTTP Status Code

Your current file-checking endpoint uses:

```python
status_code=400
```

for a missing file.

A better status code is:

```python
status_code=404
```

because:

```text
400 = Bad Request
404 = Resource Not Found
```

Therefore:

```python
raise HTTPException(
    status_code=404,
    detail="file not found"
)
```

is more appropriate.

---

# 49. Recommended Route Design

Because `/files` is already mounted for static files, it is cleaner to avoid another API endpoint using the same path.

Instead of:

```python
@app.get("/files/{filename}")
```

you could use:

```python
@app.get("/file-url/{filename}")
```

Then:

```text
GET /file-url/photo.jpg
```

returns:

```json
{
    "file_url": "http://127.0.0.1:8080/files/photo.jpg"
}
```

while:

```text
GET /files/photo.jpg
```

actually serves the file.

This creates a clearer separation.

---

# 50. Recommended Architecture

A cleaner version of the routes would be:

```text
GET  /
POST /upload
GET  /file-url/{filename}
GET  /files/{filename}
```

Where:

```text
POST /upload
        ↓
Save file
```

```text
GET /file-url/{filename}
        ↓
Return URL
```

```text
GET /files/{filename}
        ↓
Serve actual file
```

---

# 51. Complete Improved Version

Here is a cleaner version based on your project:

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil

app = FastAPI()

# Upload directory
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

# Serve uploaded files
app.mount(
    "/files",
    StaticFiles(directory=upload_dir),
    name="files"
)


# Upload API
@app.post("/upload")
def upload_file(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided"
        )

    filename = Path(file.filename).name
    file_path = upload_dir / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "file_url": f"http://127.0.0.1:8080/files/{filename}"
    }


# Get file URL
@app.get("/file-url/{filename}")
def get_file_url(filename: str):

    filename = Path(filename).name
    file_path = upload_dir / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "file_url": f"http://127.0.0.1:8080/files/{filename}"
    }


# Home
@app.get("/")
def home():
    return {
        "message": "File upload API is running"
    }
```

---

# 52. Final Concept Summary

The most important concepts in this project are:

| Concept                | Purpose                            |
| ---------------------- | ---------------------------------- |
| `FastAPI()`            | Creates the API application        |
| `UploadFile`           | Represents uploaded files          |
| `File(...)`            | Tells FastAPI to receive a file    |
| `HTTPException`        | Returns HTTP errors                |
| `os.path.exists()`     | Checks whether a path exists       |
| `os.makedirs()`        | Creates directories                |
| `os.path.join()`       | Builds safe OS-specific paths      |
| `shutil.copyfileobj()` | Copies uploaded file data          |
| `StaticFiles`          | Serves files from a directory      |
| `app.mount()`          | Mounts the static file application |
| `@app.post()`          | Creates POST endpoint              |
| `@app.get()`           | Creates GET endpoint               |
| `{filename}`           | Path parameter                     |
| `"wb"`                 | Write binary mode                  |
| `file.filename`        | Original filename                  |
| `file.file`            | Uploaded file object               |

---

# 53. Overall Architecture

```text
                 CLIENT
                   |
                   |
             POST /upload
                   |
                   v
          +----------------+
          |    FastAPI     |
          |                |
          |  UploadFile    |
          +-------+--------+
                  |
                  |
          Save uploaded file
                  |
                  v
             +---------+
             | uploads |
             +---------+
                  |
                  |
            StaticFiles
                  |
                  v
        /files/<filename>
                  |
                  v
               CLIENT
```

---

# 54. One-Line Explanation of the Project

> This FastAPI application accepts files through a multipart upload endpoint, saves them inside an `uploads` directory, and exposes those uploaded files through publicly accessible static URLs using FastAPI's `StaticFiles`.

---

# 55. Key Interview Questions

### Q1. What is `UploadFile`?

`UploadFile` is FastAPI's file-upload abstraction that provides access to the uploaded file, its filename, content type, and underlying file object.

### Q2. Why do we use `File(...)`?

It tells FastAPI that the parameter should be received as a file from a multipart form-data request.

### Q3. What does `StaticFiles` do?

It serves files from a directory through HTTP URLs.

### Q4. What does `app.mount()` do?

It mounts another ASGI application, such as `StaticFiles`, under a particular URL path.

### Q5. Why use `"wb"`?

Because uploaded files may contain binary data. `"wb"` means write binary mode.

### Q6. What does `shutil.copyfileobj()` do?

It copies data from one file-like object to another.

### Q7. What is `{filename}`?

It is a FastAPI path parameter.

### Q8. What is the difference between `400` and `404`?

```text
400 → Bad Request
404 → Resource Not Found
```

A missing requested file should normally return `404`.

### Q9. Why shouldn't we blindly trust `file.filename`?

Because filenames supplied by clients can be manipulated and may cause path traversal or filename collision problems.

### Q10. What is the purpose of the `uploads` folder?

It is the server-side storage location for files uploaded through the API.

---

# 56. Final Flow to Remember

```text
1. Client selects a file
        ↓
2. POST /upload
        ↓
3. FastAPI receives UploadFile
        ↓
4. Get file.filename
        ↓
5. Build uploads/<filename>
        ↓
6. Open destination in "wb" mode
        ↓
7. Copy file using shutil.copyfileobj()
        ↓
8. File is stored in uploads/
        ↓
9. Return file URL
        ↓
10. StaticFiles serves the file
```

This project is a basic but important example of **file handling in FastAPI** and forms the foundation for features such as profile-picture uploads, document uploads, PDF storage, image galleries, and media APIs.
