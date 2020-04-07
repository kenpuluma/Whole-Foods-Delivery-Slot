import bs4

from selenium import webdriver

import sys
import time
import msvcrt
import winsound


def getWFSlot(productUrl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }

    driver = webdriver.Chrome()
    driver.get(productUrl)
    no_open_slots = True
    duration = 5
    time.sleep(180)

    while True:
        if msvcrt.kbhit():
            if 'p' in msvcrt.getwche():
                sys.stdout.write('\rPaused at {}. Press c to continue.'.format(time.strftime('%H:%M:%S', time.localtime())))
                sys.stdout.flush()
                no_open_slots = False
            if 'c' in msvcrt.getwche():
                no_open_slots = True
        if no_open_slots:
            driver.refresh()
            html = driver.page_source
            soup = bs4.BeautifulSoup(html, 'html.parser')

            try:
                for day_button in soup.find_all('div', class_='ufss-date-select-toggle-text-container'):
                    for availability in day_button.find_all('div', class_='ufss-date-select-toggle-text-availability'):
                        for status in availability.stripped_strings:
                            if status != 'Not available':
                                print('SLOTS OPEN!')
                                winsound.Beep(440, 5000)
                                no_open_slots = False
                if no_open_slots:
                    sys.stdout.write('\rRefreshed at {}. Press p to pause.'.format(time.strftime('%H:%M:%S', time.localtime())))
                    sys.stdout.flush()
                    time.sleep(duration)
            except AttributeError as error:
                print('error: {0}'.format(error))
                continue
        else:
            time.sleep(duration)


getWFSlot('https://www.amazon.com/gp/buy/shipoptionselect/handlers/display.html?hasWorkingJavascript=1')
