import discord
from discord.interactions import Interaction
from discord.ui import Modal, TextInput


class QuestionModal(Modal, title="Запланировать вопрос"):
    question = TextInput(label="Введите вопрос", style=discord.TextStyle.paragraph)
    answer1 = TextInput(label="Введите первый ответ")
    answer2 = TextInput(label="Введите второй ответ")
    answer3 = TextInput(label="Введите третий ответ (опционально)", required=False)
    answer4 = TextInput(label="Введите четвертый ответ (опционально)", required=False)

    async def on_submit(self, interaction) -> None:
        return await super().on_submit(interaction)


class InfoModal(Modal, title="Запланировать вопрос"):
    info = TextInput(label="Введите сообщение", style=discord.TextStyle.paragraph)
    date = TextInput(label="Введите дату и время, когда планировать сообщение. Формат YY-MM-DD H:M")
