from typing import Union

from fastapi import FastAPI

from client import SPClient

from entity import FoldersRequest, FoldersResponse, FilesRequest, FilesResponse

import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("sharepoint_url")
USERNAME = os.environ["user_id"]
PASSWORD = os.environ["password"]

app = FastAPI()

client = SPClient(url=URL, username=USERNAME, password=PASSWORD)

@app.post("/folders")
def read_folders(request: FoldersRequest) -> FoldersResponse:
    folders = client.get_folders(request.folder_path)
    return FoldersResponse(folders=folders)

@app.post("/files_in_folder")
def read_files_in_folder(request: FilesRequest) -> FilesResponse:
    files = client.get_files_in_folder_path(request.folder_path)
    return FilesResponse(files=files)

@app.post("/files")
def read_files(request: FilesRequest) -> FilesResponse:
    files = client.get_files(request.folder_path)
    return FilesResponse(files=files)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)