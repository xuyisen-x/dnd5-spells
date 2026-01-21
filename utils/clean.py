import re
from bs4 import BeautifulSoup, NavigableString

def clean_soup_whitespace(soup: BeautifulSoup):
    """
    遍历 soup 中的每一个文本节点：
    1. 将换行符 \n 替换为空格
    2. 将非换行空格 \xa0 替换为空格
    3. 将连续的多个空格合并为 1 个
    """
    # soup.find_all(string=True) 会找到所有的文本节点 (NavigableString)
    for text_node in soup.find_all(string=True):
        if not isinstance(text_node, NavigableString):
            continue
        
        # 获取原始文本
        original_text = str(text_node)
        
        # 核心正则：\s+ 匹配所有空白字符（包括 \n, \r, \t, \f, 空格, \xa0）
        cleaned_text = re.sub(r'\s+', ' ', original_text)
        
        # 如果清洗后的文本变了，就替换掉原来的节点
        if original_text != cleaned_text:
            text_node.replace_with(cleaned_text)