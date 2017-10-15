# an-dl
audio network scraper

## anw_dl.py

anw_dl.py is a scraper for one song at a time

usage: anw_dl.py [url to song]

can also download secondary songs (e.g. https://www.audionetwork.com/browse/m/track/conversation-2_49932)

## an_dl.py

an_dl.py also downloads one song, same functionality and usage as anw-dl, but it is generally slower because it only works on one audionetwork page layout, and their A/B testing makes it fail often

an_scraper depends on this, which is why it exists

## an_scraper.py

an_scraper.py is a scraper for several categories at a time

usage: an_scraper.py (-r [0 or 1])

to download categories, you must copy the url of the category into data/categories.txt, one category per line

example categories.txt:

https://www.audionetwork.com/browse/m/musical-styles/latin/bossa-nova/results
https://www.audionetwork.com/browse/m/musical-styles/musical-styles/chill-out/results
https://www.audionetwork.com/browse/m/musical-styles/musical-styles/electronica/results
https://www.audionetwork.com/browse/m/musical-styles/musical-styles/trip-hop-downbeat/results

the -r argument takes 0 or 1 as an argument (just converts input with bool() in python, will not throw exception if it's not 0 or 1)

since songs.json only stores all the songs from the last run, but doesnt match up songs with categories, if you want to download a category that is in songs.json but don't want to download all the categories, this causes an issue since you can either use all the json data or none.

if -r is 0, it will try to download all the songs in songs.json, including some that may not be in the categories you have selected. keep in mind that if the files are already in the songs directory, this will be the faster option.

if -r is 1, it will not use songs.json, but rather scrape audio network again for the song URLs, which is the faster option if the audio files from the last run are not in the songs directory.

songs that are in multiple categories will not be downloaded twice

it saves songs as mp3 files in the songs directory

it saves song URLs and the categories they came from in data/songs.json, formatted as such:

{
    "categories": [
        "https://www.audionetwork.com/browse/m/musical-styles/latin/bossa-nova/results",
        "https://www.audionetwork.com/browse/m/musical-styles/musical-styles/electronica/results",
        "https://www.audionetwork.com/browse/m/musical-styles/musical-styles/chill-out/results",
        "https://www.audionetwork.com/browse/m/musical-styles/musical-styles/trip-hop-downbeat/results",
    ],
    "songs": [
        [
            "Coral", 
            "http://content2.audionetwork.com/Preview/tracks/mp3/v5res/ANW1024/06.mp3"
        ], 
        [
            "Glider", 
            "http://content2.audionetwork.com/Preview/tracks/mp3/v5res/ANW1094/06.mp3"
        ],
        ...
        [
            "Cosmic Hustle", 
            "http://content2.audionetwork.com/Preview/tracks/mp3/v5res/ANW2078/01.mp3"
        ], 
        [
            "Storm Warning", 
            "http://content2.audionetwork.com/Preview/tracks/mp3/v5res/ANW1665/01.mp3"
        ]
    ]
}

it will check if the song is already in the songs folder, and if it is it will not download it again

if there is an error in downloading the song, it will log the song title, the URL, the error, and the error message in data/skipped.log
