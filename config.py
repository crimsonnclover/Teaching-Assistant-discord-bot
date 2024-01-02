import discord_bot.config

# discord bot token
TOKEN = discord_bot.config.TOKEN

# discord bot prefix
PREFIX = discord_bot.config.PREFIX

# SQLLite DB path, data/scheduler.db by default
DB_PATH = discord_bot.config.DB_PATH

INFO_TEXT = ''' 
Описание функционала: \n
/start - основная команда. с помощью нее можно работать с вопросами и рассылками: планировать их, удалять, просматривать, просто нажав на нужную кнопку. \n
Вы можете запланировать сообщение в удобное вам время, например во время онлайн занятия, и бот сам отправит в это время вопрос/информацию. \n
Как лучше использовать: \n
Удобно создать отдельный канал для взаимодействия с ботом, чтобы учебные чаты не засорялись, и в нем планировать все события. Также нужно определить уровни доступа к боту, сделав его доступным только для администраторов/преподователей, сделать это можно в настройках.
'''

INFO_TITLE = "Привет! Это TeachingAssistantBot. Бот создан для того, чтобы сделать процесс обучения более легким и приятным."
