import re
import requests
import telebot
from config import settings

bot  = telebot.TeleBot(settings.BOT_API_TOKEN)

ALLOWED_USERS = [int(user_id.strip()) for user_id in settings.ALLOWED_USERS.split(',') if user_id.strip()]

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """
    Привет, я Gym Assistant bot 🏋️
    Я помогу привести программу тренировок к единому формату 💪
    """)

@bot.message_handler()
def get_message(message):
    try:
        if message.from_user.id not in ALLOWED_USERS:
            bot.send_message(message.chat.id, "❌ Вы не авторизованы")
            return

        # Проверка типа сообщения (только текст)
        if message.content_type != 'text':
            bot.send_message(message.chat.id, "❌ Пожалуйста, отправьте текстовое сообщение!")
            return

        user_text = message.text

        # Проверка длины текста
        if len(user_text) < 5:
            bot.send_message(message.chat.id, "❌ Текст слишком короткий! Минимум 5 символов.")
            return

        if len(user_text) > 2000:
            bot.send_message(message.chat.id, "❌ Текст слишком длинный! Максимум 1000 символов.")
            return

        # Проверка на пустое сообщение
        if not user_text.strip():
            bot.send_message(message.chat.id, "❌ Сообщение не может быть пустым!")
            return

        # Дополнительные проверки
        if user_text.startswith('/'):
            bot.send_message(message.chat.id, "❌ Сообщение не может начинаться с команды!")
            return

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['text'] = user_text


        bot.delete_state(message.from_user.id, message.chat.id)
        response = send_message_to_api(user_text)
        for workout in response:
            bot.send_message(message.chat.id, f'```\n{workout}\n```', parse_mode="Markdown")

    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка при обработке сообщения")

def send_message_to_api(message):
    url = f'http://{settings.BACKEND_URL}:8000/new-message/'
    data = {"text": f"{message}"}

    response = requests.post(url, json=data)

    response_data = response.json()
    result_text = response_data['message_formatted']
    split_result = split_workouts(result_text)
    return split_result


def split_workouts(text):
    """
    Разделяет текст на части по началу каждой тренировки (### ТРЕНИРОВКА)

    Args:
        text (str): Исходный текст с тренировками

    Returns:
        list: Список частей текста (каждая тренировка отдельно)
    """

    # Используем регулярное выражение для поиска всех начал тренировок
    pattern = r'(### .*ТРЕНИРОВКА \d+)'

    # Находим все позиции начала тренировок
    matches = list(re.finditer(pattern, text))

    if not matches:
        # Если не найдено ни одной тренировки, возвращаем весь текст как одну часть
        return [text]

    # Собираем части текста
    parts = []

    # Первая часть - от начала до первой тренировки
    first_match = matches[0]
    if first_match.start() > 0:
        parts.append(text[:first_match.start()].strip())

    # Добавляем все тренировки
    for i in range(len(matches)):
        start_pos = matches[i].start()
        if i < len(matches) - 1:
            end_pos = matches[i + 1].start()
            parts.append(text[start_pos:end_pos].strip())
        else:
            # Последняя тренировка - до конца текста
            parts.append(text[start_pos:].strip())

    return parts

# Запуск бота
if __name__ == "__main__":
    print("Bot started...")
    bot.infinity_polling()
