#!/usr/bin/env python3
import json
import os
from urllib.request import urlretrieve
from urllib.error import HTTPError
from an_dl import grab_data
from lib import timeout


def scrape_category(url, songs):
    page = 0
    succeed = True
    while succeed:
        try:
            page += 1
            nums, names, title = grab_data(
                url + '?page={}&size=3'.format(page)
            )
            for name, num in zip(names, nums):
                songs.add((name, 'http://content2.audionetwork.com/Preview/tracks/mp3/v5res/ANW{}/{}.mp3'.format(
                    num[0],
                    num[1].zfill(2)
                )))
            print('finished page {} of category'.format(page))
        except HTTPError:
            succeed = False


def set_dl_timeout(time_out=10):
    global dl

    @timeout(time_out, '{} seconds expired'.format(time_out))
    def dl(song, mp3, i, l):
        filename = 'songs/{}.mp3'.format(song)
        if os.path.isfile(filename):
            print('already downloaded {}.mp3\t({} of {})'.format(song, i, l))
            return
        print('downloading {}.mp3\t({} of {})'.format(song, i, l))
        urlretrieve(mp3, filename)


set_dl_timeout()


def an_scraper(redownload=False, time_out=None):

    if time_out is not None:
        if time_out < 0:
            raise ValueError
        set_dl_timeout(time_out)

    categories = set()
    total_categories = []
    songs = set()
    with open('data/categories.txt', 'r') as f:
        for line in f:
            if line:
                categories.add(line.strip())
    if os.path.isfile('data/songs.json'):
        try:
            with open('data/songs.json') as f:
                parsed = json.load(f)
        except ValueError:
            print('songs.json is invalid')
        else:
            some = False
            for category in parsed['categories']:
                if category in categories:
                    categories.remove(category)
                    some = True
                    if some and not redownload:
                        print("loading category '{}' from songs.json".format(category))
                        total_categories.append(category)
            if some and not redownload:
                for song in parsed['songs']:
                    songs.add(tuple(song))
            del parsed
    for category in categories:
        print('\nfinding songs in category: {}\n'.format(category))
        total_categories.append(category)
        scrape_category(category, songs)
    print('\nwriting songs to json...\n')
    with open('data/songs.json', 'w+') as f:
        json.dump({
            'categories': total_categories,
            'songs': list(songs)
        }, f, indent=4)
    length = len(songs)
    i = 0
    if not os.path.isdir('songs'):
        os.makedirs('songs')
    print('downloading songs\n')
    with open('data/skipped.log', 'w+'):
        pass
    for song, mp3 in songs:
        i += 1
        try:
            dl(song, mp3, i, length)
        except Exception as e:
            print('{}: {}'.format(type(e).__name__, e))
            print('skipping song, logging data')
            with open('data/skipped.log', 'a') as f:
                f.write('{},{},{},{}\n'.format(repr(song), repr(mp3),
                                               type(e).__name__, e))


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-r', '--redownload', default=False, type=bool,
                        help='see README.md for information')
    parser.add_argument('-t', '--timeout', type=int,
                        help='timeout (integer) (in seconds)')
    args = parser.parse_args()
    an_scraper(args.redownload, args.timeout)


if __name__ == '__main__':
    main()
