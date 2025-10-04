from typing import Optional

class Player:
    def __init__(self,
                 level: Optional[int] = None,
                 hp: Optional[int] = None,
                 mana: Optional[int] = None,
                 sp: Optional[int] = None,
                 cap: Optional[int] = None,
                 speed: Optional[int] = None,
                 food: Optional[str] = None):
        self.level = level
        self.hp = hp
        self.mana = mana
        self.sp = sp
        self.cap = cap
        self.speed = speed
        self.food = food  # MM:SS

    def update_stat(self, stat_name: str, value):
        if not hasattr(self, stat_name):
            raise AttributeError(f"No stat '{stat_name}' in Player")
        setattr(self, stat_name, value)

    def to_dict(self):
        return {
            "level": self.level,
            "hp": self.hp,
            "mana": self.mana,
            "sp": self.sp,
            "cap": self.cap,
            "speed": self.speed,
            "food": self.food,
        }

    def pretty_print(self):
        print(f"Level     : {self.level}")
        print(f"HP        : {self.hp}")
        print(f"Mana      : {self.mana}")
        print(f"SP        : {self.sp}")
        print(f"Cap       : {self.cap}")
        print(f"Speed     : {self.speed}")
        print(f"Food Timer: {self.food}")