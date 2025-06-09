"""
    The script of automatic course selection in the original xk website page.

    Last updated: 2025.6.9
"""
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import myLog as log
import argparse
import time
import os
from webdriver_manager.chrome import ChromeDriverManager    # auto update WebDriver

TIMEOUT = 1.2

Id = log.read_json('UserId')
Pwd = log.read_json('PassWd')
url = log.read_json('url')

COLUMN = 'general'
columns = {
    'common':   '//*[@id="cvPageHeadTab"]/li[2]/a',
    'general':  '//*[@id="course-main"]/div[1]/div[4]/div[1]',
    'science':  '//*[@id="course-main"]/div[1]/div[4]/div[2]',
    'public':   '//*[@id="course-main"]/div[1]/div[4]/div[3]',
    'sport':    '//*[@id="cvPageHeadTab"]/li[5]/a',
    'favorite': '//*[@id="cvPageHeadTab"]/li[8]/a'
}

search = '//*[@id="course-main"]/div[1]/div[3]/input'
term = '/html/body/div[4]/div[2]/div[1]/div/div/table/tbody/tr[2]/td[1]/div/input'
filter_0 = '//*[@id="course-main"]/div[2]/div[1]/div[1]/div/div[2]'
filter_1 = '//*[@id="course-main"]/div[2]/div[1]/div[1]/div/div[3]'
switch = '//span[text()="切换"]'
xl_campus = '/html/body/ul/li[3]/div'
final_ensure = '//*[@id="cvDialog"]/div[2]/div[2]/div[1]'

class ClickException(Exception):
    """
    Click Exception, raised while the website has been refreshed
    up to 3 times, but the button still not clickable or even unfoundable.
    """
    def __init__(self, button=''):
        self.msg = 'Click Failed.  ' + button
    def __str__(self):
        return self.msg


def init_driver(potato=False):
    """
    Initialize and return a Selenium Chrome WebDriver instance.

    This function sets up a Chrome WebDriver with customized options
    It uses `webdriver-manager` to 
    automatically download and manage the correct version of ChromeDriver.

    Args:
        potato (bool): Use PotatoPlus extension (`Ture`) or not (`False`).
                       If `True`, enables loading from a persistent Chrome user data
                       directory (used to keep login states, extensions, etc.).
    """
    opts = Options()
    opts.add_argument('--disable-gpu')
    opts.add_argument('--disable-application-cache')
    opts.add_argument('--disk-cache-size=0')
    
    driver_pt = os.path.join('.', 'webDriver')
    cache_pt = os.path.join('.', 'webDriver', 'user-data')

    # absolute path
    driver_pt = os.path.abspath(driver_pt)
    cache_pt = os.path.abspath(cache_pt)

    if potato:
        opts.add_argument(f'user-data-dir={cache_pt}')

    srvc = Service(ChromeDriverManager().install())   # auto download WebDriver
    
    driver = webdriver.Chrome(service=srvc, options=opts)
    driver.set_window_size(800, 800)
    driver.set_window_position(10, 10)
    return driver
    

def try_to_click(driver, xpath, url, script=False, timeout=30):
    """
    Try to click the button found by xpath with the timeout setted up.
    On getting the Timeout Exception, refresh the web specified by url and retry.
    If timeout for up to 3 times, raise ClickException.
    """
    time, button = 0, None
    while True:
        try:
            # log.INFO(f'Looking through the button: {xpath}...')
            button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
        except TimeoutException:
            if time < 3:
                log.WARN(f'Refresh website at {time + 1} time(s).')
                # driver.get(url)
                driver.refresh()
                time += 1
                continue
        break

    if button is not None:
        if script:
            driver.execute_script("arguments[0].click();", button)
        else:
            button.click()
    else:
        raise ClickException(xpath)
    

def refresh_while_seeking(driver):
    try:
        try_to_click(driver, '//button[text()="刷新"]', url)
    except ClickException as e:
        log.FAIL(f'Failed to click some button:\n{e}')
        driver.quit()
        exit()


def refresh_once_getting(driver):
    driver.refresh()
    if COLUMN != 'favorite':
        # 点击切换校区
        switch_campus = WebDriverWait(driver, timeout=30).until(
            EC.element_to_be_clickable((By.XPATH, switch))
        )
        driver.execute_script("arguments[0].click();", switch_campus)
        try:
            try_to_click(driver, xl_campus, url)    # 选择仙林
            time.sleep(0.6)
            try_to_click(driver, filter_0, url)
            # time.sleep(0.2)
            try_to_click(driver, filter_1, url)
        except ClickException as e:
            log.FAIL(f'Failed to click some button:\n{e}')
            driver.quit()
            exit()


