#!/usr/bin/env python3
"""
HTML-based single-song Audio Network downloader.
"""
from urllib.request import build_opener, urlretrieve
import bs4
from lib import setdefaultencoding

setdefaultencoding()

opener = build_opener()
opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) '
                                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/61.0.3163.100 Safari/537.36')]


def children(tag):
    return [child for child in tag.children if type(child) == bs4.element.Tag]


def grab_data(url):
    page = opener.open(url).read()
    soup = bs4.BeautifulSoup(page, 'html.parser')
    results = soup.find_all('span', class_='result-title')
    if not results:
        print('failed because of A/B testing')
        print('retrying...')
        return grab_data(url)
    else:
        data = [children(result) for result in soup.find_all('span', class_='result-title')]
        return (
            [result[1].string.strip().encode('ascii')[1:-1].split('/') for result in data],
            [children(result[0])[0].string for result in data],
            soup.title.string
        )


def an_dl(url):
    print('grabbing song info...')
    nums, _, title = grab_data(url)
    song = title.split(' - ')[0]
    words = song.split(' ')
    last = words[-1]
    spec = last[0] == '(' and last[-1] == ')'
    try:
        num = int(words[-1 - spec])
    except ValueError:
        num = 1
    print('done.')
    vals = nums[num]
    mp3 = 'http://content2.audionetwork.com/Preview/tracks/mp3/v5res/ANW{}/{}.mp3'.format(vals[0], vals[1].zfill(2))
    print(mp3)
    print('downloading audio file...')
    urlretrieve(mp3, '{}.mp3'.format(song))
    print('done.')
    print("saved as '{}.mp3'".format(song))


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('url')
    args = parser.parse_args()
    an_dl(args.url)


if __name__ == '__main__':
    main()
