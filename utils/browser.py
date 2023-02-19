from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = 'chromedriver_win32'
CHROMEDRIVER_PATH = ROOT_PATH / 'bin'/CHROMEDRIVER_NAME


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()
    chrome_service = Service(executable_path='CHROMEDRIVER_PATH')
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    browser = make_chrome_browser()
    browser.get(
        'https://www.workana.com/jobs?category=it-programming&language=pt')
    sleep(10)
