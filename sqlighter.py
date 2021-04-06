import sqlite3

class SQLighter:

	def __init__(self, database_file):
		""" Подключаемся к базе данных """
		self.connection = sqlite3.connect(database_file)
		self.cursor = self.connection.cursor()

	def get_subscribtions(self, status = True):
		""" Получаем подписки """
		with self.connection:
			return self.cursor.execute("SELECT * FROM `subscribes` WHERE `status` = ?",(status,)).fetchall()

	def subscriber_exists(self, chat_id):
		""" Проверяем подписку """
		with self.connection:
			result = self.cursor.execute("SELECT * FROM `subscribes` WHERE `chat_id` = ?",(chat_id,)).fetchall()
			return bool(len(result))

	def add_subscriber(self, chat_id, status = True):
		""" Добавляем подписку """
		with self.connection:
			return self.cursor.execute("INSERT INTO `subscribes` (`chat_id`, `status`) VALUES (?,?)",(chat_id, status,))

	def update_subscribtion(self, chat_id, status):
		""" Обновляем подписку """
		return self.cursor.execute("UPDATE `subscribes` SET `status` = ? WHERE `chat_id` = ?",(status, chat_id,))

	def close(self):
		""" Отключаем базу данных """
		self.connection.close()

