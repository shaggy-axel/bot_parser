import config
import logging

from aiogram import Bot, Dispatcher, executor, types
from sqlighter import SQLighter

logging.basicConfig(filename="bot.log", level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')

#Инициализируем бота
bot = Bot(token = config.token)
dp = Dispatcher(bot)

#Инициализируем базу данных
db = SQLighter('bot_db')


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


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)

