from facebook_scraper import get_posts
import json, datetime
import discord
from discord.ext import tasks


# SCRIPT SETTINGS
PAGE_NAME = 'FACEBOOK_PAGENAME_OR_PROFILE'
COOKIE_FILE = 'PATH_OF_FACEBOOK_COOKIE_FILE_TXT'
LOG_JSON = 'PATH_OF_THE_JSON_FILE'

# BOT SETTINGS
BOT_TOKEN = 'DISCORD_BOT_TOKEN'
BOT_NAME = 'DISCORD_BOT_NAME'
BOT_CHANNEL_ID = int('DISCORD_CHANNEL_ID')
BOT_CHECK_DELAY_SEC = 60*5

# Writing the Post ID in JSON
def json_write(new_data):
    with open("log.json",'r+') as file:
        file_data = json.load(file)
        file_data["posts"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

# Embed Template for Discord Send
def embed_temp(client, url, time, mediaprev, caption):
    embed = discord.Embed(title=url, url=url, timestamp=datetime.datetime.fromtimestamp(time))
    embed.set_author(name=BOT_NAME, icon_url=client.user.display_avatar)
    embed.description = caption[:999]+"..." if len(caption) > 999 else caption[:999]
    embed.set_image(url=mediaprev)
    embed.set_footer(icon_url= "https://cdn.discordapp.com/attachments/839327846773162014/999566573339676703/eFacebook.png", text="Facebook");
    return embed

# Getting the valid Data
def onMessage(data):
    log = open('log.json', 'r')
    logged = json.loads(log.read())
    oldlogid = logged["posts"]
    newlogid = data["post_id"]
    if newlogid not in oldlogid:
        # Getting the Facebook post ID
        post_id = data["post_id"]
        if post_id == None:
            post_id = "The Post ID is not found!"
        # Getting the Facebook post URL
        post_url = data["w3_fb_url"]
        if post_url == None:
            post_url = "https://facebook.com/" + data['post_id']
            if post_url == None:
                post_url = " "
        # Getting the Facebook Facebook post caption
        post_cap = data["text"]
        if post_cap == None:
            post_cap = " "
        # Getting the Facebook post datestamp
        post_time = (data['time']).timestamp()
        # Getting media from Facebook post
        if data['image'] != None:
            post_preview = data['image']
        elif data['video'] != None:
            post_preview = data['video_thumbnail']
        # id, url, caption, time, prev_media
        return [post_id, post_url, post_cap, post_time, post_preview]
    else:
        #print("No new updates from " + BOT_NAME)
        return [None]
        

# Starting the Discord client
client = discord.Client(intents=discord.Intents.all())
# Announment async task loop
@tasks.loop(seconds=BOT_CHECK_DELAY_SEC)
async def announcement():
    channel = client.get_channel(BOT_CHANNEL_ID)
    for post in get_posts(PAGE_NAME, pages=1, cookies=COOKIE_FILE):
        newpost = post
        break
    if (BOT_TOKEN == None) or (PAGE_NAME == None) or (COOKIE_FILE == None):
        print("Correct Environment Variables not provided!")
    else:
        retcode = onMessage(newpost)
        if retcode[0] != None:
            print("The Post with ID " + retcode[0] + " has been logged.")
            json_write(retcode[0])
            await channel.send(embed=embed_temp(url=retcode[1], client=client, caption=retcode[2], time=retcode[3], mediaprev=retcode[4]))

@client.event
async def on_ready():
    print(client.user.name+" is running ....")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="ACOMSS FB Page"))
    announcement.start()

# Running .....
client.run(BOT_TOKEN)




