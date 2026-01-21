import requests
from bs4 import UnicodeDammit

def download_file(path, save_path):
    url = f"https://raw.githubusercontent.com/DND5eChm/DND5e_chm/main/{path}"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    bytes_data = response.content
    dammit = UnicodeDammit(bytes_data, is_html=True)
    if not dammit.unicode_markup:
        raise UnicodeDecodeError("Failed to detect encoding")

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(dammit.unicode_markup)