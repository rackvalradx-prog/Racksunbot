import telebot
import time
from telebot import types
from flask import Flask
from threading import Thread

# --- 1. Flask Server (For 24/7 Uptime) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- 2. BOT CODE ---
API_TOKEN = '8055993364:AAGHrnI7blSeidOXnQXmLqPoMKuZFkX7QJE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_cmd(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # 👤 User Button
    btn_user = types.KeyboardButton(
        text="👤 User",
        request_users=types.KeyboardButtonRequestUsers(request_id=1, max_quantity=1)
    )
    # 👥 Group Button
    btn_group = types.KeyboardButton(
        text="👥 Group",
        request_chat=types.KeyboardButtonRequestChat(request_id=2, chat_is_channel=False)
    )
    # 📢 Channel Button
    btn_channel = types.KeyboardButton(
        text="📢 Channel",
        request_chat=types.KeyboardButtonRequestChat(request_id=3, chat_is_channel=True)
    )
    
    markup.add(btn_user, btn_group, btn_channel)
    
    # English Message
    welcome_msg = (
        f"**Welcome To @racksunbot** 🖐️\n\n"
        f"**Your ID :** `{message.from_user.id}`\n\n"
        f"Please select an option from the menu below:"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_msg,
        reply_markup=markup,
        parse_mode="Markdown"
    )

# --- ID HANDLERS ---
@bot.message_handler(content_types=['users_shared'])
def handle_users(message):
    for user in message.users_shared.users:
        bot.send_message(message.chat.id, f"👤 **User ID:** `{user.user_id}`", parse_mode="Markdown")

@bot.message_handler(content_types=['chat_shared'])
def handle_chats(message):
    bot.send_message(message.chat.id, f"🆔 **Chat ID:** `{message.chat_shared.chat_id}`", parse_mode="Markdown")

# --- 3. START BOT ---
if __name__ == "__main__":
    try:
        keep_alive()
        print("✅ Server Started!")
        print("✅ Bot is Online!")
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ Error: {e}")
        time.sleep(5)
