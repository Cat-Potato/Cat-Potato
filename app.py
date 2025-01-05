import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os
import sys
import time
from dotenv import load_dotenv
from commands.status_command import setup_status_command
from commands.ping_command import setup_ping_command
from commands.help_command import setup_help_command
from commands.stop_command import setup_stop_command
from commands.info_command import setup_info_command
from commands.servers_command import setup_servers_command
from commands.troll_voice_command import setup_troll_voice_command
from commands.user_command import setup_user_command
from utils import log_message
from utils import animate_loading
from event_logger import setup_event_logger



load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.start_time = datetime.datetime.now(datetime.UTC)

@bot.event
async def on_ready():
    """Funkcja wywoływana, gdy bot jest gotowy."""
    custom_status = discord.CustomActivity(name=f"/help")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)
    log_message("INFO", f"\033[92mZalogowano jako {bot.user}")
    await bot.tree.sync()
    log_message("INFO", f"Liczba załadowanych komend slash: {len(bot.tree.get_commands())}")

@bot.event
async def on_command(ctx):
    log_message("INFO", f"Command '{ctx.command}' used by {ctx.author} in {ctx.guild}/{ctx.channel}")

def load_commands():
    setup_status_command(bot, bot.start_time)
    setup_ping_command(bot)
    setup_help_command(bot)
    setup_stop_command(bot)
    setup_info_command(bot)
    setup_servers_command(bot)
    setup_troll_voice_command(bot)
    setup_user_command(bot)
    setup_event_logger(bot)

if __name__ == "__main__":
    token = os.getenv('DISCORD_BOT_TOKEN')
    bot.log_channel_id = os.getenv('DISCORD_LOG_CHANNEL_ID')
    if token:
        animate_loading("Bot został uruchomiony...", duration=1.3)
        load_commands()
        bot.run(token)
    else:
        log_message("ERROR", "Brak tokena bota. Upewnij się, że plik .env zawiera poprawny token.")
