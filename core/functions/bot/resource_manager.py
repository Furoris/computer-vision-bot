from core.functions.input import key_input

class ResourceManager:
    def __init__(self, config):
        self.config = config

    def mana_burn(self, player):
        try:
            mana = int(player.mana) if player.mana is not None else 0
            if mana > int(self.config.get('bot_config', 'mana_burn')):
                key_input.press(self.config.get('bot_config', 'mana_burn_key'))

                return True

            return False
        except ValueError:
            print("Could not convert mana:", player.mana)

    def heal(self, player):
        try:
            hp = int(player.hp) if player.hp is not None else 0
            mana = int(player.mana) if player.mana is not None else 0
            if hp < int(self.config.get('bot_config', 'hp_critical')):
                key_input.press(self.config.get('bot_config', 'hp_potion_key'))

                return True
            elif hp < int(self.config.get('bot_config', 'hp_low')) and mana > int(self.config.get('bot_config', 'hp_spell_mana')):
                key_input.press(self.config.get('bot_config', 'hp_spell_key'))

                return True

            return False
        except ValueError:
            print("Could not convert hp or mana:", player.hp, player.mana)