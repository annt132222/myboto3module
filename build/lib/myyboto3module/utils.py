import os
import json
from time import strftime, localtime

def create_metadata(file_name):
    upload_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
    metadata = {
        "file_name": file_name,
        "upload_time": upload_time
    }
    folder = "data"
    if not os.path.exists(folder):
        os.makedirs(folder)
    metadata_filename = os.path.join(folder, f"{file_name}_metadata.json")
    with open(metadata_filename, "w", encoding="utf-8") as meta_file:
        json.dump(metadata, meta_file, ensure_ascii=False, indent=4)
    print(f"Metadata saved to {metadata_filename}")
