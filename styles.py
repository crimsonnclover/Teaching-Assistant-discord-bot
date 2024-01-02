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


def green_embed(title: str, description: str = ""):
    return discord.Embed(title=title, description=description, color=0x00ff00)


def red_embed(title: str, description: str = ""):
    return discord.Embed(title=title, description=description, color=0xe11409)


def orange_embed(title: str, description: str = ""):
    return discord.Embed(title=title, description=description, color=0xe77e40)


def info_embed(title: str, description: str):
    return discord.Embed(title=("ℹ️" + title), description=description, color=0x818d98)


def question_embed(title:str, answers: list[str]):
    emojis = {0: "1️⃣", 1: "2️⃣", 2: "3️⃣", 3: "4️⃣"}
    answers_updated = []
    for i in range(len(answers)):
        answers_updated[i] = emojis[i] + answers[i]
    desc = "\n".join(answers_updated) + "\n" + "Голосуй с помощью эмоджи 1️⃣ 2️⃣ 3️⃣ 4️⃣!"

    return discord.Embed(title=("❔" + title), description=desc)
