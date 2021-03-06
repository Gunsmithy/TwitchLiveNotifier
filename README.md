# Twitch Live Notifier
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=LB2R9THJJW8EL)  
Python script to notify a Discord server when the streamer goes live, with the current game and box art.  

This was made to partially automate the process of notifying a Discord server that the broadcaster has gone live, while still adding useful information like the stream's title and game that would otherwise have to be done manually.

## How it works
Once running, the script will keep checking for your stream to go live and post in the Discord channel when it goes live with the message and description of your choosing, along with the box-art for the current game/activity.  

The program will run once and then stop, and will only allow one execution at a time in case your finger slips and you hit it twice really quick by mistake, which tends to happen a lot personally when using a Stream Deck. ;)  

Don't worry if there's a little delay before it says you're live, that's a Twitch issue.  

## Example Notification
![Example Notification](https://i.imgur.com/vQc9Ccg.png)

## Getting Started
The only thing you will need to run this is Python 3, which can be [downloaded easily here.](https://ninite.com/python3/)  

Once you've got that, head on over to the Releases tab and download the latest TwitchLiveNotifier-vX.X.X.zip file and extract it somewhere convenient on your PC.  

From there, make it your own by creating a ```config.ini``` file in the format of the existing ```config_example.ini``` file with your details. (I.e. Just rename the one there to config.ini)  See the below "Config file details" section for how to fill this all out.  

When you're all configured, run it in the foreground with ```start.bat``` or in the background with ```TwitchLiveNotifierHidden.exe``` thanks to the included [AutoHotkey](https://autohotkey.com/) script that comes pre-compiled in all releases. You can recompile it yourself if you have AutoHotkey using the included TwitchLiveNotifierHidden.ahk if you run into any issues with the exe.  

## Updating
All that is required to update to a newer version is copying your config.ini file from your previous installation into your newly downloaded one and adding any additional values that may be missing based on the new config_example.ini file.

## Config file details
The included config_example.ini should give you a good idea of what the config.ini file should look like, but I'll explain where to get all these values in detail.  

### Twitch
#### User
This is simply the username/handle of the streamer/broadcaster.  
It can be written in whatever case you would like it to appear in the below Discord message/description placeholders, as it will be converted to lowercase automatically for internal functionality.
#### ImagePriority
This is what image should be attempted to be used first for the message, Game or Preview.  
If the game logo or stream preview cannot be loaded, it will fall back to the user logo.
#### ClientId
This is the Client ID you can get from the [Twitch Developers console.](https://dev.twitch.tv/login)
#### ClientSecret
This is the Client Secret you can get from the [Twitch Developers console.](https://dev.twitch.tv/login)

If you do not have the above ID and Secret, go to the [Twitch Developers console](https://dev.twitch.tv/login), log in, and register an application.  
You can provide anything for the name and redirect URL, select any category, and upon creation you will get the ID and secret.
![Example Registration](https://i.imgur.com/ZKqJID9.png)

### Discord
#### Url
This is the URL for the Webhook you are going to set up in the Discord channel in which you wish to broadcast the notification. In your Discord server, select the settings cog wheel next to the text channel of your choosing, go to Webhooks, and create a new Webhook. The customization here is how you would like the bot to appear when posting the notification. Once complete, copy the Webhook URL provided here into your config.ini
#### Message
This is the message body for the notification being posted by the bot. It can contain anything you would normally type in discord, such as emotes and ```@``` tags. You can also type ```{{Name}}``` or ```{{Game}}``` anywhere in the message and it will be replaced dynamically with the above User setting and the name of the game being streamed respectively.
#### Description
This is the text that appears below the link/stream title in the preview box for the Discord notification. This works in a similar fashion as above with respect to Name and Game placeholders, but only accepts simple text, no tags or emotes.

## Debugging
If the program closes immediately for some unknown reason, running it directly from the command line may reveal the issue. To do so, hold Shift and right click anywhere in the folder you downloaded the script. Select "Open PowerShell/Command Prompt window here" and then type in ```python twitchlivenotifier\__init__.py``` and press Enter.  

This should run the script again but show you any error messages that may have occurred. If it still doesn't show up, you may have installed Python without adding it to your PATH. You can simply reinstall it, just make sure you check that box next time!  

## Enjoy!
Feel free to create an issue if you have any problems using this or a feature request if there's something you'd like added! 

If you found this useful, please consider donating to keep the development alive! :)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=LB2R9THJJW8EL)
