from utils import download_file
from tqdm import tqdm
import os

file_list = [
    ("玩家手册/魔法/法术详述/戏法.html", "玩家手册/raw/戏法.html"),
    ("玩家手册/魔法/法术详述/1环.html", "玩家手册/raw/1环.html"),
    ("玩家手册/魔法/法术详述/2环.html", "玩家手册/raw/2环.html"),
    ("玩家手册/魔法/法术详述/3环.html", "玩家手册/raw/3环.html"),
    ("玩家手册/魔法/法术详述/4环.html", "玩家手册/raw/4环.html"),
    ("玩家手册/魔法/法术详述/5环.html", "玩家手册/raw/5环.html"),
    ("玩家手册/魔法/法术详述/6环.html", "玩家手册/raw/6环.html"),
    ("玩家手册/魔法/法术详述/7环.html", "玩家手册/raw/7环.html"),
    ("玩家手册/魔法/法术详述/8环.html", "玩家手册/raw/8环.html"),
    ("玩家手册/魔法/法术详述/9环.html", "玩家手册/raw/9环.html"),
]

def download(redownload: bool):
    print("[Module] 正在下载：玩家手册2014")
    for remote_path, local_path in tqdm(file_list, desc="玩家手册2014"):
        # 如果不强制重新下载，且文件已存在，则跳过下载
        if not redownload and os.path.exists(local_path):
            continue
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
        download_file(remote_path, local_path)

if __name__ == "__main__":
    download(redownload=True)