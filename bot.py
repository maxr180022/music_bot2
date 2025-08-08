import os
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Читаем токен из переменной окружения BOT_TOKEN
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("❌ Ошибка: Токен не найден. Установи переменную окружения BOT_TOKEN")
    raise SystemExit(1)

# --- Flask веб-сервер (для Render пингов) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.getenv("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- Хендлеры Telegram ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🎵 Музыка", "📺 Видео"], ["💬 Предложить идею"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я бот для музыкантов 🎸", reply_markup=reply_markup)

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Последние треки:\n1. https://example.com/track1\n2. https://example.com/track2")

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📺 YouTube подборка:\n1. https://youtu.be/example1\n2. https://youtu.be/example2")

async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 Напиши свою идею — я передам её админу!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower() if update.message and update.message.text else ""
    if "музыка" in text:
        await music(update, context)
    elif "видео" in text:
        await video(update, context)
    elif "предлож" in text:
        await suggest(update, context)
    else:
        await update.message.reply_text("Не понял. Нажми кнопку или введи команду.")

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    members = getattr(update.message, 'new_chat_members', []) if update.message else []
    for member in members:
        name = member.full_name or member.username or "друг"
        mention = f"@{member.username}" if getattr(member, 'username', None) else name
        await update.message.reply_text(f'Привет, {mention}! Добро пожаловать в мой личный блог 🎶')

async def main():
    threading.Thread(target=run_web, daemon=True).start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("музыка", music))
    app.add_handler(CommandHandler("видео", video))
    app.add_handler(CommandHandler("предложить", suggest))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Бот запущен!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("⛔ Завершение работы")
