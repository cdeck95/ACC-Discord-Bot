import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import requests
from flask import Flask

app = Flask(__name__)

@app.route('/healthz', methods=['GET'])
def index():
    print('health page reached')
    return '200 OK'

if __name__ == '__main__':
    print('Starting Flask app...')
    app.run()

# Credentials
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Create bot
intents = discord.Intents.all();
client = commands.Bot(command_prefix='!', intents=intents)

# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# Command
@client.command(name='subjectinfo', help='Retreives the image for the specified token.')
async def getimage(ctx, tokenID):
    #if int(tokenID) > 2000:
    #    await ctx.send("Please ensure the tokenID you are entering is correct and try again.")
    #else:
    gifpath = 'https://apecountryclub.s3.amazonaws.com/IMAGE/' + tokenID + '.gif'
    path = 'https://apecountryclub.s3.amazonaws.com/IMAGE/' + tokenID + '.png'
    r = requests.head(path)
    if r.status_code == requests.codes.ok:
        await ctx.send('Subject #' + tokenID + ' has undergone trials and came out successfully with limited to no side effects.')
        await ctx.send(path)
    else:
        r = requests.head(gifpath)
        print(gifpath)
        if r.status_code == requests.codes.ok:
            await ctx.send('Subject #' + tokenID + ' has undergone trials and came out successfully with limited to no side effects.')
            await ctx.send(gifpath)
        else:
            await ctx.send("Please ensure the tokenID you are entering is correct and try again.")
    
# Run the bot
client.run(TOKEN)