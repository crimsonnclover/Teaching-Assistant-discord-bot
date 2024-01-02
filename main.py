import discord
import config
from datetime import datetime
from discord.ext import tasks, commands
from start_view import StartView 
import scheduler


class TeachingAssistantBot(commands.Bot):
    events_heap = scheduler.MinHeap()


bot = TeachingAssistantBot(
    intents=discord.Intents.all(),
    command_prefix=config.PREFIX,
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
    view = StartView(root_channel, bot)
    await interaction.response.send_message("Что вам нужно?")
    await root_channel.send(view=view)


@tasks.loop(seconds=60)
async def sender():
    if len(bot.events_heap.heap) != 0:
        dt_obj = datetime.strptime(bot.events_heap.heap[-1]["dt"], '%d/%m/%y %H:%M:%S')
        if datetime.now() >= dt_obj:
            pass #TODO: написать отправку вопросов и сообщений

bot.run(config.TOKEN)
