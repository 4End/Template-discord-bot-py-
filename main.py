import nextcord
from nextcord.ext import commands
from config import TOKEN
intents = nextcord.Intents.all()


client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command("help")


@client.event
async def on_ready():
    print('Bot is ready')


client.run(TOKEN)

