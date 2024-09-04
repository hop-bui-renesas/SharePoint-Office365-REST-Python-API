from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

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