# -*- coding: utf-8 -*-
import requests
import time
import codecs
import sys
import json
import xmltodict
import xml.etree.ElementTree as ET
import mysql.connector
import datetime

import matplotlib.pyplot  as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pandas as pd

from bs4 import BeautifulSoup

collected_data_object = {}

def scrape_charts(date):
    print("https://spotifycharts.com/regional/jp/daily/" + date)
    headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
        }
    req = requests.get(url="https://spotifycharts.com/regional/jp/daily/" + date, headers=headers)
    # html = urllib.request.urlopen(req)
    soup = BeautifulSoup(req.content, features="html.parser")
    popular_town_array = []

    chart_table_body = soup.find('table', {'class' :'chart-table'}).find('tbody')
    tr_list = chart_table_body.find_all('tr')

    rank = 1
    for tr in tr_list:
        track = tr.find('td', {'class' :'chart-table-track'})
        streams = tr.find('td', {'class' :'chart-table-streams'})

        track_text = track.find('strong').text.replace('\u2013', '')
        artist_text = track.find('span').text.replace('\u2013', '').replace('by ', '')
        # print(track_text + '-' + artist_text)

        track_object = {}

        track_object["title"] = track_text
        track_object["rank"] = rank
        track_object["date"] = date

        if artist_text not in collected_data_object:
            collected_data_object[artist_text] = {}

        if track_text not in collected_data_object[artist_text]:
            collected_data_object[artist_text][track_text] = []

        collected_data_object[artist_text][track_text].append(track_object)

        stream_text = streams.text
        print(stream_text)
        rank = rank + 1
    return

if __name__ == '__main__':
    # date = sys.argv[1]
    date_string_list = []

    base = datetime.datetime(2018, 12, 31)
    numdays = 100
    date_string_list = [(base - datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, numdays)]
    date_string_list.reverse()

    for date in date_string_list:
        scrape_charts(date)

    selected_artists = {}
    for artist in collected_data_object:
        if len(collected_data_object[artist].items()) > 8:
            selected_artists[artist] = collected_data_object[artist]

    print(selected_artists)
    fp = FontProperties(fname=r'C:\Windows\Fonts\yuminl.ttf', size=10)

    for selected_artist in selected_artists:
        for track in selected_artists[selected_artist]:
            df = pd.DataFrame.from_dict(selected_artists[selected_artist][track])
            plt.plot(pd.to_datetime(df["date"]), df["rank"], label=track)

        plt.title(selected_artist, fontproperties=fp)
        plt.ylim(200, 0)
        plt.legend(prop=fp, bbox_to_anchor=(1, 0), loc='lower right')

        # plt.show()
        plt.savefig(selected_artist + '.png')
