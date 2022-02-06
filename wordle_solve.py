import json
import re
import sys
from datetime import date

import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import util


def retrieve_js():
    response = requests.get('https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js')
    return response.text


def get_start_date(content: str):
    match = re.search(r'var\sHa=new\sDate\((?P<year>\d+),(?P<month>\d+),(?P<day>\d+),0,0,0,0\)', content)
    year = int(match.group('year'))
    month = int(match.group('month')) + 1
    day = int(match.group('day'))
    return date(year, month, day)


def get_word_list(content: str):
    match = re.search(r'var\sLa=(?P<word_list>\["\w+"(?:,"\w+")*])', content)
    return json.loads(match.group('word_list'))


def get_current_word(content: str):
    word_list = get_word_list(content)
    start_date = get_start_date(content)
    today = date.today()
    diff = (today - start_date).total_seconds() * 1000
    index = round(diff / 864e5) % len(word_list)
    return word_list[index]


def solve_wordle(word: str):
    driver = util.open_game('https://www.powerlanguage.co.uk/wordle/')
    game = WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, '/html/body/game-app')))
    ActionChains(driver).move_to_element_with_offset(game, 200, 200).click().perform()
    ActionChains(driver).send_keys(word, Keys.ENTER).perform()


if __name__ == '__main__':
    wordle_js = retrieve_js()
    wordle = get_current_word(wordle_js)
    solve_wordle(wordle)
    sys.exit(0)
