import asyncio

import discord
from discord.ui import Button, View

import scheduler
import utils
from event import Event
from styles import (InfoModal, QuestionModal, green_embed, orange_embed, red_embed)


# the main view class, which describes all interaction on the /start command. 
class StartView(View): 
    # initialization of StartView class. Every /start call is an object of this class
    def __init__(self, root_channel, bot, timeout: float | None = 180): 
        super().__init__(timeout=timeout)
        self.root_channel = root_channel # channel of /start call
        self.bot = bot # bot of /start call
        self.event = Event() # Event object, question/information scheduled in /start call

        # buttons and button callbacks initialization
        self.schedule_question_button = Button(
            custom_id="schedule_question",
            label="Запланировать вопрос",
            style=discord.ButtonStyle.green,
        )
        self.schedule_question_button.callback = self.schedule_question_button_callback

        self.schedule_info_button = Button(
            custom_id="schedule_info",
            label="Запланировать информацию",
            style=discord.ButtonStyle.green,
        )
        self.schedule_info_button.callback = self.schedule_info_button_callback

        self.list_button = Button(
            custom_id="list",
            label="Вывести список всех запланированных событий",
            style=discord.ButtonStyle.green,
        )
        self.list_button.callback = self.list_button_callback

        self.delete_button = Button(
            custom_id="delete",
            label="Удалить событие",
            style=discord.ButtonStyle.green,
        )
        self.delete_button.callback = self.delete_button_callback

        self.exit_button = Button(   
            custom_id="exit",
            label="Выход",
            style=discord.ButtonStyle.green,
        )
        self.exit_button.callback = self.exit_button_callback

        self.add_item(self.schedule_question_button)
        self.add_item(self.schedule_info_button)
        self.add_item(self.list_button)
        self.add_item(self.delete_button)
        self.add_item(self.exit_button)


    # function for deactivate buttons after interactions with ones
    def deactivate_buttons(self):
        self.schedule_question_button.disabled = True
        self.schedule_info_button.disabled = True
        self.list_button.disabled = True
        self.delete_button.disabled = True
        self.exit_button.disabled = True


    # function that gets requared channel name
    async def get_channel(self, interaction):
        original_mg = interaction.message
        self.deactivate_buttons()
        await original_mg.edit(view=self)

        await self.root_channel.send(embed=orange_embed("📰 Выберите канал!", "Впишите # и выберете нужный канал."))
        msg = await self.bot.wait_for("message")
        choosen_channel = utils.get_channel(msg.content)
        self.event.channel = choosen_channel


    # function that gets requared datetime
    async def get_datetime(self):
        await self.root_channel.send(embed=orange_embed("🕐 Напишите время, на которое запланировать вопрос.", "Формат dd/mm/yy HH:MM, без секунд"))
        msg = await self.bot.wait_for("message")
        recieved_data = utils.get_datetime(msg.content)
        self.event.dt = recieved_data


    async def schedule_question_button_callback(self, interaction: discord.Interaction):

        async def modal_on_submit(modal_interaction):
            self.event.id = modal_interaction.data["custom_id"][:10]
            self.event.guild = modal_interaction.guild_id
            self.event.type = "question"
            self.event.header = modal_interaction.data["components"][0]["components"][0]["value"]
            for i in range(1, 5):
                ans = modal_interaction.data["components"][i]["components"][0]["value"]
                if ans != "":
                    self.event.body.append(ans)
            await modal_interaction.response.send_message(embed=green_embed("✅ Вопрос сохранен!"))

            await self.get_channel(interaction)
            while self.event.channel is None:
                await self.root_channel.send(embed=red_embed("❌ Неверный канал!", "Попробуйте еще раз."))
                await self.get_channel(interaction)

            await self.get_datetime()
            while self.event.dt is None:
                await self.root_channel.send(embed=red_embed("❌ Неверное время!", "Попробуйте еще раз."))
                await self.get_datetime()

            self.bot.events_heap.push(self.event)
            scheduler.db_append(self.event)
            await self.root_channel.send(embed=green_embed("✅ Вопрос запланирован!"))

        qm = QuestionModal()
        qm.on_submit = modal_on_submit
        await interaction.response.send_modal(qm)


    async def schedule_info_button_callback(self, interaction: discord.Interaction):

        async def modal_on_submit(modal_interaction):
            self.event.id = modal_interaction.data["custom_id"][:10]
            self.event.guild = modal_interaction.guild_id
            self.event.type = "info"
            self.event.header = modal_interaction.data["components"][0]["components"][0]["value"]
            self.event.body.append(modal_interaction.data["components"][1]["components"][0]["value"])
            await modal_interaction.response.send_message(embed=green_embed("✅ Сообщение сохранено!"))

            await self.get_channel(interaction)
            while self.event.channel is None:
                await self.root_channel.send(embed=red_embed("❌ Неверный канал!", "Попробуйте еще раз."))
                await self.get_channel(interaction)
            
            await self.get_datetime()
            while self.event.dt is None:
                await self.root_channel.send(embed=red_embed("❌ Неверное время!", "Попробуйте еще раз."))
                await self.get_datetime()

            self.bot.events_heap.push(self.event)
            scheduler.db_append(self.event)
            await self.root_channel.send(embed=green_embed("✅ Сообщение запланировано!"))

        im = InfoModal()
        im.on_submit = modal_on_submit
        await interaction.response.send_modal(im)


    async def list_button_callback(self, interaction: discord.Interaction):
        await self.get_channel(interaction)
        while self.event.channel is None:
            await self.root_channel.send(embed=red_embed("❌ Неверное время!", "Попробуйте еще раз."))
            await self.get_channel(interaction)

        events_list = scheduler.db_get_by_channel(self.event.channel)
        if not len(events_list):
            await self.root_channel.send(embed=orange_embed("❕ В этом канале нет запланированных сообщений"))
        else:
            desc = []
            for event in events_list:
                desc.append(event[3] + ": " + event[4][:max(len(event[4]), 30)] + " " + event[6])
            await self.root_channel.send(embed=orange_embed("📰 Список запланированных сообщений в этом канале:",
                                                                        "\n".join(desc)))


    async def delete_button_callback(self, interaction: discord.Interaction):
        await self.get_channel(interaction)
        while self.event.channel is None:
            await self.root_channel.send(embed=red_embed("❌ Неверное время!", "Попробуйте еще раз."))
            await self.get_channel(interaction)

        events_list = scheduler.db_get_by_channel(self.event.channel)
        if not len(events_list):
            await self.root_channel.send(embed=orange_embed("❕ В этом канале нет запланированных сообщений"))
        else:
            desc = []
            for event in events_list:
                desc.append("id " + event[0] + ": " + event[4][:max(len(event[4]), 30)] + " " + event[6])
            await self.root_channel.send(embed=orange_embed("📰 Список запланированных сообщений в этом канале. Скопируйте и отправте id того, которое хотите удалить:",
                                                             "\n".join(desc)))
            id = await self.bot.wait_for("message")
            scheduler.db_remove_by_id(id.content)
            self.bot.events_heap.remove(id.content)
            await self.root_channel.send(embed=green_embed("✅ Сообщение удалено!"))


    async def exit_button_callback(self, interaction: discord.Interaction):
        self.deactivate_buttons()
        await interaction.response.edit_message(view=self)
 