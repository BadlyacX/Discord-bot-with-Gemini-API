import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import google.generativeai as genai

load_dotenv()

token = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=token)

model = genai.GenerativeModel('gemini-1.5-flash-8b')

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.dm_messages = True 
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        prompt = message.content
        try:
            response = model.generate_content(prompt)
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")
        return

    if bot.user.mentioned_in(message):
        prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if prompt:
            try:
                response = model.generate_content(prompt)
                await message.channel.send(response.text)
            except Exception as e:
                await message.channel.send(f"Error: {str(e)}")
        else:
            await message.channel.send("Please provide a prompt after mentioning me.")

DISCORD_TOKEN = os.getenv("BOTTOKEN")
bot.run(DISCORD_TOKEN)
