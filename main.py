import time
import cv2
from core.entities.player import Player
from core.entities.bot import Bot
import core.functions.cv.get_screen_data as get_screen_data
import core.functions.cv.capture_screen as screen
import keyboard
from core.config.config import Config
import os

CONFIG = Config()

def tick(player, bot):
    if bool(CONFIG.get('app','test_mode')):
        frame = cv2.imread('assets/templates/test_frame.png')
    else:
        frame = screen.get_frame()

    for attribute in vars(player):
        value = get_screen_data.get_frame_line_data(frame, attribute)
        player.update_stat(attribute, value)

    os.system('cls')
    player.pretty_print()
    bot.auto_resource_manager(player)

def main():
    player = Player()
    bot = Bot(CONFIG)

    try:
        while True:
            t0 = time.time()
            tick(player, bot)
            dt = time.time() - t0
            time.sleep(max(0, 1.0 / CONFIG.get('app','loop_hz', 'float') - dt))
            if keyboard.is_pressed('esc'):
                print('Exiting script...')
                break
    except KeyboardInterrupt:
        print('Stopped.')

if __name__ == '__main__':
    main()
