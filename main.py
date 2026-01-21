from schemas import Spell
import importlib

BOOK_LIST = [
    '玩家手册', # PHB14
    '玩家手册2024', # PHB24
    '珊娜萨的万事指南', # XGE
    '塔莎的万事坩埚', # TCE
    '费资本的巨龙宝库', # FTD
    '万象无常书', # BMT
    '拉尼卡公会长指南', # GGR
    '艾奎兹玄有限责任公司', # AI 
    '斯翠海文：混沌研习', # SCC
    '星界冒险者指南', #AAG
    '印记城与外域', # SO
    '模组法术', # MODULE
]
    

def list_to_json(spells: list[Spell]) -> str:
    import json
    return json.dumps(
        [spell.to_custom_dict() for spell in spells],
        ensure_ascii=False
    )

def file_size_and_gzip_size(path: str) -> None:
    import gzip, os, io, humanize

    raw_size = os.path.getsize(path)
    with open(path, "rb") as f:
        raw_data = f.read()
    buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
        gz.write(raw_data)
    gzipped_size = buffer.tell()

    organize_size_h = humanize.naturalsize(raw_size, binary=True, format="%.2f")
    gzipped_size_h  = humanize.naturalsize(gzipped_size, binary=True, format="%.2f")

    # 3. 输出结果
    print(f"File: {os.path.abspath(path)}")
    print(f"Original size : {organize_size_h}")
    print(f"Gzip size     : {gzipped_size_h}")
    print(f"Compression   : {gzipped_size / raw_size:.2%}")

def download(redownload: bool) -> None:
    for book in BOOK_LIST:
        module = importlib.import_module(f"{book}.download")
        module.download(redownload=redownload)

def transform(path: str) -> None:
    list_of_lists = []
    for book in BOOK_LIST:
        module = importlib.import_module(f"{book}.transform")
        spells = module.transform()
        list_of_lists.append(spells)
    final_list = [spell for sublist in list_of_lists for spell in sublist]
    # 检查一下会不是有重复id的法术（这是不可能的）
    id_set = set()
    for spell in final_list:
        if spell.id in id_set:
            raise ValueError(f"Duplicate spell id found: {spell.id} for spell {spell.name}")
        id_set.add(spell.id)
    with open(path, "w", encoding="utf-8") as f:
        f.write(list_to_json(final_list))
    file_size_and_gzip_size(path)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="DND5e Spells Data Transformer")
    parser.add_argument('--download', action='store_true', help='从不全书仓库下载数据文件')
    parser.add_argument('--transform', action='store_true', help='转化为JSON格式并输出文件')
    parser.add_argument('--redownload', action='store_true', help='下载文件时强制重新下载已存在的文件')
    parser.add_argument('--path', type=str, default='./dnd5_spells.json', help='输出文件路径，默认为 ./dnd5_spells.json')
    args = parser.parse_args()

    if not args.download and not args.transform:
        parser.print_help()
        return

    if args.download:
        download(redownload=args.redownload)
    if args.transform:
        transform(path=args.path)

if __name__ == "__main__":
    main()
