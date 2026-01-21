from utils import download_file
import os

def download(redownload: bool):
    print("[Module] 正在下载：费资本的巨龙宝库")
    local_path = "费资本的巨龙宝库/raw/巨龙法术详述.htm"
    remote_path = "费资本的巨龙宝库/玩家选项/巨龙法术详述.htm"
    if not redownload and os.path.exists(local_path):
        return
    if not os.path.exists(os.path.dirname(local_path)):
        os.makedirs(os.path.dirname(local_path))
    download_file(remote_path, local_path)

if __name__ == "__main__":
    download(redownload=True)