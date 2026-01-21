from schemas import *

SchoolMap = {
    "防护": MagicSchool.ABJURATION,
    "咒法": MagicSchool.CONJURATION,
    "预言": MagicSchool.DIVINATION,
    "惑控": MagicSchool.ENCHANTMENT,
    "塑能": MagicSchool.EVOCATION,
    "幻术": MagicSchool.ILLUSION,
    "死灵": MagicSchool.NECROMANCY,
    "变化": MagicSchool.TRANSMUTATION,
    "变化系": MagicSchool.TRANSMUTATION,
}

KlassMap = {
    "奇械师": Klass.ARTIFICER,
    "野蛮人": Klass.BARBARIAN,
    "吟游诗人": Klass.BARD,
    "牧师": Klass.CLERIC,
    "德鲁伊": Klass.DRUID,
    "战士": Klass.FIGHTER,
    "武僧": Klass.MONK,
    "圣武士": Klass.PALADIN,
    "游侠": Klass.RANGER,
    "游荡者": Klass.ROGUE,
    "术士": Klass.SORCERER,
    "契术师": Klass.WARLOCK,
    "魔契师": Klass.WARLOCK,
    "法师": Klass.WIZARD,
}

LevelMap = {
    "戏法": 0,
    "一环": 1,
    "二环": 2,
    "三环": 3,
    "四环": 4,
    "五环": 5,
    "六环": 6,
    "七环": 7,
    "八环": 8,
    "九环": 9,
}

def get_magic_school(zh_name: str) -> MagicSchool:
    if zh_name in SchoolMap:
        return SchoolMap[zh_name]
    raise ValueError(f"未知的魔法学派中文名称：'{zh_name}'")

def get_klass(zh_name: str) -> Klass:
    if zh_name in KlassMap:
        return KlassMap[zh_name]
    raise ValueError(f"未知的职业中文名称：'{zh_name}'")

def get_level(zh_name: str) -> int:
    if zh_name in LevelMap:
        return LevelMap[zh_name]
    raise ValueError(f"未知的法术等级中文名称：'{zh_name}'")