import discord
from discord.ui import Button, View
import utils
from event import Event
from my_modals import QuestionModal, InfoModal


# the main view class, which describes all interaction on the /start command. 
class ButtonsView(View): 
    def __init__(self, root_channel, bot, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        self.root_channel = root_channel
        self.bot = bot
        self.event = Event()

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


    async def channel_choosing(self, interaction):
        original_mg = interaction.message
        self.deactivate_buttons()
        await original_mg.edit(view=self)

        await self.root_channel.send("Выберите канал!")
        msg = await self.bot.wait_for("message")
        choosen_channel = utils.get_channel(msg.content)
        self.event.channel = choosen_channel


    async def schedule_question_button_callback(self, interaction: discord.Interaction):
        a = QuestionModal()
        await interaction.response.send_modal(a)

        self.event.guild = interaction.guild_id

        if self.event.channel is None:
            await self.root_channel.send("Неверный канал! Попробуйте еще раз.")
            await self.channel_choosing(interaction)


    async def schedule_info_button_callback(self, interaction: discord.Interaction):
        await self.channel_choosing(interaction)


    async def list_button_callback(self, interaction: discord.Interaction):
        await self.channel_choosing(interaction)


    async def delete_button_callback(self, interaction: discord.Interaction):
        await self.channel_choosing(interaction)


    async def exit_button_callback(self, interaction: discord.Interaction):
        self.deactivate_buttons()
        await interaction.response.edit_message(view=self)
 