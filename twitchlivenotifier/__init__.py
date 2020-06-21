# -*- coding: utf-8 -*-

"""
Twitch Live Notifier
~~~~~~~~~~~~~~~~~~~

Python script to notify a Discord server when the streamer goes live, with the current game and box art.

:copyright: (c) 2017-2020 Dylan Kauling
:license: GPLv3, see LICENSE for more details.

"""

__title__ = 'twitchlivenotifier'
__author__ = 'Dylan Kauling'
__license__ = 'GPLv3'
__copyright__ = 'Copyright 2017-2020 Dylan Kauling'
__version__ = '0.3'

import time
import sys
import configparser

import requests
import zc.lockfile

twitch_client_id = ''
twitch_secret_key = ''
twitch_app_token_json = {}
twitch_user = ''
image_priority = ''
stream_api_url = ''
stream_url = ''
discord_url = ''
discord_message = ''
discord_description = ''
lock = None


def config():
    config_file = configparser.ConfigParser()
    config_file.read('config.ini')

    try:
        twitch_config = config_file['Twitch']
    except KeyError:
        print('[Twitch] section not found in config file. Please set values for [Twitch] in config.ini')
        print('Take a look at config_example.ini for how config.ini should look.')
        sys.exit()

    global twitch_user
    try:
        twitch_user = twitch_config['User']
    except KeyError:
        print('User not found in Twitch section of config file. Please set User under [Twitch] in config.ini')
        print('This is the broadcaster\'s Twitch name, case-insensitive.')
        sys.exit()

    global image_priority
    try:
        image_priority = twitch_config['ImagePriority']
    except KeyError:
        print('ImagePriority not found in Twitch section of config file. '
              'Please set ImagePriority under [Twitch] in config.ini')
        print('This is what image should be attempted to be used first for the message, Game or Preview.')
        print('If the game logo or stream preview cannot be loaded, it will fall back to the user logo.')
        sys.exit()

    global twitch_client_id
    try:
        twitch_client_id = twitch_config['ClientId']
    except KeyError:
        print('ClientId not found in Twitch section of config file. Please set ClientId under [Twitch] in config.ini')
        print('This is the Client ID you receive when registering an application as a Twitch developer.')
        print('Please check the README for more instructions.')
        sys.exit()

    global twitch_secret_key
    try:
        twitch_secret_key = twitch_config['ClientSecret']
    except KeyError:
        print('ClientSecret not found in Twitch section of config file. Please set ClientSecret under [Twitch] in '
              'config.ini')
        print('This is the Client Secret you receive when registering an application as a Twitch developer.')
        print('Please check the README for more instructions.')
        sys.exit()

    global stream_api_url
    stream_api_url = "https://api.twitch.tv/helix/streams"

    global stream_url
    stream_url = "https://www.twitch.tv/" + twitch_user.lower()

    try:
        discord_config = config_file['Discord']
    except KeyError:
        print('[Discord] section not found in config file. Please set values for [Discord] in config.ini')
        print('Take a look at config_example.ini for how config.ini should look.')
        sys.exit()

    global discord_url
    try:
        discord_url = discord_config['Url']
    except KeyError:
        print('Url not found in Discord section of config file. Please set Url under [Discord] in config.ini')
        print('This can be found by editing a Discord channel, selecting Webhooks, and creating a hook.')
        sys.exit()

    global discord_message
    try:
        discord_message = discord_config['Message']
    except KeyError:
        print('Message not found in Discord section of config file. Please set Message under [Discord] in config.ini')
        print('This can be set to whatever you want the bot to say, with {{Name}} and {{Game}} as placeholders.')
        sys.exit()

    global discord_description
    try:
        discord_description = discord_config['Description']
    except KeyError:
        print('Description not found in Discord section of config file. Please set Description under [Discord]' +
              ' in config.ini')
        print('This can be set to whatever you want to appear under the stream title, with {{Name}} and {{Game}}' +
              ' as placeholders.')
        sys.exit()


def get_lock():
    try:
        print("Acquiring lock...")
        global lock
        lock = zc.lockfile.LockFile('lock.lock')
    except:
        print("Failed to acquire lock, terminating...")
        sys.exit()


