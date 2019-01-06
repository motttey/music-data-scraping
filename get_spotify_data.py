# -*- coding: utf-8 -*-
import urllib.request
import time
import codecs
import sys
import json
import xmltodict
import xml.etree.ElementTree as ET
import mysql.connector
from bs4 import BeautifulSoup

def scrape_charts(date):
    print("https://spotifycharts.com/regional/jp/daily/" + date)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }
    req = urllib.request.Request(url="https://spotifycharts.com/regional/jp/daily/" + date, headers=headers)
    html = urllib.request.urlopen(req)
    soup = BeautifulSoup(html, features="html.parser")
    popular_town_array = []

    chart_table_body = soup.find('table', {'class' :'chart-table'}).find('tbody')
    tr_list = chart_table_body.find_all('tr')
    for tr in tr_list:
        track = tr.find('td', {'class' :'chart-table-track'})
        streams = tr.find('td', {'class' :'chart-table-streams'})

        track_text = track.find('strong').text.replace('\u2013', '')
        artist_text = track.find('span').text.replace('\u2013', '').replace('by ', '')
        print(track_text + '-' + artist_text)

        stream_text = streams.text
        print(stream_text)

    return popular_town_array

if __name__ == '__main__':
    date = sys.argv[1]
    scrape_charts(date)
