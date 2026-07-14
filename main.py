import os
import telebot
from flask import Flask, request

# Токен вашего бота (полученный у @BotFather)
API_TOKEN = 'ВАШ_ТОКЕН_БОТА'

# URL вашего приложения на Render (строго с https://)
BASE_URL = 'https://onrender.com'
WEBHOOK_URL = f'{BASE_URL}/webhook/'

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Здравствуй мой друг, ты попал в крипто бота основного на компании @send, "
        "данная компания полностью дала разрешение и подтвердила что данный бот "
        "не нарушает правил платформы телеграмма, а также не занимается мошенической схемой."
    )
    
    # Кнопка для открытия Web App кошелька
    keyboard = telebot.types.InlineKeyboardMarkup()
    web_app_info = telebot.types.WebAppInfo(url=BASE_URL)
    button = telebot.types.InlineKeyboardButton(text="🚀 Запустить приложение", web_app=web_app_info)
    keyboard.add(button)
    
    bot.reply_to(message, welcome_text, reply_markup=keyboard)

# Системные маршруты для работы вебхука и отображения сайта
@app.route('/webhook/', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Forbidden', 403

@app.route('/')
def index():
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    return "Сайт работает, но index.html не найден."

@app.route('/script.js')
def static_js():
    if os.path.exists('script.js'):
        with open('script.js', 'r', encoding='utf-8') as f:
            return f.read()
    return ""

@app.route('/style.css')
def static_css():
    if os.path.exists('style.css'):
        with open('style.css', 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# Переустановка вебхука при перезапуске сервера
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
