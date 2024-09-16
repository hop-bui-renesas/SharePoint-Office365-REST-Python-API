import argparse
import os
import time
import json

from client import SPClient

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("sharepoint_url")
USERNAME = os.environ["user_id"]
PASSWORD = os.environ["password"]

client = SPClient(url=URL, username=USERNAME, password=PASSWORD)

LOCAL_DIR = "saved/"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download files in a folder')
    parser.add_argument('--folder-name', type=str, help='Folder name')
    parser.add_argument('--local-dir', type=str, help='Local directory to save files')
    args = parser.parse_args()

    LOCAL_DIR = args.local_dir

    if not os.path.exists(LOCAL_DIR):
        os.makedirs(LOCAL_DIR)

    # folder_name = "Shared Documents/TOI Session Archive"
    folder_name = args.folder_name

    all_folders = []
    all_files = []
    all_download_results = []

    def get_folders_files_recursively(folder_name):
        print("Getting folders and files in", folder_name)
        n_retries = 0
        while True:
            try:
                folders = client.get_folders(folder_path=folder_name, recursive=False)
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

        files = client.get_files(folder_path=folder_name, recursive=False)
        download_result = client.download_files(files=files, local_dir=LOCAL_DIR)
        print("Number of files", len(files))
        all_files.extend(files)
        all_download_results.extend(download_result)

    start = time.perf_counter()
    get_folders_files_recursively(folder_name)
    end = time.perf_counter()

    print("Est time", end-start)

    with open('folders.json', 'w', encoding='utf-8') as f:
        json_data = json.dumps(all_folders, ensure_ascii=False, indent=4, default=str)
        f.write(json_data)

    with open('files.json', 'w', encoding='utf-8') as f:
        json_data = json.dumps(all_files, ensure_ascii=False, indent=4, default=str)
        f.write(json_data)

    with open('download_results.json', 'w', encoding='utf-8') as f:
        json_data = json.dumps(all_download_results, ensure_ascii=False, indent=4, default=str)
        f.write(json_data)