"""
    Clicks-xk, used in combination with the Small Potato plugin.

    Last updated: 2025.2.28
"""
from selenium import webdriver
from selenium.common import TimeoutException, JavascriptException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import myLog as log
import clicks_xk as click
import argparse
import time

TIMEOUT = 1.2
COLUMN = 'favorite'

Id = log.read_json('UserId')
Pwd = log.read_json('PassWd')
url = log.read_json('url')

search = '//*[@id="course-main"]/div[1]/div[3]/input'
term = '/html/body/div[4]/div[2]/div[1]/div/div/table/tbody/tr[2]/td[1]/div/input'
# dropdown = '/html/body/div[1]/header/div[3]/div/div[3]/div[1]'
# potato = '//div[text()="启用 PotatoPlus (Beta)"]'
# auto = '//div[text()="手动"]'
filter_full = '//*[@id="pjw-filter-avail-switch"]/div[2]/div/div[2]'
filter_chosen = '//*[@id="pjw-deselect-switch-box"]/label'
filter_conflict = '//*[@id="pjw-filter-hours-switch"]/div[2]/div/div[1]'
select_first =  '//*[@id="course-main"]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[3]/div[1]/button/div[1]'
switch = '//span[text()="切换"]'
xl_campus = '/html/body/ul/li[3]/div'

def main():
    driver = click.init_driver(potato=True)
    click.init_xk_page(driver, Id, Pwd)

    click.choose_column(driver, COLUMN)
    # click.try_to_click(driver, dropdown, url)
    # click.try_to_click(driver, potato, url)
    # 点击切换校区
    click.try_to_click(driver, switch, url, script=True)
    click.try_to_click(driver, xl_campus, url)    # 选择仙林
    click.try_to_click(driver, filter_full, url, script=True)    # 过滤已满
    click.try_to_click(driver, filter_chosen, url, script=True)  # 过滤已选
    click.try_to_click(driver, filter_conflict, url, script=True)   # 过滤冲突
    # click.try_to_click(driver, auto, url)           # 自动
    if COLUMN in ['general', 'science', 'public']:
        log.CONF('Press Enter to confirm to continue...')
    retry = 0
    while True:
        try:
            select = WebDriverWait(driver, timeout=TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, select_first))
            )
            driver.execute_script(f"arguments[0].click();", select)
            print()
            log.DONE('Got one!')
            retry = 0
            time.sleep(1.2)
            
        except KeyboardInterrupt:
            print()
            log.INFO('Interrupted end.')
            exit()
        except TimeoutException:
            retry += 1
            log.INFO(f'Retry for {retry} times...', cover=True)
        except JavascriptException:
            retry += 1
            log.INFO(f'Retry for {retry} times...', cover=True)

        click.refresh_while_seeking(driver)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', type=float, default=1.2)
    parser.add_argument('-c', '--column', type=str, default='favorite')
    args = parser.parse_args()
    TIMEOUT, COLUMN = args.timeout, args.column

    # check
    if COLUMN not in click.columns.keys() or TIMEOUT <= 0:
        log.FAIL('Invalid parameter(s) entered by user!')
        exit()

    try:
        main()
    except KeyboardInterrupt:
        log.INFO('Interrupted end.')
        exit()