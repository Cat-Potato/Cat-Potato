import discord
from discord import app_commands

def setup_info_command(bot):
    @bot.tree.command(name="info", description="Wyświetla informacje o bocie")
    async def info(interaction: discord.Interaction):
        embed = discord.Embed(
            title="ℹ️ Informacje o bocie",
            description="Szczegółowe informacje o bocie",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
        embed.add_field(name="👤 Autor", value="[Potato Cat](https://github.com/Cat-Potato/)", inline=False)
        embed.add_field(name="🛠️ Wersja", value="1.0.1", inline=True)
        embed.add_field(name="🗣️ Język", value="Python", inline=True)
        embed.add_field(name="📚 Biblioteka", value="[discord.py](https://discordpy.readthedocs.io/en/stable/)", inline=False)
        embed.add_field(name="🌐 Serwery", value=len(bot.guilds), inline=True)
        embed.add_field(name="📜 Komendy", value=len(bot.tree.get_commands()), inline=True)
        embed.set_footer(text="Dziękujemy za korzystanie z naszego bota!")
        await interaction.response.send_message(embed=embed)