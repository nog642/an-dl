#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Selenium-based single-song Audio Network downloader.
"""
from __future__ import print_function
import os
from urllib import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lib import setdefaultencoding, unbuffer

setdefaultencoding()
unbuffer()


def anw_dl(url, chromedriver_path=None):
    """
    Downloads audio network song at url.

    Warning: Does not verify chromedriver path is a valid path.
    :param url: URL of song to download.
    :param chromedriver_path: Path to chromedriver executable.
    :return: exit code
    """

    print('setting up webdriver...', end='')
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_args = {'desired_capabilities': caps, 'chrome_options': chrome_options}
    if chromedriver_path is not None:
        chrome_args['executable_path'] = chromedriver_path
    driver = webdriver.Chrome(**chrome_args)
    print(' done.')

    print('loading web page...', end='')
    driver.get(url)
    song = driver.title.split(' - ')[0]
    words = song.split(' ')
    last = words[-1]
    spec = last[0] == '(' and last[-1] == ')'
    try:
        num = int(words[-1 - spec])
    except ValueError:
        num = 1
    print(' done.')
    print('intercepting network requests...', end='')
    players = driver.find_elements_by_class_name("play")
    if not players:
        print()
        print('err: player not found')
        return 1
    actions = ActionChains(driver)
    actions.move_to_element(players[num]).perform()
    players[num - 1].click()
    print(' done.')
    players[num - 1].click()

    print('extracting audio file...', end='')
    mp3 = ''
    for entry in driver.get_log('performance'):
        if 'mp3' in entry['message']:
            mp3 = entry['message'].split('"url":"')[1].split('.mp3')[0] + '.mp3'
            print(' done.')
            print(mp3)
            break
    if not mp3:
        print()
        print('err: mp3 not found')
        return 1
    driver.quit()
    print('downloading audio file...', end='')
    urlretrieve(mp3, "{}.mp3".format(song))
    print(' done.')
    print('saved as "{}.mp3"'.format(song))

    return 0


def main():
    from argparse import ArgumentParser
    from sys import exit
    parser = ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-p', '--chromedriver-path')
    args = parser.parse_args()

    if not os.path.isfile(args.chromedriver_path):
        raise ValueError("--chromedriver-path '{}' is not a file".format(
            args.chromedriver_path
        ))

    exit(anw_dl(
        url=args.url,
        chromedriver_path=args.chromedriver_path
    ))


if __name__ == '__main__':
    main()
