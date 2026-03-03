from utils import download_file
import os

def download(redownload: bool):
    print("[Module] 正在下载：被遗忘的国度")
    local_path = "被遗忘的国度/raw/法术详述.htm"
    remote_path = "被遗忘的国度/费伦英雄/第五章/新法术.htm"
    if not redownload and os.path.exists(local_path):
        return
    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))
    download_file(remote_path, local_path)

if __name__ == "__main__":
    download(redownload=True)