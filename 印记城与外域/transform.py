from schemas import *
from utils import get_klass, get_level, get_magic_school, clean_soup_whitespace
from bs4 import BeautifulSoup, Tag
from bs4 import PageElement
import re

def deal_with_klass_line(klass_line: str) -> tuple[bool, list[KlassWithExtraInfo]]:
    # 先根据“；”分割
    klass_parts = [part.strip() for part in klass_line.split('；')]
    
    is_ritual = False
    klass_list: list[KlassWithExtraInfo] = []

    for part in klass_parts:
        if part == "仪式":
            is_ritual = True
            continue
        if '：' in part:
            # 包含来源信息
            source_info, klasses_info = part.split('：', maxsplit=1)
            source = source_info.strip()
            for klass_zh in klasses_info.split('、'):
                klass = get_klass(klass_zh.strip())
                klass_list.append(KlassWithExtraInfo(klass=klass, source=source))
        else:
            # 不包含来源信息
            for klass_zh in part.split('、'):
                klass = get_klass(klass_zh.strip())
                klass_list.append(KlassWithExtraInfo(klass=klass, source=None))
    return is_ritual, klass_list

def deal_with_material_line(material_line: str) -> tuple[bool, bool, str | None]:
    material_pattern = re.compile(r"M\s*[（\(](.*?)[）\)]")
    
    # 先处理材料成分
    match = material_pattern.search(material_line)
    material = match.group(1) if match else None

    # 处理言语和姿势成分
    text_for_flags = material_pattern.sub("", material_line)
    need_verbal = 'V' in text_for_flags
    need_somatic = 'S' in text_for_flags
    return need_verbal, need_somatic, material

def deal_with_duration_line(duration_line: str) -> tuple[bool, str]:
    concentration_pattern = re.compile(r"^专注，\s*(.*)$")
    match = concentration_pattern.match(duration_line)
    if match:
        need_concentration = True
        duration = match.group(1).strip()
    else:
        need_concentration = False
        duration = duration_line.strip()
    return need_concentration, duration

def transform_spell_from_html_block(html_block: list[PageElement]) -> Spell:
    # 提取中文名称和英文名称
    header = html_block[0]
    full_title_parts = header.get_text().strip().split('｜')
    name_zh = full_title_parts[0].strip()
    name_en = full_title_parts[1].strip()
    
    # 处理剩下的 HTML 块内容
    details = []
    for element in html_block[2:]:
        if isinstance(element, str):
            continue
        details.extend(element.contents)
    
    
    # 得到第一个标签下的所有文本内容
    first_tag_text = details[0].get_text().replace('（', ' ').replace('）', ' ').strip().split(' ', maxsplit=2)
    if first_tag_text[1].strip() == "戏法":
        level = get_level(first_tag_text[1].strip())
        school = get_magic_school(first_tag_text[0].strip())
    else:
        level = get_level(first_tag_text[0].strip())
        school = get_magic_school(first_tag_text[1].strip())
    is_ritual, class_list = deal_with_klass_line(first_tag_text[2].strip())

    current_index = 1
    # 找到包含施法时间的标签的下一个标签
    while current_index < len(details):
        tag_text = details[current_index].get_text().strip()
        if tag_text.startswith("施法时间："):
            break
        current_index += 1
    else:
        raise ValueError(f"未找到施法时间标签，法术名称：'{name_zh}'")
    current_index += 1
    casting_time = details[current_index].strip()
    current_index += 1

    # 找到包含施法范围的标签的下一个标签
    while current_index < len(details):
        tag_text = details[current_index].get_text().strip()
        if tag_text.startswith("施法距离："):
            break
        current_index += 1
    else:
        raise ValueError(f"未找到施法范围标签，法术名称：'{name_zh}'")
    current_index += 1
    spell_range = details[current_index].strip()
    current_index += 1

    # 找到包含法术成分的标签的下一个标签
    while current_index < len(details):
        tag_text = details[current_index].get_text().strip()
        if tag_text.startswith("法术成分："):
            break
        current_index += 1
    else:
        raise ValueError(f"未找到法术成分标签，法术名称：'{name_zh}'")
    current_index += 1
    need_verbal, need_somatic, material = deal_with_material_line(details[current_index].get_text().strip())
    current_index += 1
    
    # 找到包含持续时间的标签的下一个标签
    while current_index < len(details):
        tag_text = details[current_index].get_text().strip()
        if tag_text.startswith("持续时间："):
            break
        current_index += 1
    else:
        raise ValueError(f"未找到持续时间标签，法术名称：'{name_zh}'")
    current_index += 1
    need_concentration, duration = deal_with_duration_line(details[current_index].get_text().strip())
    current_index += 1

    # 如果当前内容是<br/>，跳过
    if details[current_index].name == 'br':
        current_index += 1

    # 提取描述内容，直到下一个 h4 标签
    html_parts = []
    for element in details[current_index:]:
        if getattr(element, 'name', None) == 'h4':
            break
        html_parts.append(str(element))
        if isinstance(element, Tag):
            # A. 移除当前顶层标签的 class
            element.attrs.pop('class', None)
            
            # B. 递归移除所有子孙标签的 class
            for child in element.find_all(True):
                child.attrs.pop('class', None)
    description = "".join(html_parts).strip()
    
    return Spell(
        name=name_zh,
        english_name=name_en,
        level=level,
        school=school,
        class_list=class_list,
        is_ritual=is_ritual,
        casting_time=casting_time,
        spell_range=spell_range,
        need_verbal=need_verbal,
        need_somatic=need_somatic,
        material=material,
        need_concentration=need_concentration,
        duration=duration,
        description=description,
        source=Source.SO,
    )

def transform_single_file(file_path: str) -> list[Spell]:
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(content, 'html.parser')
    clean_soup_whitespace(soup)
    all_spells = []

    # 先找到所有 H4 标签，并根据H4标签划分法术
    header_tags = soup.find_all('h4')
    for header in header_tags:
        # 统计当前 H4 标签以及其后面的所有兄弟节点，直到下一个 H4 标签
        html_block = [header]
        for sibling in header.next_siblings:
            if sibling.name == 'h4':
                break
            html_block.append(sibling)
        all_spells.append(transform_spell_from_html_block(html_block))

    return all_spells

def transform() -> list[Spell]:
    import os
    print("[Module] 正在转化：印记城与外域")
    # 遍历 玩家手册/raw 目录下的所有文件
    filename = os.path.join(os.path.dirname(__file__), "raw", "法术详述.htm")
    return transform_single_file(filename)
