from discord.ext import commands, tasks # for bot commands and tasks
import discord # for discord API
import datetime # for timestamp
from dotenv import load_dotenv # for environment variables
import os # for environment variables
import json # for json dump
from confluent_kafka import Producer # for kafka producer
import sys # for sys.exit
import requests # for requests

load_dotenv()  # take environment variables from .env.

# bot env var
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# kafka env var
topic = 'chat-messages'
UPSTASH_KAFKA_SERVER = os.getenv("UPSTASH_KAFKA_SERVER")
UPSTASH_KAFKA_USERNAME = os.getenv('UPSTASH_KAFKA_USERNAME')
UPSTASH_KAFKA_PASSWORD = os.getenv('UPSTASH_KAFKA_PASSWORD')

conf = {
    'bootstrap.servers': UPSTASH_KAFKA_SERVER,
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'security.protocol': 'SASL_SSL',
    'sasl.username': UPSTASH_KAFKA_USERNAME,
    'sasl.password': UPSTASH_KAFKA_PASSWORD
}

producer = Producer(**conf)

# kafka acked definition
def acked(err, msg):
    if err is not None:
        print(f"Failed to deliver message: {err.str()}")
    else:
        print(f"Message produced: {msg.topic()}")

# define the prefix for the bot commands
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
# ------------------------------------------------- DISCORD EVENTS -----------------------------------------------------

# BOT READY CHECK ON CONSOLE
@bot.event
async def on_ready():
    # send message to console when bot is ready
    print('Logged in as')
    print(bot.user.name)
    print('Console Check: ChatsTodo Bot is Ready')
    
# MESSAGE LISTENER TO KAFKA
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.id == bot.user.id:
        return
    
    # this line is important for bot commands to work, 
    # otherwise it will not recognise commands as
    # it will not process them and only reads the message
    await bot.process_commands(message)
    
    # check if message is a command, if so return
    if message.content.startswith(bot.command_prefix):
        return

    # send message to kafka
    platform = "discord"
    sender_user_id = message.author.name
    group_id = message.channel.id
    timestamp = message.created_at.isoformat()
    message = message.content
    
    kafka_parcel = {"platform": platform, "sender_user_id": sender_user_id, "group_id": group_id, "timestamp": timestamp, "message": message}
    kafka_parcel_string = json.dumps(kafka_parcel)
    print(kafka_parcel_string) # print the kafka parcel string for debugging
    
    try:
        producer.produce(topic, kafka_parcel_string, callback=acked)
        producer.poll(1) 
    except Exception as e:
        print(f"Error producing message: {e}")
        # need to handle if cannot send to kafka what to do,
        # now it is an infinite loop that keeps trying to send to kafka       
        # sys.exit(f"Error producing message: {e}")

    producer.flush()

# ------------------------------------------------- DISCORD COMMANDS -----------------------------------------------------

#ping command
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
# hi command
@bot.command()
async def hi(ctx):
    await ctx.send('Hello! I am ChatsTodo Bot. I am here to help you with your tasks.\n'
                    'Here are the commands you can use:\n'
                    '!ping - Pong!\n')
    
# connect command
@bot.command()
async def connect(ctx):
    if isinstance(ctx.channel, discord.DMChannel):  # Check if the command is issued in a private channel
        api_url = "http://authentication:8080/auth/api/v1/bot/request-code"
        
        user_credentials = {"userId": str(ctx.author.id), "platform": "Discord"}
        
        response = requests.post(api_url, json=user_credentials)
        
        x = response.json()
        code = x["verification_code"]
        await ctx.send(f"Here is your code {code}")
    
# summary command
@bot.command()
async def summary(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send('Here is your summary...\n')

# run the bot with the provided token
bot.run(BOT_TOKEN)