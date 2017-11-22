# TwitchLiveNotifier
Python script to notify a Discord server when the streamer goes live, with the current game and box art.  

This was made to partially automate the process of notifying a Discord server that the broadcaster has gone live, while still adding useful information like the stream's title and game that would otherwise have to be done manually.

## Getting Started
The only thing you will need to run this is Python 3 , which can be [found here.](https://www.python.org/downloads/)  

Once you've got that, head on over to the Releases tab and download the latest zip file and extract it somewhere convenient on your PC.  

From there, make it your own by creating a config.ini file in the format of the existing config_example.ini file with your details.  

When you're all configured, run it in the foreground with start.bat or if you have [AutoHotkey](https://autohotkey.com/) you can compile the included TwitchLiveNotifierHidden.ahk to run it in the background instead!  

Once running, the script will keep checking for your stream to go live and post in the Discord channel when it is. 

The program will run once and then stop, and will only allow one execution at a time in case your finger slips and you hit it twice really quick by mistake, which tends to happen a lot personally when using a Stream Deck. ;)

Don't worry if there's a little delay before it says you're live, that's a Twitch issue.  

## Updating
All that is required to update to a newer version is copying your config.ini file from your previous installation into your newly downloaded one and adding any additional values that may be missing based on the new config_example.ini file.

## Config file details
The included config_example.ini should give you a good idea of what the config.ini file should look like, but I'll explain where to get all these values in detail.  

### Twitch
#### User
This is simply the username/handle of the streamer/broadcaster. It can be written in whatever case you would like it to appear in the below Discord message/description placeholders, as it will be converted to lowercase automatically for internal functionality.
#### Client ID
This is a unique identifier given to you by Twitch to give the script access to their APIs to check if you're live and see what game you're playing. You can get this by going to [the Twitch API site here](https://dev.twitch.tv/dashboard/apps/create) and creating a new "App." You can name and categorize it however you like, and simply set the OAuth Redirect URI to ```http://localhost``` before pressing Register. It will then provide you with the Client ID to paste into your config.ini file.

### Discord
#### Url
This is the URL for the Webhook you set up in the Discord channel in which you wish to broadcast the notification. Select the settings cog wheel next to the text channel of your choosing, go to Webhooks, and create a new Webhook. The customization here is how you would like the bot to appear when posting the notification. Once complete, copy the Webhook URL provided here into your config.ini
#### Message
This is the message body for the notification being posted by the bot. It can contain anything you would normally type in discord, such as emotes and ```@``` tags. You can also type ```{{Name}}``` or ```{{Game}}``` anywhere in the message and it will be replaced dynamically with the above User setting and the name of the game being streamed respectively.
#### Description
This is the text that appears below the link/stream title in the preview box for the Discord notification. This works in a similar fashion as above with respect to Name and Game placeholders, but only accepts simple text, no tags or emotes.

## Example Notification
![Example Notification](https://i.imgur.com/vQc9Ccg.png)

## Enjoy!
Feel free to create an issue if you have any problems using this or a feature request if there's something you'd like added! :)