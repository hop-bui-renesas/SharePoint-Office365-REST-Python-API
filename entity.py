from pydantic import BaseModel

class FoldersRequest(BaseModel):
    folder_path: str

class FoldersResponse(BaseModel):
    folders: list[dict]

class FilesRequest(BaseModel):
    folder_path: str

class FilesResponse(BaseModel):
    files: list[dict]