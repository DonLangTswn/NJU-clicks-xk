"""
    Run when you first use clicks with potatos.
    Firstly check your python dependencies.

    Last updated: 2025.6.9
"""
import sys
import subprocess

# check dependencies
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])

ensure_package('selenium')
ensure_package('colorama')
ensure_package('filelock')
ensure_package('webdriver_manager')

import time
import clicks
import myLog as log

url = 'https://chromewebstore.google.com/search/PotatoPlus?utm_source=ext_app_menu'
rectangle = '//*[@id="yDmH0d"]/c-wiz/div/div/div/main/section/div[1]/div/a'
addChrome = '//*[@id="yDmH0d"]/c-wiz/div/div/main/div/section[1]/section/div/div[1]/div[2]/div/button/span[6]'

try:
    driver = clicks.init_driver(potato=True)
    driver.get(url)
    time.sleep(1.2)
    log.INFO('Clicking the "PotatoPlus"...')
    clicks.try_to_click(driver, rectangle, url)
    time.sleep(1.2)
    log.INFO('Clicking to add to your Chrome...')
    clicks.try_to_click(driver, addChrome, url)
    log.DONE('Please click to confirm the addition...')
    time.sleep(3)
    log.DONE('Use ctrl+C to finish.')
    time.sleep(3000)

except clicks.ClickException:
    log.FAIL('Failed to click to download PotatoPlus, check your connection first.')
    driver.quit()
    exit()

except KeyboardInterrupt:
    log.DONE('Exited.')
    driver.quit()
    exit()