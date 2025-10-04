import time
import cv2
import pygetwindow as gw
from core.entities.player import Player
import core.functions.cv.get_screen_data as get_screen_data
import core.functions.cv.capture_screen as screen
import keyboard
from core.config.config import Config
import os
from core.functions.input import key_input

CONFIG = Config()

def get_game_bbox():
    wins = [w for w in gw.getAllTitles() if CONFIG.get('app','game_window_title').lower() in w.lower()]
    if not wins:
        raise RuntimeError('Game window not found. Launch the game and set GAME_WINDOW_TITLE.')
    win = gw.getWindowsWithTitle(wins[0])[0]
    if win.isMinimized:
        win.restore()
        time.sleep(0.5)
    win.activate()
    time.sleep(0.1)


class Bot:
    def __init__(self):
        get_game_bbox()
        self.last_action = 0.0

    def tick(self, player):
        frame = screen.get_frame()
        #frame = cv2.imread('assets/templates/test_frame.png')

        for attribute in vars(player):
            value = get_screen_data.get_frame_line_data(frame, attribute)
            player.update_stat(attribute, value)

        os.system('cls')
        player.pretty_print()

        try:
            mana = int(player.mana) if player.mana is not None else 0
            if mana > 120:
                key_input.press('0')
        except ValueError:
            print("Could not convert mana:", player.mana)


def main():
    bot = Bot()
    player = Player()
    try:
        while True:
            t0 = time.time()
            bot.tick(player)
            dt = time.time() - t0
            time.sleep(max(0, 1.0 / CONFIG.get('app','loop_hz', 'float') - dt))
            if keyboard.is_pressed('esc'):
                print('Exiting script...')
                break
    except KeyboardInterrupt:
        print('Stopped.')


if __name__ == '__main__':
    main()
