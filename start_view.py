import discord
from discord.ui import Button, View
from event import Event
from my_modals import QuestionModal, InfoModal
import utils


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


    def deactivate_buttons(self):
        self.schedule_question_button.disabled = True
        self.schedule_info_button.disabled = True
        self.list_button.disabled = True
        self.delete_button.disabled = True
        self.exit_button.disabled = True


    async def channel_choosing(self, interaction): # function that gets requiered channel name
        original_mg = interaction.message
        self.deactivate_buttons()
        await original_mg.edit(view=self)

        await self.root_channel.send("Выберите канал! Впишите # и выберете нужный канал.")
        msg = await self.bot.wait_for("message")
        choosen_channel = utils.get_channel(msg.content)
        self.event.channel = choosen_channel


    async def get_datetime(self):
        await self.root_channel.send("Напишите время, на которое запланировать вопрос. Формат dd/mm/yy HH:MM")
        msg = await self.bot.wait_for("message")
        recieved_data = utils.get_datetime(msg.content)
        self.event.dt = recieved_data


    # question button callback 
    async def schedule_question_button_callback(self, interaction: discord.Interaction):

        async def modal_on_submit(modal_interaction):
            self.event.guild = modal_interaction.guild_id
            self.event.type = "question"
            self.event.header = modal_interaction.data["components"][0]["components"][0]["value"]
            for i in range(1, 5):
                ans = modal_interaction.data["components"][i]["components"][0]["value"]
                if ans != "":
                    self.event.body.append(ans)
            await modal_interaction.response.send_message("Вопрос сохранен!")

            await self.channel_choosing(interaction)
            while self.event.channel is None:
                await self.root_channel.send("Неверный канал! Попробуйте еще раз.")
                await self.channel_choosing(interaction)

            await self.get_datetime()
            while self.event.dt is None:
                await self.root_channel.send("Неверное время! Попробуйте еще раз.")
                await self.get_datetime()

            self.bot.events_heap.push(self.event)

        qm = QuestionModal()
        qm.on_submit = modal_on_submit
        await interaction.response.send_modal(qm)


    async def schedule_info_button_callback(self, interaction: discord.Interaction):

        async def modal_on_submit(modal_interaction):
            self.event.guild = modal_interaction.guild_id
            self.event.type = "info"
            self.event.header = modal_interaction.data["components"][0]["components"][0]["value"]
            self.event.body.append(modal_interaction.data["components"][1]["components"][0]["value"])
            await modal_interaction.response.send_message("Сообщение сохранено!")

            await self.channel_choosing(interaction)
            while self.event.channel is None:
                await self.root_channel.send("Неверный канал! Попробуйте еще раз.")
                await self.channel_choosing(interaction)

            await self.get_datetime()
            while self.event.dt is None:
                await self.root_channel.send("Неверное время! Попробуйте еще раз.")
                await self.get_datetime()

            self.bot.events_heap.push(self.event)

        im = InfoModal()
        im.on_submit = modal_on_submit
        await interaction.response.send_modal(im)


    async def list_button_callback(self, interaction: discord.Interaction):
        await self.channel_choosing(interaction)
        while self.event.channel is None:
            await self.root_channel.send("Неверный канал! Попробуйте еще раз.")
            await self.channel_choosing(interaction)


    async def delete_button_callback(self, interaction: discord.Interaction):
        await self.channel_choosing(interaction)
        while self.event.channel is None:
            await self.root_channel.send("Неверный канал! Попробуйте еще раз.")
            await self.channel_choosing(interaction)


    async def exit_button_callback(self, interaction: discord.Interaction):
        self.deactivate_buttons()
        await interaction.response.edit_message(view=self)
 