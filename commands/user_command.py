import discord
from discord import app_commands
from utils import log_message
from datetime import timedelta
from event_logger import log_to_channel

ACTIONS = ["ban", "timeout", "untimeout", "kick"]

async def action_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=action, value=action) for action in ACTIONS if current.lower() in action.lower()]

def setup_user_command(bot):
    @bot.tree.command(name="user", description="Zarządzaj użytkownikami za pomocą akcji: ban, kick, timeout, untimeut")
    @app_commands.describe(user="Użytkownik do zarządzania", action="Akcja do wykonania: ban, kick, timeout, untimeut", duration="Czas trwania akcji (w minutach)", reason="Powód akcji")
    @app_commands.autocomplete(action=action_autocomplete)
    async def user(interaction: discord.Interaction, user: discord.Member, action: str, duration: str = None, reason: str = None):
        if action not in ACTIONS:
            await interaction.response.send_message("Nieprawidłowa akcja. Użyj 'ban', 'kick', 'timeout' lub 'untimeut'.", ephemeral=True)
            return

        if action == "ban" and not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("Nie masz uprawnień do banowania użytkowników.", ephemeral=True)
            return
        elif action == "kick" and not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("Nie masz uprawnień do wyrzucania użytkowników.", ephemeral=True)
            return
        elif action == "timeout" and not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("Nie masz uprawnień do timeoutowania użytkowników.", ephemeral=True)
            return
        elif action == "untimeout" and not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("Nie masz uprawnień do odtimeoutowania użytkowników.", ephemeral=True)
            return

        try:
            if action == "ban":
                await user.send(f"Zostałeś zbanowany na serwerze {interaction.guild.name}. Powód: {reason}")
                await interaction.guild.ban(user, reason=reason)
                await interaction.response.send_message(f"Użytkownik {user} został zbanowany.", ephemeral=True)
            elif action == "kick":
                await user.send(f"Zostałeś wyrzucony z serwera {interaction.guild.name}. Powód: {reason}")
                await interaction.guild.kick(user, reason=reason)
                await interaction.response.send_message(f"Użytkownik {user} został wyrzucony.", ephemeral=True)
                embed = discord.Embed(
                    title="Użytkownik został wyrzucony",
                    description="",
                    color=discord.Color.red()
                )
                embed.add_field(name="Kto:", value=f"<@{user.id}>", inline=False)
                if reason is None:
                    reason = "Brak powodu"
                embed.add_field(name="Powód:", value=reason, inline=False)
                embed.add_field(name="Przez użytkownika:", value=f"<@{interaction.user.id}>", inline=False)
                embed.set_footer(text=f"User ID: {user.id}")
                await log_to_channel(bot, embed)
            elif action == "timeout":
                duration_seconds = int(duration) * 60
                await user.send(f"Zostałeś timeoutowany na serwerze ({interaction.guild.name}) na {duration} minut. Powód: {reason}")
                await user.timeout(timedelta(seconds=duration_seconds), reason=reason)
                await interaction.response.send_message(f"Użytkownik <@{user.id}> został timeoutowany na {duration} minut.", ephemeral=True)
                embed = discord.Embed(
                    title="Użytkownik dostaje timeout",
                    description="",
                    color=discord.Color.red()
                )
                embed.add_field(name="Kto:", value=f"<@{user.id}>", inline=False)
                embed.add_field(name="Czas trwania:", value=f"{duration} minut", inline=False)
                if reason is None:
                    reason = "Brak powodu"
                embed.add_field(name="Powód:", value=reason, inline=False)
                embed.add_field(name="Przez użytkownika:", value=f"<@{interaction.user.id}>", inline=False)
                embed.set_footer(text=f"User ID: {user.id}")
                await log_to_channel(bot, embed)
            elif action == "untimeout":
                await user.send(f"Twój timeout na serwerze {interaction.guild.name} został zakończony. Powód: {reason}")
                await user.timeout(None, reason=reason)
                await interaction.response.send_message(f"Użytkownik {user} został odtimeoutowany.", ephemeral=True)
                embed = discord.Embed(
                    title="Użytkownik dostaje untimeout",
                    description="",
                    color=discord.Color.green()
                )
                embed.add_field(name="Kto:", value=f"<@{user.id}>", inline=False)
                if reason is None:
                    reason = "Brak powodu"
                embed.add_field(name="Powód:", value=reason, inline=False)
                embed.add_field(name="Przez użytkownika:", value=f"<@{interaction.user.id}>", inline=False)
                embed.set_footer(text=f"User ID: {user.id}")
                await log_to_channel(bot, embed)
        except discord.Forbidden:
            await interaction.response.send_message("Nie mogłem wysłać wiadomości do użytkownika.", ephemeral=True)
