import re
from typing import get_args
import requests
from bs4 import BeautifulSoup
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DeThatBit.settings")
import django
django.setup()
from albums.models import Albums

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

url_melon = 'https://www.melon.com/genre/album_listPaging.htm?startIndex=1&pageSize=10000&gnrCode=GN0300'
url_detail = 'https://www.melon.com/album/detail.htm?albumId='

def get_melon():
    result = requests.get(
        url_melon, headers=header)
    soup = BeautifulSoup(result.text, "html.parser")
    albums = soup.find("div", {"class": "service_list_album"}).find("ul").find_all(
        "li", recursive=False)
    # print(albums)
    album_list = []
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
        album_list.append(
            {'link':link, 'cover': cover, 'artist': artist, 'type': type, 'album': album_name, 'date': date})

    return album_list

if __name__=='__main__':
    albums=get_melon()
    for data in albums:
        tmp=data['date'].split('.')
        date_tmp=tmp[0]+'-'+tmp[1]+'-'+tmp[2]
        Albums(artist=data['artist'], a_type=data['type'], 
            album=data['album'], date=date_tmp, cover=data['cover'], link=data['link']).save()