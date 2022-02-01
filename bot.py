import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import pickledb
import config
from os import listdir
from config import isFile
import asyncio
import os
import keyboards as kb

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def starting_mail(message: types.Message):
	await message.answer("Приветствую тебя в почтовом клиенте *Telegram Mail*\nЗдесь ты сможешь создать свою телеграмм почту и принимать сообщения.\nЧтобы зарегистрировать почту, напиши /register",parse_mode="markdown")

@dp.message_handler(commands=["register"])
async def registration_mail(message: types.Message):
	if isFile("users/"+str(message.from_user.id)+".json"):
		await message.answer("Извините, но у вас уже есть почта.")
	else:
		await message.answer("Запущен процесс регистрации в сети Telegram Mail.\nРегистрируясь вы соглашаетесь со следующими документами:\nПолитика Конфиденциальности - https://clck.ru/aqLCD\nУсловия пользования - https://clck.ru/arPfM", reply_markup=kb.reg_markup)

@dp.message_handler(commands=["edit","change"])
async def change_user_mail(message: types.Message):
	if isFile("users/"+str(message.from_user.id)+".json"):
		ms, ml = message.get_args().split()
		if "@telegram.org" in ml:
			m = ms.replace("@telegram.org", "")
			current_user = pickledb.load("users/"+str(message.from_user.id)+".json", False)
			current_mail = pickledb.load("mails/"+m+".json", False)
			current_id = current_mail.get("id")
			if current_id == message.from_user.id:
				current_mail.set("mail", ml)
				current_user.set("mail", ml)
				current_user.dump()
				current_mail.dump()
				mk = ml.replace("@telegram.org", "")
				os.rename("mails/"+m+".json","mails/"+mk+".json")
				message.answer("Ваш ник-нейм успешно изменён!\nВы можете проверить это, введя комманду /info")
			else:
				await message.answer("Извините, но это не ваша почта!")
		else:
			await message.answer("Неккоректный второй аргумент")
	else:
		await message.answer("Для того, чтобы менять почту, её нужно создать😉")

@dp.message_handler(commands=["reset"])
async def remove_user_mail(message: types.Message):
	if config.isFile("users/"+str(message.from_user.id)+".json"):
		rem_mail = message.get_args()
		if "@telegram.org" in rem_mail:
			r_mail = rem_mail.replace("@telegram.org","")
			current_mail = pickledb.load("mails/"+r_mail+".json", False)
			current_id = current_mail.get("id")
			if current_id == message.from_user.id:
				os.remove("mails/"+r_mail+".json")
				os.remove("users/"+str(message.from_user.id)+".json")
				await message.answer("Данные успешно сброшены!")
			else:
				await message.answer("Это не ваша почта!")
		else:
			await message.answer("Неккоректная почта! Введите почту по форме:\nваша почта@telegram.org")
	else:
		await message.answer("Упс! А у вас похоже нет почты!\nЧтобы создать пропишите /register")

@dp.message_handler(commands=["info"])
async def user_information(message: types.Message):
	if isFile("users/"+str(message.from_user.id)+".json"):
		usr_db = pickledb.load("users/"+str(message.from_user.id)+".json", False)
		usr_mail = usr_db.get("mail")
		if usr_db.get("full") == 1:
			usr_full = "Есть"
			await message.answer(
				f"Вот информация о вас:\n*Имя пользователя:* `{message.from_user.username}`\n*ID:* `{message.from_user.id}`\n*Ваша почта:* `{usr_mail}`\nПолный доступ: *{usr_full}*",
				parse_mode="markdown")
		else:
			usr_full = "Нет"
			await message.answer(
				f"Вот информация о вас:\n*Имя пользователя:* `{message.from_user.username}`\n*ID:* `{message.from_user.id}`\n*Ваша почта:* `{usr_mail}`\nПолный доступ: *{usr_full}*",
				parse_mode="markdown", reply_markup=kb.info_markup)
	else:
		await message.answer("Простите, но вы не зарегистрированны!\nЧтобы это сделать - напишите /register")

