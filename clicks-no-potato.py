"""
    The script WITHOUT PotatoPlus plugin, in the original xk website page.

    Last updated: 2025.9.1
"""
import sys
import subprocess

# check dependencies
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

print('[INFO]:  Checking the dependencies...')
ensure_package('selenium')
ensure_package('colorama')
ensure_package('filelock')
ensure_package('webdriver_manager')
print('[DONE]:  Dependency check done.')

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import myLog as log
import argparse
import time
import clicks

search = '//*[@id="course-main"]/div[1]/div[3]/input'
term = '/html/body/div[4]/div[2]/div[1]/div/div/table/tbody/tr[2]/td[1]/div/input'
filter_0 = '//*[@id="course-main"]/div[2]/div[1]/div[1]/div/div[2]'
filter_1 = '//*[@id="course-main"]/div[2]/div[1]/div[1]/div/div[3]'
switch = '//span[text()="切换"]'
final_ensure = '//*[@id="cvDialog"]/div[2]/div[2]/div[1]'

TIMEOUT = 1.2
COLUMN = 'general'


def refresh_once_getting(driver, url, campus):
    driver.refresh()
    if COLUMN != 'favorite':
        try:
            clicks.try_to_click(driver, switch, url, script=True)   # 点击切换校区
            time.sleep(0.3)
            clicks.try_to_click(driver, campus, url)                # 选择校区（需要传入校区 XPATH）
            time.sleep(0.3)
            clicks.try_to_click(driver, filter_0, url)
            time.sleep(0.6)
            clicks.try_to_click(driver, filter_1, url)
            time.sleep(1.2)
        except clicks.ClickException as e:
            log.FAIL(f'Failed to click some button:\n{e}')
            driver.quit()
            exit()

def main():
    Id =  log.read_json('UserId')
    Pwd = log.read_json('PassWd')
    Cam = log.read_json('Campus')
    url = log.read_json('url')
    
    try:
        campus = f'/html/body/ul/li[{clicks.campus_no[Cam]}]/div'   # 校区xpath
    except KeyError:
        log.FAIL(f"Invalid campus code '{Cam}', please choose from [鼓楼: \"GL\", 浦口: \"PK\", 仙林: \"XL\", 苏州: \"SZ\"]")
        exit()

    driver = clicks.init_driver(False)  # 不使用 PotatoPlus 插件
    clicks.init_xk_page(driver, Id, Pwd, url)
    
    clicks.choose_column(driver, COLUMN, url)

    if COLUMN != 'favorite':
        # 点击切换校区
        clicks.try_to_click(driver, switch, url, script=True)   # 点击切换校区
        time.sleep(0.3)
        clicks.try_to_click(driver, campus, url)                # 选择校区
        time.sleep(0.3)
        clicks.try_to_click(driver, filter_0, url)
        time.sleep(0.6)
        clicks.try_to_click(driver, filter_1, url)
        time.sleep(1.2)

    refresh = 0
    while True:
        try:
            if refresh >= 100 and refresh % 100 == 0 and COLUMN != 'favorite':
                time.sleep(0.8)
                clicks.try_to_click(driver, filter_0, url)
                time.sleep(0.8)
                clicks.try_to_click(driver, filter_0, url)
                time.sleep(0.8)

            select = WebDriverWait(driver, timeout=TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="选择"][1]'))
            )
            select.click()
            time.sleep(0.6)

        except TimeoutException:
            refresh += 1
            log.INFO(f'Refreshed at {refresh} times...', cover=True)
            clicks.refresh_while_seeking(driver, url)
            time.sleep(0.2)
            continue

        clicks.try_to_click(driver, final_ensure, url)
        print()
        log.DONE('Got one! waiting to be processed.')
        time.sleep(2)

        refresh_once_getting(driver, url, campus)
        refresh = 1
        log.INFO(f'Refreshed at {refresh} times...', cover=True)
        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--timeout', type=float, default=1.2)
    parser.add_argument('-c', '--column', type=str, default='general')
    args = parser.parse_args()
    TIMEOUT, COLUMN = args.timeout, args.column

    # check parameters inpupt
    if COLUMN not in clicks.columns.keys() or TIMEOUT <= 0:
        log.FAIL('Invalid parameter(s) entered by user!')
        exit()
    # column 'favorite'
    if COLUMN == 'favorite':
        log.FAIL('If you want to operate in the \'favorites\' column, please try clicks-potato.py')
        exit()

    try:
        main()
    except clicks.ClickException:
        log.FAIL('Failed to find some button :(')
        exit()
    except KeyboardInterrupt:
        log.INFO('Interrupted end.')
        exit()