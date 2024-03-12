#!/usr/bin/python
import requests, os, re, demjson3
from bs4 import BeautifulSoup

def parse_script(url):    
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36' }
    #первый запрос (поиск плеера на странице и наименования)
    page_video = requests.get(url, headers=headers)
    content = BeautifulSoup(page_video.content, 'html.parser')

    iframe = content.find('iframe')
    video_link = 'https:' + iframe['src']

    video_info = content.find('ul', class_='flist')
    name = video_info.find('span', itemprop="name").text

    #второй запрос (поиск скрипта с описанием видео)
    vedeo = requests.get(video_link)
    html_code = BeautifulSoup(vedeo.content, 'html.parser')
    js_script = html_code.find('script', {'data-name': 'mk'})

    #обработка скрипта
    script_content = js_script.string
    match = re.search(r'makePlayer\((.*?)\);', script_content, re.DOTALL)
    json_data = match.group(1)

    jeson_data_decode = demjson3.decode(json_data, return_errors=True)[0]

    if 'title' in jeson_data_decode: vedeo_type = 'movie'
    else: vedeo_type = 'serial'

    return {'name': name, 'type': vedeo_type, 'collection': jeson_data_decode}


def count(collection):
    serial_dict = collection['playlist']['seasons']    
    count_dict = dict()    
    for season in serial_dict:
        count = len(season['episodes'])
        key = season['season']
        count_dict[f'Сезон {key}'] = count
    return count_dict
        

def transformation_link(string:str):
    string_1 = string.replace(':', '%3A')
    string_2 = string_1.replace('/', '%2F')
    final_link = 'https://fazhzcezbdi.showvid.ws/x-px/video-download?m=' + string_2
    return final_link


def get_serials(collection):
    #collection = parse_script(url)
    seasons_dict = dict()
    for season in collection['playlist']['seasons']:
        season_number = str(season['season'])        
        episodes_dict = dict()
        for episode in season['episodes']:
            episode_number = episode['episode']
            episode_link = episode['hls']
            link = transformation_link(episode_link)
            episodes_dict[f'Серия {episode_number}'] = link
            #episodes_mass.append({f'Серия {episode_number}': link})
        seasons_dict[f'Сезон {season_number}'] = episodes_dict
    return seasons_dict


def main(url):
    data = parse_script(url)
    name = data['name']
    d_type = data['type']
    collection = data['collection']

    if d_type == 'movie':
        link = get_film(collection)
        data['collection'] = link
    elif d_type == 'serial':
        link_dict = get_serials(collection)
        data['collection'] = link_dict

    return data


    # try:
    #     for season in collection['playlist']['seasons']:
    #         if season['season'] == season_number:
    #             season_dict = season
    #     for episode in season_dict['episodes']:
    #         if episode['episode'] == str(episode_number):
    #             episode_dict = episode

    #     link = transformation_link(episode_dict['hls'])    
    #     return link
    # except: return None
    

def get_film(collection):
    #collection = parse_script(url)
    link = transformation_link(collection['source']['hls'])
    return link


if __name__ == '__main__':
    url = 'https://z.mvgfilm.ru/serialy/19926-nastoyaschiy-detektiv-2014.html'
    d = parse_script(url)
    c = count(d['collection'])
    links = get_serials(d['collection'])
    for key, value in links.items():
        print (key)
        for i, j in value.items():
            print(i, j)
        
