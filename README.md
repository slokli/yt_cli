
# YT_CLI

It's a simple CLI for watching your favourite YouTube channels unnecessarily opening web browser


## Installation and Usage

Before installing the project, fill out the subscribtion list `channels.json` with IDs of channels that you'd like to watch.
Since the script parses data from unofficial YouTube mirror https://yewtu.be, you can follow the link before and find channel's IDs there.

### Important

Since YT_CLI isn't a video player, just a CLI, you should globally install mpv player in your OS.

#### Mac OS

```
brew install mpv
```

#### Linux / Windows WSL

```
apt install mpv
```

### Project installation

```
python -m venv venv

source ./venv/bin/activate

pip install -r ./requirements.txt

python ./main.py
```


## TODO:

- [x] Add caching
- [ ] Add video thumbnail previews via ASCII art
- [ ] Rewrite data parsing using Selenium

