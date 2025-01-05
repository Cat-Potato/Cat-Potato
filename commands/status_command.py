import discord
from discord import app_commands
import datetime

def setup_status_command(bot, start_time):
    @bot.tree.command(name="status", description="Wyświetla status i uptime bota")
    async def status(interaction: discord.Interaction):
        # Sprawiamy, żeby 'now' było timezone-aware
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        # Używamy przekazanego 'start_time' bez nadpisywania go
        start_time_aware = start_time.replace(tzinfo=datetime.timezone.utc)

        uptime = now - start_time_aware
        days, remainder = divmod(uptime.total_seconds(), 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_percentage = (uptime.total_seconds() / 86400) * 100  # Przyjmując 1 dzień jako 100%

        # Tworzenie paska postępu
        progress_bar_length = 20
        filled_length = int(progress_bar_length * uptime_percentage // 100)
        progress_bar = '█' * filled_length + '░' * (progress_bar_length - filled_length)

        embed = discord.Embed(title="⏳ Uptime", color=discord.Color.blue())
        embed.add_field(name="Bot działa od:", value=f"{int(days)} dni, {int(hours)} godzin, {int(minutes)} minut, {int(seconds)} sekund.", inline=False)
        embed.add_field(name="Progres uptime:", value=f"[{progress_bar}] ({uptime_percentage:.2f}%)", inline=False)
        embed.add_field(name="Data:", value=now.strftime('%d.%m.%Y'), inline=True)
        embed.add_field(name="Godzina:", value=now.strftime('%H:%M:%S'), inline=True)

        await interaction.response.send_message(embed=embed)
