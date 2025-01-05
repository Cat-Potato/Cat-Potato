import discord
from discord import app_commands

def setup_help_command(bot):
    @bot.tree.command(name="help", description="Wyświetla dostępne komendy bota")
    async def help_command(interaction: discord.Interaction):
        embed = discord.Embed(title="Dostępne komendy", color=discord.Color.green())
        # Komenda /user
        embed.add_field(
            name="/user",
            value="Zarządzaj użytkownikami za pomocą akcji: ban, kick, timeout, untimeut",
            inline=False
        )
        # Komenda /status
        embed.add_field(
            name="/status",
            value="Wyświetla status i uptime bota",
            inline=False
        )
        # Komenda /ping
        embed.add_field(
            name="/ping",
            value="Sprawdza ping bota.",
            inline=False
        )
        # Komenda /info
        embed.add_field(
            name="/info",
            value="Wyświetla informacje o bocie.",
            inline=False
        )
        # Komenda /troll_voice
        embed.add_field(
            name="/troll_voice",
            value="Przerzuca wybranego użytkownika losowo między kanałami głosowymi.",
            inline=False
        )
        # Komenda /servers
        embed.add_field(
            name="/servers",
            value="Wyświetla listę serwerów, na których jest bot (tylko dla właściciela bota).",
            inline=False
        )
        # Komenda /stop
        embed.add_field(
            name="/stop",
            value="Zatrzymywanie bota.(tylko dla właściciela bota)",
            inline=False
        )

        await interaction.response.send_message(embed=embed)
