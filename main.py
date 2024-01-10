from datetime import datetime

import discord
from discord.ext import commands, tasks

import config
import scheduler
from event import Event
from start_view import StartView
from styles import info_embed, question_embed


# extention of Bot class with min heap
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
    scheduler.db_init()
    saved_events = scheduler.db_load()
    for event in saved_events:
        e = Event(event[0], event[1], event[2], event[3], event[4], [], event[6])
        e.body_from_text(event[5])
        bot.events_heap.push(e)
    sender.start()


# info slash command
@bot.tree.command(name="info")
async def info(interaction):
    await interaction.response.send_message(embed=discord.Embed(title=config.INFO_TITLE, description=config.INFO_TEXT, color=0x563196))


# start slash command
@bot.tree.command(name="start")
async def start(interaction):
    root_channel = bot.get_channel(interaction.channel_id)
    view = StartView(root_channel, bot)
    await interaction.response.send_message(embed=discord.Embed(title="Что вам нужно?", color=0x563196), view=view)


# loop with 20 seconds interval, which checks scheduled events and sends it
@tasks.loop(seconds=20)
async def sender():
    events = []
    print(datetime.now())
    while len(bot.events_heap.heap) != 0  and \
                        datetime.now() >= datetime.strptime(bot.events_heap.heap[0].dt, '%d/%m/%y %H:%M:%S'):
        events.append(bot.events_heap.pop())
        scheduler.db_remove_by_id(events[-1].id)
    for event in events:
        channel = bot.get_channel(event.channel)
        if event.type == "question":
            await channel.send(embed=question_embed(event.header, event.body))
        elif event.type == "info":
            await channel.send(embed=info_embed(event.header, event.body[0]))


@sender.before_loop
async def before_sender():
    await bot.wait_until_ready()


# running the bot
bot.run(config.TOKEN)