@dp.message_handler(commands=["send"])
async def send_mail_from_user(message: types.Message):
	if isFile("users/"+str(message.from_user.id)+".json"):
		try:
			write_to = message.get_args() #recipient mail. Example: user@telegram.org
			if "@telegram.org" in write_to:
				check_db = pickledb.load("users/"+str(message.from_user.id)+".json", False)
				user_full = check_db.get('full')
				await message.delete()
				if user_full == 1:
					await message.answer(f"Проводится обработка.\nВведёный адрес: `{write_to}`\nУ вас есть *полный доступ*, а значит задержка минимальна", parse_mode="markdown")
					config.recipient_mail = write_to.replace("@telegram.org", "")
					await asyncio.sleep(0.1)
				else:
					await message.answer(
						f"Проводится обработка.\nВведёный адрес: `{write_to}`\n*Внимание:* Так как у вас нет полного доступа, будет задержка.",
						parse_mode="markdown")
					config.recipient_mail = write_to.replace("@telegram.org", "")
					await asyncio.sleep(1.9)
				if isFile("mails/"+config.recipient_mail+".json"):
					await message.answer("Почтовый адрес найден\nНапишите сообщение которое хотите ему отправить.")
					config.is_mailing = True
				else:
					await message.answer("Пользователь не найден, попробуйте ещё раз.")
			else:
				await message.delete()
				await message.answer("Неккоретный адрес!\nВведите ещё раз.")
				config.is_mailing = False

		except:
			await message.answer("Произошла неизвестная ошибка! Попробуйте ещё раз!")

	else:
		await message.answer("Извините, но вы не зарегистрировали вашу почту.\nЧтобы это сделать - пропишите /register")

@dp.message_handler(commands=["mails"])
async def read_all_mails(message: types.Message):
	usr_base = pickledb.load("users/"+str(message.from_user.id)+".json", False)
	if usr_base.get("full") == 1:
		await message.answer("Обрабатывается запрос...")
		mails = listdir("mails")
		all_mails = ""
		for i in range(len(mails)):
			all_mails = all_mails + "`" + mails[i] + "@telegram.org`\n"
		all_mails = all_mails.replace(".json", "")
		await message.answer(f"Вот текущий список зарегестрированных почт:\n{all_mails}", parse_mode="markdown")
	else:
		await message.answer("Извините! Но вы не можете это использовать!\nЧтобы увидеть список, приобретите полный доступ.\n/full")

@dp.message_handler(commands=["full"])
async def full_sub_invoice(message: types.Message):
	if isFile("users/"+str(message.from_user.id)+".json"):
		usr_db = pickledb.load("users/" + str(message.from_user.id) + ".json", False)
		if usr_db.get("full") == 1:
			await message.answer("У вас уже есть полный доступ!\nНовая покупка уже имеющегося товара - лишняя трата денег!")
		else:
			await message.answer("Выберите один способ для оплаты:", reply_markup=kb.pay_full)
	else:
		await message.answer("Для начала зарегистрируйтесь!\n/register")

@dp.pre_checkout_query_handler()
async def process_precheckout(pre_checkout: types.PreCheckoutQuery):
	await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
	if message.successful_payment.invoice_payload == "sub_full":
		user_pay = pickledb.load("users/"+str(message.from_user.id)+".json", False)
		user_pay.set("full", 1)
		user_pay.dump()
		await message.answer("Полный доступ успешно активирован!\nТеперь вам будут доступны новые комманды, посмотреть которые вы можете в списке комманд бота")
		

