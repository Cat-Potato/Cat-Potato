import discord
from utils import log_message
from utils import log_to_channel

def setup_event_logger(bot):
    @bot.event
    async def on_message_delete(message):
        if message.author.bot:
            return
        chanale = message.channel.id
        embed = discord.Embed(
            title="Usnięta wiadomość",
            description=f"Wiadomość od <@{message.author.id}> na <#{chanale}> została usunięta.",
            color=discord.Color.red()
        )
        embed.add_field(name="Treść", value=message.content or "*Brak treści*", inline=False)
        embed.set_footer(text=f"User ID: {message.author.id}")
        await log_to_channel(bot, embed)

    @bot.event
    async def on_message_edit(before, after):
        if before.author.bot:
            return
        if before.content is None and after.content is None:
            return  # Exit if both contents are None
        chanale = before.channel.id
        embed = discord.Embed(
            title="Edytowana wiadomość",
            description=f"Wiadomość na <#{chanale}> autorstwa <@{before.author.id}> została edytowana.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Przed", value=before.content or "*Brak treści*", inline=False)
        embed.add_field(name="Teraz", value=after.content or "*Brak treści*", inline=False)
        embed.set_footer(text=f"User ID: {before.author.id}")
        await log_to_channel(bot, embed)


    @bot.event
    async def on_member_ban(guild, user):
        embed = discord.Embed(
            title="Użyktownik zbanowany",
            description=f"{user} został zbanowany w {guild}.",
            color=discord.Color.red()
        )
        embed.set_footer(text=f"User ID: {user.id}")
        await log_to_channel(bot, embed)

    @bot.event
    async def on_member_unban(guild, user):
        embed = discord.Embed(
            title="Użyktownik odblokowany",
            description=f"{user} został odbanowany.",
            color=discord.Color.green()
        )
        embed.set_footer(text=f"User ID: {user.id}")
        await log_to_channel(bot, embed)

    @bot.event
    async def on_member_update(before, after):
        if before.roles != after.roles:
            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            embed = discord.Embed(
                title="Zaktualizowano role użyktownika",
                description=f"Role zaktualizowane dla {before}",
                color=discord.Color.blue()
            )

            if added_roles:
                embed.add_field(name="Dodano Role", value=", ".join(role.name for role in added_roles), inline=False)
            if removed_roles:
                embed.add_field(name="Usunięto Role", value=", ".join(role.name for role in removed_roles), inline=False)

            embed.set_footer(text=f"User ID: {before.id}")
            await log_to_channel(bot, embed)

    @bot.event
    async def on_guild_role_create(role):
        guild = role.guild

        # Pobranie dzienników audytu dla utworzenia roli
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_create):
            if entry.target.id == role.id:
                creator = entry.user
                break
        else:
            creator = None

        # Tworzenie embedu
        embed = discord.Embed(
            title="Nowa rola utworzona",
            description=f"Rola: `{role.name}`",
            color=discord.Color.green(),
        )
        embed.add_field(name="ID roli", value=role.id, inline=True)
        embed.add_field(name="Kolor roli", value=str(role.color), inline=True)
        embed.add_field(name="Pozycja roli", value=role.position, inline=True)

        if creator:
            embed.add_field(name="Utworzona przez", value=f"{creator} ({creator.id})", inline=False)
        else:
            embed.add_field(name="Utworzona przez", value="Nieznane", inline=False)

        embed.set_footer(text=f"Data utworzenia: {role.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        await log_to_channel(bot, embed)

    @bot.event
    async def on_guild_role_delete(role):
        guild = role.guild

        # Pobranie dzienników audytu dla usunięcia roli
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
            if entry.target.id == role.id:
                deleter = entry.user
                break
        else:
            deleter = None

        # Tworzenie embedu
        embed = discord.Embed(
            title="Rola usunięta",
            description=f"Rola: `{role.name}`",
            color=discord.Color.red(),
        )
        embed.add_field(name="ID roli", value=role.id, inline=True)

        if deleter:
            embed.add_field(name="Usunięta przez", value=f"{deleter} ({deleter.id})", inline=False)
        else:
            embed.add_field(name="Usunięta przez", value="Nieznane", inline=False)

        await log_to_channel(bot, embed)
