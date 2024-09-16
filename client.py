import os
import time

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

from utils import print_download_progress
class SPClient():
    username: str
    password: str
    url: str
    user_credentials: UserCredential
    ctx = None

    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password
        self.user_credentials = UserCredential(username, password)
    
    @property
    def static_ctx(self) -> ClientContext:
        if self.ctx is None:
            self.ctx = ClientContext(self.url).with_credentials(self.user_credentials)
        return self.ctx
    
    def get_folders(self, folder_path: str, recursive: bool) -> list[dict]:
        web = self.static_ctx.web
        self.ctx.load(web)
        self.ctx.execute_query()
        server_relative_url = web.properties['ServerRelativeUrl']
        folder_server_relative_url = server_relative_url + folder_path
        root_folder = self.ctx.web.get_folder_by_server_relative_url(folder_server_relative_url)
        folders = root_folder.get_folders(recursive=recursive).execute_query()
        return [folder.properties for folder in folders]
    
    def get_files(self, folder_path: str, recursive: bool) -> list[dict]:
        web = self.static_ctx.web
        self.ctx.load(web)
        self.ctx.execute_query()
        root_folder = self.ctx.web.get_folder_by_server_relative_path(folder_path)
        files = root_folder.get_files(recursive=recursive).execute_query()
        return [file.properties for file in files]
    
    def download_files(self, files: list[dict], local_dir: str) -> list[dict]:
        download_result = []
        for file in files:
            start_time  = time.time()
            error = False
            file_name = file["Name"]
            file_path = file["ServerRelativeUrl"]
            source_file = self.ctx.web.get_file_by_server_relative_url(file_path)
            local_file_name = os.path.join(local_dir, os.path.basename(file_name))
            size = 0
            try:
                with open(local_file_name, "wb") as local_file:
                    source_file.download_session(local_file, print_download_progress).execute_query()
                size = os.path.getsize(local_file_name)
            except Exception as e:
                print(e)
                error = True
            end_time = time.time()
            print("Start time", start_time)
            print("End time", end_time)
            download_result.append({
                "filename": file_name,
                "filepath": file_path,
                "error": error,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "duration": str(end_time - start_time),
                "size": size
            })
        
        return download_result
