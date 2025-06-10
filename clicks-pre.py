"""
    Run when you first use clicks with potatos.
    Firstly check & download user's python dependencies.
    Download PotatoPlus plugin on user's chrome driver.

    Last updated: 2025.6.10
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

import time
import clicks
import myLog as log

url = 'https://chromewebstore.google.com/detail/potatoplus/mokphlegfcilcbnjmhgfikjgnbnconba?hl=zh-CN&utm_source=ext_sidebar'
addChrome = '//*[@id="yDmH0d"]/c-wiz/div/div/main/div/section[1]/section/div/div[1]/div[2]/div/button/span[6]'

try:
    driver = clicks.init_driver(potato=True)
    log.INFO('Trying to open the plugin page...')
    driver.get(url)

    time.sleep(1)
    clicks.try_to_click(driver, addChrome ,url, script=True)

    log.INFO('Please press "添加扩展程序" button to ensure :)')
    log.DONE('Use ctrl+C to finish.')
    time.sleep(3000)

except KeyboardInterrupt:
    log.DONE('Exited.')
    driver.quit()
    exit()