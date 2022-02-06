import argparse
import json
import re
import sys

from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import util


def parse_arguments():
    parser = argparse.ArgumentParser()
    mode_list = ['main', 'mini', 'max', 'hex']
    parser.add_argument('--mode', '-m', default='main', choices=mode_list)
    return parser.parse_args()


def get_current_word(mode: str, driver: WebDriver):
    if mode in ['main', 'mini', 'max']:
        user_data = json.loads(driver.execute_script(f'return localStorage.getItem("saltong-user-data");'))
        return user_data[mode]['correctAnswer']


def input_answer(word: str, driver: WebDriver):
    ActionChains(driver).send_keys(word, Keys.ENTER).perform()


def solve_saltong_hex(driver: WebDriver):
    hex_data = json.loads(driver.execute_script(f'return localStorage.getItem("saltong-hex-data");'))
    dictionary_data = json.loads(driver.execute_script(f'return localStorage.getItem("saltong-dictionary");'))
    dictionary = dictionary_data['dictionary']
    longest_word = hex_data['rootWord']
    center_letter = hex_data['centerLetter']
    for letter_count, dict_word_list in dictionary.items():
        for word in dict_word_list:
            if re.match(f'^[{longest_word}]+$', word) and center_letter in word:
                input_answer(word, driver)


def solve_saltong(mode: str):
    driver = util.open_game(f'https://saltong.carldegs.com/{mode}')
    game = WebDriverWait(driver, 15).until(
        expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[3]')))
    ActionChains(driver).move_to_element(game).send_keys(Keys.ESCAPE).perform()
    if mode != 'hex':
        current_word = get_current_word(mode, driver)
        input_answer(current_word, driver)
    else:
        solve_saltong_hex(driver)


if __name__ == '__main__':
    saltong_mode = parse_arguments().mode
    solve_saltong(saltong_mode)
    sys.exit(0)