def init_xk_page(driver, myId, myPwd):
    log.INFO('Loading page...')

    try:
        driver.get(url)
    except Exception:
        log.FAIL('Failed to load njuxk page, please check your connection first.')
        driver.quit()
        exit()

    inputId = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="loginName"]'))
    )
    inputId.clear()
    inputId.send_keys(myId)
    inputPsw = WebDriverWait(driver, timeout=30).until(
        EC.element_to_be_clickable((By.XPATH, '//input[@id="loginPwd"]'))
    )
    inputPsw.clear()
    inputPsw.send_keys(myPwd)
    log.INFO('Entering username & password')
    # code = log.CONF('Give me your VRcode:')
    # vrcode_input = WebDriverWait(driver, timeout=30).until(
    #     EC.element_to_be_clickable((By.XPATH, '//input[@id="verifyCode"]'))
    # )
    # vrcode_input.clear()
    # vrcode_input.send_keys(code)
    # loginBtn = WebDriverWait(driver, timeout=30).until(
    #     EC.element_to_be_clickable((By.XPATH, '//button[@id="studentLoginBtn"]'))
    # )
    # loginBtn.click()
    # log.INFO('Logged in.')
    log.WARN('Please complete the verification code by yourself...')
    # term_button = WebDriverWait(driver, timeout=30).until(
    #     EC.element_to_be_clickable((By.XPATH, term))
    # )
    # term_button.click()
    # ensure_button = WebDriverWait(driver, timeout=30).until(
    #     EC.element_to_be_clickable((By.XPATH, '//button[text()="确认"]'))
    # )
    # ensure_button.click()
    start_button = WebDriverWait(driver, timeout=300).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="开始选课"]'))
    )
    start_button.click()
    log.INFO('Starting...')


def choose_column(driver, column: str):
    """
    Choose the column in the NJU-xk main-page.
    """
    log.INFO(f'Trying to choose column "{column}"')
    try:
        if column in ['general', 'science', 'public']:
            time.sleep(0.8)
            try_to_click(driver, columns['common'], url)
        time.sleep(0.8)
        try_to_click(driver, columns[column], url)
        time.sleep(0.8)

    except ClickException as e:
        log.FAIL(f'Failed to click some button:\n{e}')
        driver.quit()
        exit()


def main():
    driver = init_driver()
    init_xk_page(driver, Id, Pwd)
    
    choose_column(driver, COLUMN)

    if COLUMN != 'favorite':
        # 点击切换校区
        switch_campus = WebDriverWait(driver, timeout=30).until(
            EC.element_to_be_clickable((By.XPATH, switch))
        )
        driver.execute_script("arguments[0].click();", switch_campus)
        try_to_click(driver, xl_campus, url)    # 选择仙林
        time.sleep(0.6)
        try_to_click(driver, filter_0, url)
        # time.sleep(0.2)
        try_to_click(driver, filter_1, url)
        time.sleep(0.6)

    refresh = 0
    while True:
        try:
            if refresh >= 100 and refresh % 100 == 0 and COLUMN != 'favorite':
                time.sleep(0.8)
                try_to_click(driver, filter_0, url)
                time.sleep(0.8)
                try_to_click(driver, filter_0, url)
                time.sleep(0.8)

            select = WebDriverWait(driver, timeout=TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="选择"][1]'))
            )
            select.click()
        except TimeoutException:
            refresh += 1
            log.INFO(f'Refreshed at {refresh} times...', cover=True)
            refresh_while_seeking(driver)
            time.sleep(0.2)
            continue

        try_to_click(driver, final_ensure, url)
        print()
        log.DONE('Got one!')
        time.sleep(1)
        refresh = 0
        log.INFO(f'Refreshed at {refresh} times...', cover=True)
        refresh_once_getting(driver)
        # break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', type=float, default=1.2)
    parser.add_argument('-c', '--column', type=str, default='general')
    args = parser.parse_args()
    TIMEOUT, COLUMN = args.timeout, args.column

    # check parameters inpupt
    if COLUMN not in columns.keys() or TIMEOUT <= 0:
        log.FAIL('Invalid parameter(s) entered by user!')
        exit()

    try:
        main()
    except KeyboardInterrupt:
        log.INFO('Interrupted end.')
        exit()