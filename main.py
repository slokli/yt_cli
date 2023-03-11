from requests import get
from bs4 import BeautifulSoup
from json import load, dumps
from os import path, system
from re import compile
import inquirer
from random import choice

def get_random_user_agent():
    agents_list = []
    with open(path.abspath('user-agents.txt')) as agents:
        for agent in agents.readlines():
            agents_list.append(agent.replace('\n', ''))
    return choice(agents_list)

def get_channels():
    channels = []
    try:
        with open(path.abspath('channels.json')) as list:
            for id in load(list):
                url = f'https://yewtu.be/channel/{id}'
                channel_html = get(url, headers={'User-Agent': get_random_user_agent()})
                channel_html.encoding = 'utf-8'
                sp = BeautifulSoup(channel_html.text, 'html.parser')
                channel_title = sp.find('div', class_='channel-profile').find('span')
                channels.append({ 'title': channel_title.get_text(), 'url': url })
    except Exception as err:
        print(f'Oops, something went wrong..\n{err}')
    return channels

def get_channel_content(url, content={'title': '', 'videos': []}):
    channel_content = content
    channel_html = get(url, headers={'User-Agent': get_random_user_agent()})
    channel_html.encoding = 'utf-8'
    sp = BeautifulSoup(channel_html.text, 'html.parser')

    channel_title = sp.find('div', class_='channel-profile').find('span')
    channel_content['title'] = channel_title.get_text()
    
    video_urls =  sp.find_all('a', href=compile('^\/watch\?v='), title=False)
    next_page_btn = sp.find('a', href=compile('^/channel/.*\?continuation=')) 

    for index, url in enumerate(video_urls):
        channel_content['videos'].append({
            'title': url.find('p', dir='auto').get_text(),
            'url': f'https://yewtu.be{url.get("href")}',
            'thumbnail': 'https://yewtu.be' + url.find('img', class_='thumbnail').get('src')
        })

    if next_page_btn:
        get_channel_content(url=f'https://yewtu.be{next_page_btn.get("href")}', content=channel_content)

    return channel_content


def main(cached_channels=[]):
    channels = cached_channels if len(cached_channels) != 0 else get_channels()
    channel_titles = []
    video_titles = []
    service_answers = {'EXIT': 'Сорян, ошибся дверью =/', 'PREV': 'Мне на этаж ниже (o_o)/'}

    for ch in channels:
        channel_titles.append(ch['title'])
    channel_titles.append(service_answers['EXIT'])

    channels_list = [inquirer.List(
        'channel',
        message='Ну что, дружок-пирожок, кого будем смотреть?',
        choices=channel_titles
    )]

    channel_choice = inquirer.prompt(channels_list)

    if channel_choice['channel'] == service_answers['EXIT']:
        exit(0)
    else:
        system('clear')
        choosen_channel_dict = [ch for ch in channels if channel_choice['channel'] == ch['title']]
        choosen_channel_content = []
        choosen_channel_content = get_channel_content(url=choosen_channel_dict[0]['url'], content={'title': '', 'videos': []}) #TODO: Cache

        for video in choosen_channel_content['videos']:
            video_titles.append(video['title'])
        video_titles.append(service_answers['PREV'])

        video_list = [inquirer.List(
            'video',
            message='Хорошо, кожевник. А видос какой?',
            choices=video_titles
        )]

        video_choice = inquirer.prompt(video_list)

        if video_choice['video'] == service_answers['PREV']:
            system('clear')
            main(cached_channels=channels)
        else:
            choosen_video_dict = [v for v in choosen_channel_content['videos'] if video_choice['video'] == v['title']]
            system('clear')
            system(f'mpv {choosen_video_dict[0]["url"]}')
    

if __name__ == '__main__':
    main()

