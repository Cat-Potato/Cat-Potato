import discord
from discord import app_commands
import random
import asyncio
import time
from utils import log_message
from discord.ext import commands
from utils import log_to_channel

def cooldown_key(interaction: discord.Interaction):
    return interaction.user.id

cooldowns = commands.CooldownMapping.from_cooldown(1, 20.0, cooldown_key)

def setup_troll_voice_command(bot):
    @bot.tree.command(name="troll_voice", description="Przerzuca wybranego użytkownika losowo między kanałami głosowymi.")
    @app_commands.describe(user="Użytkownik do przerzucania", duration="Czas trwania przerzucania w sekundach (Domyślnie: 20) (Maksymalnie: 60)", notify="Czy powiadomić użytkownika przez DM (Domyślnie: Nie)", interval="Interwał między przenosinami w sekundach (Domyślnie: 0.5)")
    async def troll(interaction: discord.Interaction, user: discord.Member, duration: int = 20, notify: bool = False, interval: float = 0.5):
        bucket = cooldowns.get_bucket(interaction)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await interaction.response.send_message(f"Proszę czekać {retry_after:.2f} sekund przed ponownym użyciem tej komendy.", ephemeral=True)
            return

        if not interaction.user.guild_permissions.move_members:
            await interaction.response.send_message("Nie masz permisji.", ephemeral=True)
            return

        if not interaction.guild.me.guild_permissions.move_members:
            await interaction.response.send_message("Bot nie ma permisji na serwerze do `Przenoszenia członków.`", ephemeral=True)
            return

        if interaction.guild.me.top_role <= user.top_role:
            await interaction.response.send_message("Bot nie ma wystarczającej roli, aby przenieść tego użytkownika.", ephemeral=True)
            return

        if not user.voice or not user.voice.channel:
            await interaction.response.send_message("Użytkownik nie jest na kanale głosowym.", ephemeral=True)
            return

        if duration > 60:
            await interaction.response.send_message("Maksymalny czas trwania to 60 sekund. \n-# Poproś <@624624090866778112> jeśli dla ciebie to za mało", ephemeral=True)
            return

        original_channel = user.voice.channel
        voice_channels = [channel for channel in interaction.guild.voice_channels if channel != original_channel and channel.permissions_for(user).connect]

        if not voice_channels:
            await interaction.response.send_message("Brak innych kanałów głosowych do przerzucania.", ephemeral=True)
            return

        server_name = interaction.guild.name
        await interaction.response.send_message(f"Przerzucanie {user.mention} między losowymi kanałami głosowymi przez {duration} sekund.", ephemeral=True)
        if notify:
            try:
                await user.send(f"Zostałeś strolowany przez {interaction.user.mention}.")
            except discord.DiscordException as e:
                log_message("ERROR", f"Error sending DM to {user} on server {server_name}: {e}")
        end_time = time.time() + duration
        embed = discord.Embed(
            title="Trollowanie użytkownika",
            description=f"",
            color=discord.Color.red()
        )
        embed.add_field(name="Kto:", value=f"{user.mention}", inline=False)
        embed.add_field(name="Czas trwania:", value=f"{duration} sekund", inline=False)
        embed.add_field(name="Przez użytkownika:", value=f"{interaction.user.mention}", inline=False)
        await log_to_channel(bot, embed)
        while time.time() < end_time:
            new_channel = random.choice(voice_channels)
            if not interaction.guild.me.guild_permissions.move_members:
                await interaction.followup.send(f"Bot stracił permisje do przenoszenia członków.", ephemeral=True)
                return
            try:
                await user.move_to(new_channel)
            except discord.DiscordException as e:
                if e.code == 40032:  # Target user is not connected to voice
                    await interaction.followup.send(f"Użytkownika {user.mention} już nie jest na kanale głosowym.", ephemeral=True)
                    return
                elif e.code == 50013:  # Missing Permissions
                    await interaction.followup.send(f"Bot nie ma permisji, aby przenieść {user.mention}.", ephemeral=True)
                    log_message("INFO", f"{e.code}")
                    return
                elif isinstance(e, discord.NotFound):  # Channel not found
                    voice_channels.remove(new_channel)
                    if not voice_channels:
                        await interaction.followup.send("Brak innych kanałów głosowych do przerzucania.", ephemeral=True)
                        return
                log_message("ERROR", f"Error moving {user} to {new_channel} on server {server_name}: {e}")
            await asyncio.sleep(interval)

        # Ensure the user is moved back to the original channel
        if not interaction.guild.me.guild_permissions.move_members:
            await interaction.followup.send(f"Bot stracił permisje do przenoszenia członków.", ephemeral=True)
            return
        try:
            await user.move_to(original_channel)
        except discord.DiscordException as e:
            if e.code == 40032:  # Target user is not connected to voice
                return
            elif e.code == 50013:  # Missing Permissions
                await interaction.followup.send(f"Bot nie ma permisji, aby przenieść {user.mention}.", ephemeral=True)
                return
            log_message("ERROR", f"Error moving {user} back to {original_channel} on server {server_name}: {e}")
