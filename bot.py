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
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    is_valid, error = validate_music_request(message.text)
    if not is_valid:
        bot.reply_to(message, error)
        return

    # 1. МИТТЄВА ВІДПОВІДЬ (щоб юзер не чекав 4 хвилини в тиші)
    processing_msg = bot.reply_to(
        message, 
        "⏳ **Занурююсь у глибокий андеграунд...**\nПошук рідкісних гуртів може зайняти до хвилини, зачекайте трохи.", 
        parse_mode='Markdown'
    )
    
    # Показуємо статус "друкує" в заголовку чату
    bot.send_chat_action(message.chat.id, 'typing')
    
    print(f"DEBUG: Запит від юзера: {message.text}")
    
    try:
        # 2. ОСНОВНА ЛОГІКА (ШІ + Spotify)
        result = get_recommendations(message.text)
        
        # 3. ВИДАЛЯЄМО СТАТУС ОЧІКУВАННЯ
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
        # 4. ВІДПРАВЛЯЄМО РЕЗУЛЬТАТ
        bot.reply_to(message, result, parse_mode='Markdown')
        
    except Exception as e:
        print(f"❌ ПОМИЛКА: {e}")
        # Видаляємо "пісочний годинник", якщо сталася помилка
        try:
            bot.delete_message(message.chat.id, processing_msg.message_id)
        except:
            pass
        bot.send_message(message.chat.id, "🌚 Андеграунд виявився занадто глибоким. Спробуй інший гурт або повтори пізніше.")

if __name__ == "__main__":
    print("✅ Бот запущений у спрощеному режимі... Натисніть Ctrl+C для зупинки.")
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)