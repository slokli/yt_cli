from requests import get
from bs4 import BeautifulSoup
from json import load, dumps
from os import path

   
def get_channels():
    channels = []
    try:
        with open(path.abspath('channels.json')) as list:
            for id in load(list):
                channels.append(f'https://yewtu.be/channel/{id}')
    except Exception as err:
        print(f'Oops, something went wrong..\n{err}')
    return channels

def get_channel_content(url):
    channel_content = {}
    channel_html = get(url)
    channel_html.encoding = channel_html.apparent_encoding
    print(channel_html.text)

def main():
    channels = get_channels()
    print(channels)
    get_channel_content(channels[0])
    

if __name__ == '__main__':
    main()

