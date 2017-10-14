#!/usr/bin/env python
import sys
import urllib
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from lib import Unbuffered
sys.stdout = Unbuffered(sys.stdout)


caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get('https://www.audionetwork.com/browse/m/track/daybreak_4259')



def anw_dl(url, chromedriver_path=None):

    sys.stdout.write('setting up webdriver...')
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_args = {'desired_capabilities': caps, 'chrome_options': chrome_options}
    if chromedriver_path is not None:
        chrome_args['executable_path'] = chromedriver_path
    driver = webdriver.Chrome(**chrome_args)
    print ' done.'

    sys.stdout.write('loading web page...')
    driver.get(url)
    song = driver.title.split(' - ')[0]
    words = song.split(' ')
    last = words[-1]
    spec = last[0] == '(' and last[-1] == ')'
    try:
        num = int(words[-1 - spec])
    except ValueError:
        num = 1
    print ' done.'
    sys.stdout.write('intercepting network requests...')
    players = driver.find_elements_by_class_name("play")
    if not players:
        print
        print 'err: player not found'
        sys.exit(-1)
    actions = ActionChains(driver)
    actions.move_to_element(players[num]).perform()
    players[num - 1].click()
    print ' done.'
    players[num - 1].click()

    sys.stdout.write('extracting audio file...')
    mp3 = ''
    for entry in driver.get_log('performance'):
        if 'mp3' in entry['message']:
            mp3 = entry['message'].split('"url":"')[1].split('.mp3')[0] + '.mp3'
            print ' done.'
            print mp3
            break
    if not mp3:
        print
        print 'err: mp3 not found'
        sys.exit(-1)
    driver.quit()
    sys.stdout.write('downloading audio file...')
    urllib.urlretrieve(mp3, "{}.mp3".format(song))
    print ' done.'
    print 'saved as "{}.mp3"'.format(song)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    anw_dl(args.url)
