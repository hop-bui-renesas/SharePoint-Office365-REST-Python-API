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
    recursive = False if request.recursive is None else request.recursive
    folders = client.get_folders(folder_path=request.folder_path, recursive=recursive)
    return FoldersResponse(folders=folders)

@app.post("/files")
def read_files(request: FilesRequest) -> FilesResponse:
    recursive = False if request.recursive is None else request.recursive
    files = client.get_files(folder_path=request.folder_path, recursive=recursive)
    if request.is_download:
        client.download_files(files=files, local_dir=request.local_dir)
    return FilesResponse(files=files)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)