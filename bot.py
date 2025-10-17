import os
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ========== FLASK ДЛЯ ПИНГА ==========
app = Flask('')

@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>🤖 Simple Telegram Bot</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255,255,255,0.1);
                    padding: 30px;
                    border-radius: 15px;
                    backdrop-filter: blur(10px);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Бот работает!</h1>
                <p>Статус: <strong>Активен</strong> ✅</p>
                <p>Простой Telegram бот на Python</p>
                <p>💡 Напиши /start в Telegram</p>
            </div>
        </body>
    </html>
    """

@app.route('/ping')
def ping():
    return "pong"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# ========== TELEGRAM БОТ ==========
TOKEN = os.environ.get('8409817458:AAFJrILIJDimP7rroXysLly9MYV6sMGo5Uo')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.message.from_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n"
        f"Я самый простой бот!\n"
        f"Напиши мне что-нибудь 😊"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "📝 Доступные команды:\n"
        "/start - Начать общение\n"
        "/help - Помощь\n"
        "/info - Информация о боте\n\n"
        "Или просто напиши мне сообщение!"
    )

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /info"""
    await update.message.reply_text(
        "🤖 Простой Telegram бот\n"
        "🔧 Создан на Python\n"
        "📚 Использует python-telegram-bot\n"
        "🌐 Работает 24/7 с Flask пингом\n"
        "🚀 Запущен на Replit"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на любое текстовое сообщение"""
    user_text = update.message.text
    await update.message.reply_text(
        f"Ты написал: '{user_text}'\n"
        f"Попробуй команду /help 😉"
    )

def main():
    """Основная функция запуска бота"""
    # Запускаем Flask сервер для пинга
    keep_alive()
    print("🌐 Flask сервер запущен на порту 8080")
    
    if not TOKEN:
        print("❌ Ошибка: TELEGRAM_TOKEN не найден!")
        print("💡 Добавь TELEGRAM_TOKEN в Secrets (Replit)")
        return
    
    # Создаем приложение Telegram
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    print("🤖 Telegram бот запускается...")
    application.run_polling()

if __name__ == "__main__":
    main()