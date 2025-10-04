import pygetwindow as gw
import time
from core.functions.bot.resource_manager import ResourceManager

class Bot:
    def __init__(self, config):
        self.config = config
        self.get_game_bbox()
        self.resource_manager = ResourceManager(config)

    def get_game_bbox(self):
        wins = [w for w in gw.getAllTitles() if self.config.get('app', 'game_window_title').lower() in w.lower()]
        if not wins:
            raise RuntimeError('Game window not found. Launch the game and set GAME_WINDOW_TITLE.')
        win = gw.getWindowsWithTitle(wins[0])[0]
        if win.isMinimized:
            win.restore()
            time.sleep(0.5)
        win.activate()
        time.sleep(0.1)

    def auto_resource_manager(self, player):
        if not self.resource_manager.heal(player):
            self.resource_manager.mana_burn(player)

