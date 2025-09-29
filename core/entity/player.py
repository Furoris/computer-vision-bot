class Player:
    def __init__(self, level: int = 1, hp: int = 100, mana: int = 0,
                 soul: int = 100, capacity: int = 0, speed: int = 0,
                 food: str = "00:00"):
        self.level = level
        self.hp = hp
        self.mana = mana
        self.soul = soul
        self.capacity = capacity
        self.speed = speed
        self.food = food  # MM:SS

    def __repr__(self):
        return (f"Player(Level={self.level}, HP={self.hp}, Mana={self.mana}, "
                f"Soul={self.soul}, Cap={self.capacity}, Speed={self.speed}, "
                f"Food='{self.food}')")

    def update_stat(self, stat_name: str, value):
        if not hasattr(self, stat_name):
            raise AttributeError(f"No stat '{stat_name}' in Player")
        setattr(self, stat_name, value)

    def to_dict(self):
        return {
            "level": self.level,
            "hp": self.hp,
            "mana": self.mana,
            "soul": self.soul,
            "capacity": self.capacity,
            "speed": self.speed,
            "food": self.food,
        }

    def pretty_print(self):
        print(f"Level     : {self.level}")
        print(f"HP        : {self.hp}")
        print(f"Mana      : {self.mana}")
        print(f"Soul Pts  : {self.soul}")
        print(f"Capacity  : {self.capacity}")
        print(f"Speed     : {self.speed}")
        print(f"Food Timer: {self.food}")