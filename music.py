import os
import sys
import json
from bs4 import BeautifulSoup
import requests
from typing import get_args
import re
import django
from django.db.models import Q
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DeThatBit.settings")
django.setup()

#import albums
from albums.models import Albums
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
api_flo = 'https://www.music-flo.com/api/display/v1/browser/genre/newalbum/6?timestamp=1615814390181'

def get_flo():
    req = requests.get(api_flo)
    data = req.json()
    new_albums = data['data']['albumList']
    result = []

    #print(new_albums[0])

    for new_album in new_albums:
        artist_str=""

        for i in range(len(new_album['artistList'])):
            artist_str += new_album['artistList'][i]['name']

            if i == len(new_album['artistList'])-1: continue
            else: artist_str += ", "

        result.append({
            'type': new_album['type'],
            'cover': new_album['imgList'][0]['url'],
            'artist': artist_str,
            'album': new_album['title'],
            'date': new_album['releaseYmd']
        })

    return result

def main():
    albums = get_flo()
    
    for data in albums:
        tmp = data['date']
        tmp0 = tmp[0:4]
        tmp1 = tmp[4:6]
        tmp2 = tmp[6:]
        date_tmp = tmp0+'-'+tmp1+'-'+tmp2
        #print(data['artist'])
        exist=Albums.objects.filter(
                Q(album=data['album']) & Q(artist=data['artist'] )
            ).distinct()
        if exist:
            #print(exist) 
            continue
        Albums(artist=data['artist'], a_type=data['type'],
               album=data['album'], date=date_tmp, cover=data['cover']).save()


if __name__ == '__main__':

    while True:
        t=time.time()
        if int(t)%100==0:
            print("music.py Work")
            main()
            time.sleep(50)

