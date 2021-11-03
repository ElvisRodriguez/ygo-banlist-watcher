# ygo-banlist-watcher

Tool to monitor Yu-Gi-Oh's official site and report changes to the Forbidden &amp; Limited List.

```diff
-THIS TOOL IS STILL IN DEVELOPMENT
```

## Setting this tool up on your machine:

### Requirements:
- Python 3.6 or greater.
- OS: Linux.
    - This tool is untested on Mac and Windows, it could produce unintended behavior or simply not work.

### Clone repository and set up virtual environment

```bash
$ git clone git@github.com:ElvisRodriguez/ygo-banlist-watcher.git
$ cd ygo-banlist-watcher
$ python3 -m venv .
$ source bin/activate
(ygo-banlist-watcher) $ pip3 install -r requirements.txt
(ygo-banlist-watcher) $ python3 api/watcher.py
```

### Spin up the watcher script

```bash
(ygo-banlist-watcher) $ python3 api/watcher.py
(ygo-banlist-watcher) $ Scraping Yu-Gi-Oh official F&L list page...
(ygo-banlist-watcher) $ No updates detected. Sleeping for 10 seconds...
```
