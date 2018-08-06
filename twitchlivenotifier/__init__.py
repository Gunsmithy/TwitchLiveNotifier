# -*- coding: utf-8 -*-

"""
Twitch Live Notifier
~~~~~~~~~~~~~~~~~~~

Python script to notify a Discord server when the streamer goes live, with the current game and box art.

:copyright: (c) 2017-2018 Dylan Kauling
:license: GPLv3, see LICENSE for more details.

"""

__title__ = 'twitchlivenotifier'
__author__ = 'Dylan Kauling'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2017-2018 Dylan Kauling'
__version__ = '0.1'

import json
import time
import sys
import urllib.parse
import configparser

import requests
import zc.lockfile

twitch_client_id = 'r5og8xrcb7c4r0b53tyijq2gvxgryp'
twitch_user = None
stream_api_url = None
stream_url = None
discord_url = None
discord_message = None
lock = None


def config():
    config_file = configparser.ConfigParser()
    config_file.read('config.ini')

    twitch_config = {}
    try:
        twitch_config = config_file['Twitch']
    except:
        print('[Twitch] section not found in config file. Please set values for [Twitch] in config.ini')
        print('Take a look at config_example.ini for how config.ini should look.')
        sys.exit()

    global twitch_user
    try:
        twitch_user = twitch_config['User']
    except:
        print('User not found in Twitch section of config file. Please set User under [Twitch] in config.ini')
        print('This is the broadcaster\'s Twitch name, case-insensitive.')
        sys.exit()

    global stream_api_url
    stream_api_url = "https://api.twitch.tv/kraken/streams/" + twitch_user.lower()

    global stream_url
    stream_url = "https://www.twitch.tv/" + twitch_user.lower()

    discord_config = {}
    try:
        discord_config = config_file['Discord']
    except:
        print('[Discord] section not found in config file. Please set values for [Discord] in config.ini')
        print('Take a look at config_example.ini for how config.ini should look.')
        sys.exit()

    global discord_url
    try:
        discord_url = discord_config['Url']
    except:
        print('Url not found in Discord section of config file. Please set Url under [Discord] in config.ini')
        print('This can be found by editing a Discord channel, selecting Webhooks, and creating a hook.')
        sys.exit()

    global discord_message
    try:
        discord_message = discord_config['Message']
    except:
        print('Message not found in Discord section of config file. Please set Message under [Discord] in config.ini')
        print('This can be set to whatever you want the bot to say, with {{Name}} and {{Game}} as placeholders.')
        sys.exit()

    global discord_description
    try:
        discord_description = discord_config['Description']
    except:
        print('Description not found in Discord section of config file. Please set Description under [Discord]' +
              ' in config.ini')
        print('This can be set to whatever you want to appear under the stream title, with {{Name}} and {{Game}}' +
              ' as placeholders.')
        sys.exit()


def lock():
    try:
        print("Acquiring lock...")
        global lock
        lock = zc.lockfile.LockFile('lock.lock')
    except:
        print("Failed to acquire lock, terminating...")
        sys.exit()


def main():
    twitch_json = {}
    while twitch_json.get('stream', None) is None:
        twitch_headers = {'Client-ID': twitch_client_id}
        twitch_request = requests.get(stream_api_url, headers=twitch_headers)
        twitch_json = twitch_request.json()

        if twitch_json['stream'] is not None:
            print("Stream is live.")

            stream_title = twitch_json['stream']['channel']['status']
            stream_game = twitch_json['stream']['channel']['game']
            stream_logo = twitch_json['stream']['channel']['logo']

            game_search_url = "https://api.twitch.tv/kraken/search/games?query=" + urllib.parse.quote_plus(stream_game)
            game_headers = {'Client-ID': twitch_client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            game_logo_request = requests.get(game_search_url, headers=game_headers)
            search_response = game_logo_request.json()
            if search_response.get('games'):
                if len(search_response.get('games')) > 0:
                    game_logo = search_response.get('games')[0]['box']['large']
                    logo_request = requests.get(game_logo)
                    if '404' not in logo_request.url:
                        stream_logo = game_logo

            # Scrub ./ from the boxart URL if present so it works with the Discord API properly
            stream_logo = stream_logo.replace('./', '')

            global discord_description
            discord_description = discord_description.replace('{{Name}}', twitch_user)
            discord_description = discord_description.replace('{{Game}}', stream_game)
            global discord_message
            discord_message = discord_message.replace('{{Name}}', twitch_user)
            discord_message = discord_message.replace('{{Game}}', stream_game)

            discord_payload = {
                "content": discord_message,
                "embeds": [
                    {
                        "title": stream_title,
                        "url": stream_url,
                        "description": discord_description,
                        "thumbnail": {
                            "url": stream_logo
                        }
                     }
                ]
            }

            status_code = 0
            while status_code != 204:
                discord_request = requests.post(discord_url, json=discord_payload)
                status_code = discord_request.status_code

                if discord_request.status_code == 204:
                    print("Successfully called Discord API. Waiting 5 seconds to terminate...")
                    time.sleep(5)
                else:
                    print("Failed to call Discord API. Waiting 5 seconds to retry...")
                    time.sleep(5)
        else:
            print("Stream is not live. Waiting 5 seconds to retry...")
            time.sleep(5)


if __name__ == "__main__":
    config()
    lock()
    main()
