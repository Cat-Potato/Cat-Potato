import discord
from discord import app_commands

def setup_ping_command(bot):
    @bot.tree.command(name="ping", description="Sprawdza ping bota.")
    async def ping(interaction: discord.Interaction):
        latency = bot.latency  # Opóźnienie bota w sekundach
        # Tworzymy embed z odpowiedzią
        embed = discord.Embed(
            title="🏓 Opóźnienie Bota",
            color=discord.Color.green()  # Kolor okna embed
        )
        # Dodajemy pole do embed z wartością opóźnienia
        embed.add_field(
            name="",
            value=f"Ping bota wynosi: **{latency * 1000:.2f} ms**",
            inline=False
        )
        # Wysłanie odpowiedzi z embed
        await interaction.response.send_message(embed=embed)
