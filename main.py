from requests import get
from bs4 import BeautifulSoup
from json import load, dumps
from os import path
from re import compile

   
def get_channels():
    channels = []
    try:
        with open(path.abspath('channels.json')) as list:
            for id in load(list):
                url = f'https://yewtu.be/channel/{id}'
                channel_html = get(url)
                channel_html.encoding = 'utf-8'
                sp = BeautifulSoup(channel_html.text, 'html.parser')
                channel_title = sp.find('div', class_='channel-profile').find('span')
                channels.append({ 'title': channel_title.get_text(), 'url': url })
    except Exception as err:
        print(f'Oops, something went wrong..\n{err}')
    return channels

def get_channel_content(url, content={'title': '', 'videos': []}):
    channel_content = content
    channel_html = get(url)
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


def main():
    channels = get_channels()
    ch_content = get_channel_content(channels[0]['url'])
    print(ch_content)
    

if __name__ == '__main__':
    main()

