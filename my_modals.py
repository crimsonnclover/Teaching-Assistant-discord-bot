import discord
from discord.ui import Modal, TextInput


class QuestionModal(Modal, title="Запланировать вопрос"):
    question = TextInput(label="Введите вопрос", style=discord.TextStyle.paragraph)
    answer1 = TextInput(label="Введите первый ответ")
    answer2 = TextInput(label="Введите второй ответ")
    answer3 = TextInput(label="Введите третий ответ (опционально)", required=False)
    answer4 = TextInput(label="Введите четвертый ответ (опционально)", required=False)


class InfoModal(Modal, title="Запланировать вопрос"):
    answer1 = TextInput(label="Введите заголовок")
    question = TextInput(label="Введите текст сообщения", style=discord.TextStyle.paragraph)
