"""
    Run when you first use clicks with potatos.
"""
import time
import clicks_xk as click
import myLog as log

url = 'https://chromewebstore.google.com/search/PotatoPlus?utm_source=ext_app_menu'
rectangle = '//*[@id="yDmH0d"]/c-wiz/div/div/div/main/section/div[1]/div/a'
addChrome = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/main/div/section[1]/section/div[2]/div/button/span[6]'

try:
    driver = click.init_driver(potato=True)
    driver.get(url)
    time.sleep(1.2)
    log.INFO('Clicking the "PotatoPlus"...')
    click.try_to_click(driver, rectangle, url)
    time.sleep(1.2)
    log.INFO('Clicking to add to your Chrome...')
    click.try_to_click(driver, addChrome, url)
    log.DONE('Please click to confirm the addition.')
    time.sleep(3000)

except KeyboardInterrupt:
    log.DONE('Exited.')
    exit()