def authorize():
    token_params = {
        'client_id': twitch_client_id,
        'client_secret': twitch_secret_key,
        'grant_type': 'client_credentials',
    }
    app_token_request = requests.post('https://id.twitch.tv/oauth2/token', params=token_params)
    global twitch_app_token_json
    twitch_app_token_json = app_token_request.json()


def main():
    twitch_json = {'data': []}
    while len(twitch_json['data']) == 0:
        twitch_headers = {
            'Client-ID': twitch_client_id,
            'Authorization': 'Bearer ' + twitch_app_token_json['access_token'],
        }
        twitch_params = {'user_login': twitch_user.lower()}
        request_status = 401
        while request_status == 401:
            twitch_request = requests.get(stream_api_url, headers=twitch_headers, params=twitch_params)
            request_status = twitch_request.status_code
            if request_status == 401:
                authorize()
                twitch_headers['Authorization'] = 'Bearer ' + twitch_app_token_json['access_token']
                continue
            twitch_json = twitch_request.json()

        if len(twitch_json['data']) == 1:
            print("Stream is live.")

            stream_json = twitch_json['data'][0]
            stream_title = stream_json['title']
            stream_game_id = stream_json['game_id']
            stream_preview_temp = stream_json['thumbnail_url']
            stream_preview_temp = stream_preview_temp.replace('{width}', '1280')
            stream_preview_temp = stream_preview_temp.replace('{height}', '720')
            preview_request = requests.get(stream_preview_temp)
            if '404' not in preview_request.url:
                stream_preview = stream_preview_temp
            else:
                stream_preview = None

            game_search_url = "https://api.twitch.tv/helix/games"
            game_params = {'id': stream_game_id}
            search_response = {}
            request_status = 401
            while request_status == 401:
                game_request = requests.get(game_search_url, headers=twitch_headers, params=game_params)
                request_status = game_request.status_code
                if request_status == 401:
                    authorize()
                    twitch_headers['Authorization'] = 'Bearer ' + twitch_app_token_json['access_token']
                    continue
                search_response = game_request.json()

            stream_game = "something"
            game_logo = None
            if len(search_response['data']) > 0:
                game_data = search_response['data'][0]
                stream_game = game_data['name']
                game_logo_temp = game_data['box_art_url']
                game_logo_temp = game_logo_temp.replace('{width}', '340')
                game_logo_temp = game_logo_temp.replace('{height}', '452')
                logo_request = requests.get(game_logo_temp)
                if '404' not in logo_request.url:
                    # Scrub ./ from the boxart URL if present so it works with the Discord API properly
                    game_logo = game_logo_temp.replace('./', '')

            user_search_url = "https://api.twitch.tv/helix/users"
            user_params = {'login': twitch_user.lower()}
            user_response = {}
            request_status = 401
            while request_status == 401:
                user_request = requests.get(user_search_url, headers=twitch_headers, params=user_params)
                request_status = user_request.status_code
                if request_status == 401:
                    authorize()
                    twitch_headers['Authorization'] = 'Bearer ' + twitch_app_token_json['access_token']
                    continue
                user_response = user_request.json()

            user_logo = None
            print(str(user_response))
            if len(user_response['data']) == 1:
                user_data = user_response['data'][0]
                user_logo_temp = user_data['profile_image_url']
                logo_request = requests.get(user_logo_temp)
                if '404' not in logo_request.url:
                    # Scrub ./ from the boxart URL if present so it works with the Discord API properly
                    user_logo = user_logo_temp.replace('./', '')

            global discord_description
            discord_description = discord_description.replace('{{Name}}', twitch_user)
            discord_description = discord_description.replace('{{Game}}', stream_game)
            global discord_message
            discord_message = discord_message.replace('{{Name}}', twitch_user)
            discord_message = discord_message.replace('{{Game}}', stream_game)

            if image_priority == "Game":
                if game_logo:
                    stream_logo = game_logo
                else:
                    if stream_preview:
                        stream_logo = stream_preview
                    else:
                        stream_logo = user_logo
            else:
                if stream_preview:
                    stream_logo = stream_preview
                else:
                    if game_logo:
                        stream_logo = game_logo
                    else:
                        stream_logo = user_logo

            discord_payload = {
                "content": discord_message,
                "embeds": [
                    {
                        "title": stream_title,
                        "url": stream_url,
                        "description": discord_description,
                        "image": {
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
    get_lock()
    authorize()
    main()
