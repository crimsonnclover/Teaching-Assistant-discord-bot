import discord
import config
from discord.ui import Button, View, Select, Modal
from discord.ext import commands
import start_view


bot_config = {
    'token': config.TOKEN,
    'prefix': config.PREFIX,
}

bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix=bot_config['prefix'],
)


@bot.event
async def on_ready():
    try:
        print("Bot is ups and ready!")
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as ex:
        print(ex)


@bot.tree.command(name="info")
async def info(iteraction):
    root_channel = bot.get_channel(iteraction.channel_id)
    await root_channel.send(config.INFO_TEXT)


@bot.tree.command(name="start")
async def start(interaction):
    root_channel = bot.get_channel(interaction.channel_id)
    view = start_view.ButtonsView(root_channel, bot)
    await interaction.response.send_message("Что вам нужно?")
    await root_channel.send(view=view)


bot.run(bot_config['token'])
