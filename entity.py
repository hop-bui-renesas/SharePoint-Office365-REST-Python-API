from pydantic import BaseModel

class FoldersRequest(BaseModel):
    folder_path: str
    recursive: bool

class FoldersResponse(BaseModel):
    folders: list[dict]

class FilesRequest(BaseModel):
    folder_path: str
    recursive: bool
    is_download: bool
    local_dir: str

class FilesResponse(BaseModel):
    files: list[dict]