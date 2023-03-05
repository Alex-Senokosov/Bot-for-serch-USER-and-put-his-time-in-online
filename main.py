import telebot

# Создание объекта бота с токеном
bot = telebot.TeleBot('6260578840:AAF8IvgYmk2fMYBt3wHBC3Zzg_0v-XLiSKg')


# Обработчик команды старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Введите имя пользователя или номер телефона для поиска")


# Обработчик входящих сообщений с именем пользователя или номером телефона для поиска
@bot.message_handler(func=lambda message: True)
def search_users(message):
    search_query = message.text
    try:
        # Поиск пользователя по имени пользователя или номеру телефона
        if search_query.startswith("+"):
            user_info = bot.get_chat(search_query)
        else:
            user_info = bot.get_chat("@" + search_query)

        if user_info.type == "private":
            # Получаем фотографию профиля пользователя
            photos = bot.get_user_profile_photos(user_info.id)
            if photos.total_count > 0:
                # Получаем время последнего изменения фотографии
                last_photo_time = photos.photos[0][-1].date
                bot.reply_to(message, f"Пользователь {user_info.first_name} был в онлайн в {last_photo_time}")
            else:
                bot.reply_to(message, f"Пользователь {user_info.first_name} не был в онлайн")
        else:
            bot.reply_to(message, f"Пользователь {user_info.title} в онлайн")

    except telebot.apihelper.ApiException as e:
        if "Chat not found" in str(e):
            bot.reply_to(message, "Не удалось найти пользователя")
        else:
            bot.reply_to(message, f"Ошибка: {e}")


# Запуск бота
bot.polling()
