from .klass import KlassWithExtraInfo
from .school import MagicSchool
from .source import Source
from dataclasses import dataclass, field
import hashlib

def _generate_spell_id(name: str, english_name: str, source: Source) -> str:
    h = hashlib.shake_128()
    def _update_field(val: str):
        val_bytes = val.encode('utf-8')
        h.update(str(len(val_bytes)).encode('ascii'))
        h.update(b':') 
        h.update(val_bytes)

    _update_field(name)
    _update_field(english_name)
    _update_field(source.name)
    
    return h.hexdigest(8)

@dataclass(frozen=True, slots=True)
class Spell:
    id: str = field(init=False)             # 法术唯一标识符
    name: str                               # 法术名称
    english_name: str                       # 法术英文名称
    level: int                              # 法术等级，0为戏法
    school: MagicSchool                     # 魔法学派
    class_list: list[KlassWithExtraInfo]    # 可使用该法术的职业列表
    is_ritual: bool                         # 是否为仪式法术
    casting_time: str                       # 施法时间
    spell_range: str                        # 施法范围
    need_verbal: bool                       # 法术成分：言语
    need_somatic: bool                      # 法术成分：姿势
    material: str | None                    # 法术成分：材料
    need_concentration: bool                # 是否需要专注
    duration: str                           # 持续时间
    description: str                        # 法术描述
    source: Source                          # 法术来源
    is_legacy: bool = False                 # 是否已经过时

    def __post_init__(self):
        # 通过name, english_name, source生成唯一id
        id = _generate_spell_id(self.name, self.english_name, self.source)
        object.__setattr__(self, 'id', id)

    def to_custom_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "english_name": self.english_name,
            "level": self.level,
            "school": self.school.value,
            "class_list": [{"class":klass.klass.value, "source":klass.source} for klass in self.class_list],
            "is_ritual": self.is_ritual,
            "casting_time": self.casting_time,
            "range": self.spell_range,
            "need_verbal": self.need_verbal,
            "need_somatic": self.need_somatic,
            "material": self.material,
            "need_concentration": self.need_concentration,
            "duration": self.duration,
            "description": self.description,
            "source": self.source.value,
            "is_legacy": self.is_legacy,
        }
    
    def to_json(self) -> str:
        import json
        return json.dumps(self.to_custom_dict(), ensure_ascii=False, indent=None)