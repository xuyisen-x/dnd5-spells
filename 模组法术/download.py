from utils import download_file
from tqdm import tqdm
import os

file_list = [
    ("模组/冰风谷/新法术.html", "模组法术/raw/冰风谷.html"),
    ("模组/夸力许/新法术.html", "模组法术/raw/夸力许的失落实验室.html"),
]

def download(redownload: bool):
    print("[Module] 正在下载：模组法术")
    for remote_path, local_path in tqdm(file_list, desc="模组法术"):
        # 如果不强制重新下载，且文件已存在，则跳过下载
        if not redownload and os.path.exists(local_path):
            continue
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        download_file(remote_path, local_path)

if __name__ == "__main__":
    download(redownload=True)