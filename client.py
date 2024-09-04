from datetime import datetime

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

import os

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

def get_sharepoint_context_using_user(url, username, password):
    try:
        # Initialize the client credentials
        user_credentials = UserCredential(username, password)

        # create client context object
        ctx = ClientContext(url).with_credentials(user_credentials)
        print(f"{datetime.now()}\t Authenticated successfully.")
        return ctx

    except Exception as e:
        print(f"{datetime.now()}\t Exception occurred: ", str(e))
        print(f"{datetime.now()}\t ------------------------------------ \n")

def download_SharePointFile(sharepoint_url, userID, password, saved_path, folder_in_sharepoint):
    try:
        #This function helps to download the sharepoint file to /tmp location , /tmp is driver local to cluster
        ctx = get_sharepoint_context_using_user(sharepoint_url, userID, password)
        
        # Get the server-relative URL of the web
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()
        server_relative_url = web.properties['ServerRelativeUrl']
        # print(server_relative_url)

        # Concatenate the server-relative URL with the folder path
        folder_server_relative_url = server_relative_url + folder_in_sharepoint
        print(f"{datetime.now()}\t SharePoint Relative URL: {folder_server_relative_url}")

        # Get the folder by its server-relative URL
        folder = ctx.web.get_folder_by_server_relative_url(folder_server_relative_url)
        ctx.load(folder)
        ctx.execute_query()
        # print(folder)

        # Get files in the folder
        files = folder.files
        ctx.load(files)
        ctx.execute_query()

        print(f"{datetime.now()}\t {len(files)} file(s) have identified in {folder_in_sharepoint}")
        
        for file in files:

            # if file.properties["Name"] in ['result2.csv','result.csv']:
            #     continue

            try:
                print(f"{datetime.now()}\t Processing - File Name: {file.properties['Name']}")

                # download csv from sharepoint to databricks volume
                print(f"{datetime.now()}\t Downloading {file.properties['Name']} to Databricks Volume...")
                rel_path_to_file = folder_in_sharepoint + file.properties["Name"]
                # print(rel_path_to_file)
                source_file = ctx.web.get_file_by_server_relative_path(rel_path_to_file)

                local_file_name = os.path.join(saved_path, os.path.basename(file.properties["Name"]))

                with open(local_file_name, "wb") as local_file:
                    source_file.download_session(local_file, print_download_progress).execute_query()

                print(f"{datetime.now()}\t [Completed] - {file.properties['Name']} has been downloaded to Databricks Volume: {local_file_name}")

                # # move/archive csv to archive path on sharepoint
                # print(f"{datetime.now()}\t Moving {file.properties['Name']} to archive folder on SharePoint...")
                # current_time = datetime.now()
                # new_file_name = f"{file.properties['Name'].split('.')[0]}_{current_time.strftime('%Y%m%d%H%M%S')}"
                # archive_file_path = f"{folder_server_relative_url}archive/{new_file_name}"
                # source_file.moveto(archive_file_path, 1)
                # ctx.execute_query()

                # print(f"{datetime.now()}\t [Completed] - {file.properties['Name']} moved to {archive_file_path} on SharePoint...")
                # print(f"{datetime.now()}\t Processing - File Name: {file.properties['Name']} - Completed!")
                # print(f"{datetime.now()}\t ------------------------------------ \n")
            
            except Exception as e:
                print(f"{datetime.now()}\t Exception occurred: ", str(e))
                print(f"{datetime.now()}\t ------------------------------------ \n")

        return files

    except Exception as e:
        print(f"{datetime.now()}\t Exception occurred: ", str(e))
        print(f"{datetime.now()}\t ----------------------")