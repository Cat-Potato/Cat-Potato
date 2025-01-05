import discord
from discord import app_commands

def setup_servers_command(bot):
    @bot.tree.command(name="servers", description="Wyświetla listę serwerów, na których jest bot (tylko dla właściciela bota)")
    async def servers(interaction: discord.Interaction):
        if interaction.user.id != 624624090866778112:
            await interaction.response.send_message("Nie masz uprawnień do użycia tej komendy.", ephemeral=True)
            return

        embed = discord.Embed(title="🌐 Serwery, na których jest bot", color=discord.Color.blue())
        embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
        embed.set_footer(text=f"Łączna liczba serwerów: {len(bot.guilds)}")

        for guild in bot.guilds:
            owner = await bot.fetch_user(guild.owner_id)
            guild_info = (
                f"**🆔 Guild ID:** {guild.id}\n"
                f"**👥 Członkowie:** {guild.member_count}\n"
                f"**👑 Właściciel:** {owner.mention}\n"
                f"**📅 Utworzony:** {guild.created_at.strftime('%d.%m.%Y')}\n"
            )
            embed.add_field(name=f"🏷️ {guild.name}", value=guild_info, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)