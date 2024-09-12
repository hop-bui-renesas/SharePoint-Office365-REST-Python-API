import os
import requests
import time
import json

FOLDER_ENDPOINT = "http://localhost:8000/folders"
FILES_ENDPOINT = "http://localhost:8000/files"

LOCAL_DIR = "saved/"

if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

folder_name = "Shared Documents/TOI Session Archive"

all_folders = []
all_files = []

def get_folders_files_recursively(folder_name):
    payload = {
        "folder_path": folder_name,
        "recursive": False
    }
    print("Getting folders and files in", folder_name)
    n_retries = 0
    while True:
        try:
            response = requests.post(FOLDER_ENDPOINT, json=payload)
            folders = response.json()["folders"]
            all_folders.extend(folders)
            break
        except Exception as e:
            print(e)
            n_retries += 1
            time.sleep(1)
            if n_retries >= 3:
                break
    for folder in folders:
        sub_folder_name = folder["ServerRelativeUrl"].replace("/sites/TransferofInformationTOIBroadcastChannel/", "")
        get_folders_files_recursively(sub_folder_name)

    payload = {
        "folder_path": folder_name,
        "recursive": False,
        "is_download": True,
        "local_dir": "saved/"
    }
    response = requests.post(FILES_ENDPOINT, json=payload)
    files = response.json()["files"]
    print("Number of files", len(files))
    all_files.extend(files)

start = time.perf_counter()
get_folders_files_recursively(folder_name)
end = time.perf_counter()

print("Est time", end-start)

with open('folders.json', 'w', encoding='utf-8') as f:
    json.dump(all_folders, f, ensure_ascii=False, indent=4)

with open('files.json', 'w', encoding='utf-8') as f:
    json.dump(all_files, f, ensure_ascii=False, indent=4)