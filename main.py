import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Токен вашего бота
API_TOKEN = '8908913545:AAFqVtBWMZNTrJQKGJxDPyi3wsSHC9iv77Y'

# URL вашего приложения на Render (строго с https:// и без слеша на конце)
BASE_URL = 'https://im-bot-je1b.onrender.com'
WEBHOOK_PATH = f'/webhook/{API_TOKEN}'
WEBHOOK_URL = f'{BASE_URL}{WEBHOOK_PATH}'

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- Ваши хендлеры ---

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    welcome_text = (
        "Здравствуй мой друг, ты попал в крипто бота основного на компании @send, "
        "данная компания полностью дала разрешение и подтвердила что данный бот "
        "не нарушает правил платформы телеграмма, а также не занимается мошенической схемой."
    )
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="🚀 Запустить приложение", 
            web_app=WebAppInfo(url=BASE_URL)
        )
    )
    await message.reply(welcome_text, reply_markup=keyboard)


# --- Системная логика вебхука и веб-сервера ---

async def on_startup(app):
    # Регистрируем вебхук в Telegram при старте
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    # Удаляем вебхук при остановке приложения
    await bot.delete_webhook()
    await bot.close()

async def handle_webhook(request):
    # Принимаем апдейты от Telegram
    url = request.url
    text = await request.text()
    if text:
        update = types.Update.loads(text)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(update)
    return web.Response()

async def handle_root(request):
    # Если кто-то заходит по главной ссылке, отдаем HTML интерфейс кошелька
    # Файл index.html должен лежать в той же папке на GitHub
    if os.path.exists('index.html'):
        return web.FileResponse('index.html')
    return web.Response(text="Сайт кошелька работает, но файл index.html не найден.")

# Инициализация веб-сервера aiohttp
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Маршруты сервера
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.router.add_get('/', handle_root)
# Если у вас есть папка со стилями/картинками (например, static), раскомментируйте строку ниже:
# app.router.add_static('/static/', path='static', name='static')

if __name__ == '__main__':
    # Render передает порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host='0.0.0.0', port=port)

