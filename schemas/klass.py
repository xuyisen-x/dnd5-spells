from enum import Enum
from dataclasses import dataclass

class Klass(Enum):
    ARTIFICER   = "artificer"   # 奇械师
    BARBARIAN   = "barbarian"   # 野蛮人
    BARD        = "bard"        # 吟游诗人
    CLERIC      = "cleric"      # 牧师
    DRUID       = "druid"       # 德鲁伊
    FIGHTER     = "fighter"     # 战士
    MONK        = "monk"        # 武僧
    PALADIN     = "paladin"     # 圣武士
    RANGER      = "ranger"      # 游侠
    ROGUE       = "rogue"       # 游荡者
    SORCERER    = "sorcerer"    # 术士
    WARLOCK     = "warlock"     # 契术师
    WIZARD      = "wizard"      # 法师

@dataclass(frozen=True, slots=True)
class KlassWithExtraInfo:
    klass: Klass
    source: str | None = None # 某些法术可能是在某个扩展中，拓展了某个职业的法术列表，需要记录来源，典型来源如：TCE

