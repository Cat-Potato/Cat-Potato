import discord
from discord import app_commands
import asyncio
from utils import log_message

def setup_stop_command(bot):
    @bot.tree.command(name="stop", description="Zatrzymywanie bota.(tylko dla właściciela bota)")
    async def stop(interaction: discord.Interaction):
        if interaction.user.id != 624624090866778112:
            await interaction.response.send_message("Nie masz uprawnień do użycia tej komendy.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Zatrzymywanie bota...",
            description="Bot zostanie zatrzymany za 10 sekund.",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        message = await interaction.original_response()

        countdown_art = [
            "🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥",
            "🟥🟥🟥🟥🟥🟥🟥🟥🟥⬛",
            "🟥🟥🟥🟥🟥🟥🟥🟥⬛⬛",
            "🟥🟥🟥🟥🟥🟥🟥⬛⬛⬛",
            "🟥🟥🟥🟥🟥🟥⬛⬛⬛⬛",
            "🟥🟥🟥🟥🟥⬛⬛⬛⬛⬛",
            "🟥🟥🟥🟥⬛⬛⬛⬛⬛⬛",
            "🟥🟥🟥⬛⬛⬛⬛⬛⬛⬛",
            "🟥🟥⬛⬛⬛⬛⬛⬛⬛⬛",
            "🟥⬛⬛⬛⬛⬛⬛⬛⬛⬛"
        ]

        for i in range(10, 0, -1):
            embed.description = f"Bot zostanie zatrzymany za {i} sekund.\n```\n{countdown_art[10-i]}\n```"
            await message.edit(embed=embed)
            await asyncio.sleep(1)
            log_message("WARNING", f"Bot zostanie zatrzymany za {i} sekund.")
        log_message("INFO", "Bot został zatrzymany.")
        embed.description = "Bot został zatrzymany."
        await message.edit(embed=embed)
        await bot.close()