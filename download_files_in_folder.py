import os
from client import SPClient

from client import get_sharepoint_context_using_user, download_SharePointFile

from utils import print_download_progress

import urllib.parse

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    sharepoint_url = "https://renesasgroup.sharepoint.com/sites/TransferofInformationTOIBroadcastChannel"
    username = os.environ["user_id"]
    password = os.environ["password"]
    
    ctx = get_sharepoint_context_using_user(sharepoint_url, username, password)

    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    server_relative_url = web.properties['ServerRelativeUrl']

    print("server relative url", server_relative_url)

    folder_path = "Shared%20Documents/TOI%20Session%20Archive/"

    folder_server_relative_url = server_relative_url + folder_path

    # Get the folder by its server-relative URL
    root = ctx.web.get_folder_by_server_relative_url(folder_server_relative_url)
    ctx.load(root)
    ctx.execute_query()

    folders = root.folders
    ctx.load(folders)
    ctx.execute_query()

    for i, folder in enumerate(folders):
        print(i, "Folder path:", folder)
        print(i, "Folder properties:", folder.properties)

    files = root.files
    ctx.load(files)
    ctx.execute_query()

    for i, file in enumerate(files):
        print(i, "File path: ", file)
    
    rel_path_to_file = folder_path + urllib.parse.quote(file.properties["Name"]).strip()

    print(rel_path_to_file)

    saved_path = "./saved"

    source_file = ctx.web.get_file_by_server_relative_url(rel_path_to_file)
    local_file_name = os.path.join(saved_path, os.path.basename(file.properties["Name"]))

    with open(local_file_name, "wb") as local_file:
        source_file.download_session(local_file, print_download_progress).execute_query()