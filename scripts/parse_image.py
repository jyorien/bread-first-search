import base64
import os
import requests
def base64_to_img(b64, folder_path, file_name):
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{file_name}.jpg")
    try:
        if not b64.startswith("data:image"):
            return False
        header, data = b64.split(",", 1)
        type = header.split(";")[0].split(":")[1]
        if type != "image/png" and type != "image/jpeg":
            return False
        print(f"type: {type}")
        
        img_data = base64.b64decode(data)

        with open(file_path, "wb") as file:
            file.write(img_data)
    except Exception as e:
        print(f"ERROR: {e}")
        print("Skipping...")
        return False

    return True
    
def url_to_img(url, folder_path, file_name):
    try:
        res = requests.get(url, stream=True)
        res.raise_for_status()
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{file_name}.jpg")
        with open(file_path, "wb") as file:
            for chunk in res.iter_content(1024):
                file.write(chunk)
            return True
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
        return False