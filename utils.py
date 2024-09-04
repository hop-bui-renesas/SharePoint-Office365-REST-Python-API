from datetime import datetime

def print_download_progress(offset):
    offset_mb = offset / 1024 / 1024
    print(f"{datetime.now()}\t Downloaded '{round(offset_mb,3)}' MB...")