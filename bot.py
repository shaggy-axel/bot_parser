import config
import logging

import asyncio
from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter
from stopgame import StopGame

logging.basicConfig(filename="bot.log", level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

#Инициализируем бота
bot = Bot(token = config.token)
dp = Dispatcher(bot)

#Инициализируем базу данных
db = SQLighter('bot_db')

# инициализируем парсер
sg = StopGame('lastkey.txt')

poll = 10

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	""" Команда подписки """

	if(not db.subscriber_exists(message.from_user.id)):
		#Если юзера нет в базе добавляем его
		db.add_subscriber(message.from_user.id)
	else:
		#Если он уже есть в базе данных
		db.update_subscribtion(message.from_user.id, True)

	await message.answer("Вы подписались на уведомления")


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	""" Команда отписки """

	if(not db.subscriber_exists(message.from_user.id)):
		db.add_subscriber(message.from_user.id, False)
	else:
		#Если он уже есть в базе данных
		db.update_subscribtion(message.from_user.id, False)
	await message.answer("Вы отписались от уведомлений")


# проверяем наличие новых игр и делаем рассылки
async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		# проверяем наличие новых игр
		new_games = sg.new_games()

		if(new_games):
			# если игры есть, переворачиваем список и итерируем
			new_games.reverse()
			for ng in new_games:
				# парсим инфу о новой игре
				nfo = sg.game_info(ng)

				# получаем список подписчиков бота
				subscriptions = db.get_subscribtions()

				# отправляем всем новость
				with open(sg.download_image(nfo['image']), 'rb') as photo:
					for s in subscriptions:
						await bot.send_photo(
							s[1],
							photo,
							caption = nfo['title'] + "\n" + "Оценка: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" + nfo['link'],
							disable_notification = True
						)
				
				# обновляем ключ
				sg.update_lastkey(nfo['id'])


if __name__ == '__main__':
	dp.loop.create_task(scheduled(poll)) # пока что оставим 10 секунд (в качестве теста)	
	executor.start_polling(dp, skip_updates=True)

