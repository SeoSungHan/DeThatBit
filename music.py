import os
import sys
import json
from bs4 import BeautifulSoup
import requests
from typing import get_args
import re
import django
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DeThatBit.settings")
django.setup()

#import albums
from albums.models import Albums
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

<<<<<<< HEAD
url_melon = 'https://www.melon.com/genre/album_listPaging.htm?startIndex=1&pageSize=100&gnrCode=GN0300'
=======
url_melon = 'https://www.melon.com/genre/album_listPaging.htm?startIndex=1&pageSize=20&gnrCode=GN0300'
>>>>>>> ae744f6d1c0b5fb147838e243dca5cfca47d5618
url_detail = 'https://www.melon.com/album/detail.htm?albumId='


def get_melon():
    result = requests.get(
        url_melon, headers=header)
    soup = BeautifulSoup(result.text, "html.parser")
    albums = soup.find("div", {"class": "service_list_album"}).find("ul").find_all(
        "li", recursive=False)
    # print(albums)
    album_list = []
    artist_list = []
    for album in albums:
        link_ = album.find("a", {"class": "album_name"})["href"]
        link_id = re.findall("\d+", link_)[0]
        link = f'{url_detail}{link_id}'

        cover = album.find("div", {"class": "thumb"}).find("img")["src"]
        artist = album.find(
            "span", {"class": "checkEllipsis"}).get_text(strip=True)
        album_name = album.find(
            "a", {"class": "album_name"}).get_text(strip=True)
        type = album.find("span", {"class": "vdo_name"}).get_text(strip=True)
        date = album.find("span", {"class": "reg_date"}).get_text(strip=True)
        # save artists in artist_list
        if artist not in artist_list:
            artist_list.append(artist)
        album_list.append(
            {'link': link, 'cover': cover, 'artist': artist, 'type': type, 'album': album_name, 'date': date})

    return album_list, artist_list


if __name__ == '__main__':
    albums, artists = get_melon()
    #print(albums)
    #print(artists)
    
    for data in albums:
        tmp = data['date'].split('.')
        date_tmp = tmp[0]+'-'+tmp[1]+'-'+tmp[2]

        exist=Albums.objects.filter(
                Q(album=data['album']) & Q(artist=data['artist'] )
            ).distinct()
        if exist:
            #print(data) 
            continue
        #print(data)
        Albums(artist=data['artist'], a_type=data['type'],
               album=data['album'], date=date_tmp, cover=data['cover'], link=data['link']).save()

