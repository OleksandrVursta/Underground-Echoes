import telebot
import os
from dotenv import load_dotenv
from services.openai_service import get_recommendations
from utils.validators import validate_music_request

load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")

if not token:
    print("❌ ПОМИЛКА: TELEGRAM_TOKEN не знайдено в .env")
    exit()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "🤘 **Привіт у Underground Echoes!**\n\n"
        "Напиши мені назву гурту, який тобі подобається, "
        "а я підберу для тебе 5 схожих нішевих проектів зі Spotify."
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    is_valid, error = validate_music_request(message.text)
    if not is_valid:
        bot.reply_to(message, error)
        return

    bot.send_chat_action(message.chat.id, 'typing')
    
    print(f"DEBUG: Запит від юзера: {message.text}")
    
    try:
        result = get_recommendations(message.text)
        bot.reply_to(message, result, parse_mode='Markdown')
    except Exception as e:
        print(f"❌ ПОМИЛКА в bot.py: {e}")
        bot.send_message(message.chat.id, "⚠️ Сталася помилка при підборі музики. Спробуй пізніше.")

if __name__ == "__main__":
    print("✅ Бот запущений у спрощеному режимі... Натисніть Ctrl+C для зупинки.")
    bot.polling(none_stop=True)