@dp.message_handler()
async def mail_handler(message: types.Message):
	if config.registration:
		config.registration = False
		if "@" in message.text:
			await message.answer("Неккоректная почта! Попробуйте другую")
			config.registration = True
		try:
			f = open("mails/"+message.text+".json", "r")
			f.close()
			await message.answer("Простите, но такая почта уже зарегистрированна!\nПридумайте новую.")
			config.registration = True
		except:
			user_mail = message.text+"@telegram.org"
			user_file = pickledb.load("mails/"+message.text+".json", False)
			user_file.set("username", message.from_user.username)
			user_file.set("id", message.from_user.id)
			user_file.set("mail", user_mail)
			user_file.dump()
			new_user = pickledb.load("users/"+str(message.from_user.id)+".json", False)
			new_user.set("username", message.from_user.username)
			new_user.set("id", message.from_user.id)
			new_user.set("mail", user_mail)
			new_user.set("full", 0)
			new_user.dump()
			await message.answer("Поздравляем! Вы зарегистрировали почту:\nПользователь: {}\nID: `{}`\nПочта: {}".format(message.from_user.username, message.from_user.id, user_mail),parse_mode="markdown")

	if config.is_mailing:
		config.is_mailing = False
		mail_text = message.text
		usr = pickledb.load("mails/"+config.recipient_mail+".json",False)
		usr_id = usr.get("id")
		m_usr = pickledb.load("users/"+str(message.from_user.id)+".json", False)
		m_usr_ml = m_usr.get("mail")
		m_usr_mail = m_usr_ml.replace("@telegram.org", "")
		usr_mail = config.recipient_mail + "@telegram.org"
		await bot.send_message(usr_id, f"Сообщение от *{m_usr_mail}*\nОтправитель: `*{m_usr_ml}*`\nТекст:\n*{mail_text}*", parse_mode="markdown")
		await bot.send_message(config.admin_id, f"Сообщение от *{m_usr_mail}*\nОтправитель: `*{m_usr_ml} | {message.from_user.id}*`\nПолучатель: ` *{usr_mail} | {usr_id}*`\nТекст:\n*{mail_text}*", parse_mode="markdown")
		await message.answer("Сообщение успешно доставлено.")

#CallBack Handlers
@dp.callback_query_handler(text="reg_success")
async def success_registration_query(query: types.CallbackQuery):
	await bot.edit_message_text("Отлично! Вы успешно согласились и можете продолжать регистрацию.\nВведите имя пользователя для почты, оно не должно содержать символов и должно быть на английском.\nПримечани: будет добавлено '@telegram.org'", query.from_user.id, query.message.message_id, query.id, parse_mode="markdown")
	config.registration = True

@dp.callback_query_handler(text="info_full")
async def information_buy_full_query(query: types.CallbackQuery):
	await bot.edit_message_text("Выберите один способ для оплаты:", query.from_user.id, query.message.message_id, query.id, reply_markup=kb.pay_full)

@dp.callback_query_handler(text="yookassa")
async def yookassa_payment_full(query: types.CallbackQuery):
	await bot.delete_message(query.from_user.id, query.message.message_id)
	await bot.send_message(query.from_user.id, "Вот ваш счёт для оплаты [ЮКасса]:")
	await bot.send_invoice(chat_id=query.from_user.id, title="Полный доступ",
						   description="Полный доступ к боту Telegram Mail", payload="sub_full",
						   provider_token=config.YOUTOKEN, currency="RUB", start_parameter="full_payment",
						   prices=[{"label": "РУБ", "amount": 12000}])

@dp.callback_query_handler(text="sberbank")
async def sberbank_payment_full(query: types.CallbackQuery):
	await bot.delete_message(query.from_user.id, query.message.message_id)
	await bot.send_message(query.from_user.id, "Вот ваш счёт для оплаты [СберБанк]:")
	await bot.send_invoice(chat_id=query.from_user.id, title="Полный доступ",
						   description="Полный доступ к боту Telegram Mail", payload="sub_full",
						   provider_token=config.SBERTOKEN, currency="RUB", start_parameter="full_payment",
						   prices=[{"label": "РУБ", "amount": 12000}])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)