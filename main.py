import nextcord
from nextcord.ext import commands
from config import TOKEN
from config import botcolor
from config import botname
from verify import emojiconfig
from verify import messageidconfig
from verify import rolename
import asyncio
intents = nextcord.Intents.all()


client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command("help")
client.remove_command('say')

@client.event
async def on_ready():
    members = 0
    for guild in client.guilds:
        members += guild.member_count - 1

    await client.change_presence(
        activity=nextcord.Activity(
            type=nextcord.ActivityType.watching, name=f"[{members}] members"
        )
    )
    print('Bot is ready')

class Verify(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label=f"Click here to get {rolename}", style=nextcord.ButtonStyle.red)
    async def accept(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        role = [role for role in await interaction.guild.fetch_roles() if role.name == rolename]
        await interaction.user.add_roles(role[0])
        await interaction.response.send_message(f"You got {rolename}", ephemeral=True)




# @client.event
# async def on_raw_reaction_add(payload):
#     ourMessageID = messageidconfig
#
#
#     if ourMessageID == payload.message_id:
#         member = payload.member
#         guild = member.guild
#         emoji = payload.emoji.name
#         if emoji == emojiconfig:
#             role = nextcord.utils.get(guild.roles, name=rolename)
#             await member.add_roles(role)



@client.command()
async def disverify(ctx, *, message):
    await ctx.message.delete()
    em = nextcord.Embed(color=botcolor, title=botname, description=f'{message}', timestamp=ctx.message.created_at)
    em.set_footer(text=botname)

    button = Verify()
    msg = await ctx.send(embed=em, view=button)
    # await msg.add_reaction(emojiconfig)




@client.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    em = nextcord.Embed(color=botcolor, title=botname, description=f'{message}', timestamp=ctx.message.created_at)
    em.set_footer(text=botname)
    await ctx.send(embed=em)

@commands.has_permissions(kick_members=True)
async def forcekick(ctx, member: nextcord.Member):
    await ctx.message.delete()

    message = await ctx.send(f'are you sure you want to kick {member}?')
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user

    try:
        reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)
    except asyncio.TimeoutError:
        await message.edit(content='Kick cancelled, timed out.', delete_after=5)
        return

    if str(reaction.emoji) == '✅':
        await member.kick()
        await message.edit(content=f'{member} has been kicked.', delete_after=3)
        return

    await message.edit(content='kick cancelled.', delete_after=5)

@client.command()
@commands.has_permissions(ban_members=True)
async def forceban(ctx, member: nextcord.Member):
    await ctx.message.delete()


    message = await ctx.send(f"Are you sure you want to ban {member}?")
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    check = lambda r, u: u == ctx.author and str(r.emoji) in "✅❌"  # r=reaction, u=user

    try:
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=30)
    except asyncio.TimeoutError:
        await message.edit(content="Ban cancelled, timed out.")
        return

    if str(reaction.emoji) == "✅":
        await member.ban()
        await message.edit(content=f"{member} has been banned.", delete_after=3)
        return

    await message.edit(content="Ban cancelled.", delete_after=5)


client.run(TOKEN)

