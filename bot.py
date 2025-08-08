import os
import threading
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# TOKEN: first try environment variable (safer on Render), otherwise fall back to the embedded token you provided
TOKEN = os.getenv("TOKEN", "7997104197:AAFAI8wkZsIUkfvoVKgSd4XDZdkqNZg26hk")

if not TOKEN:
    print("❌ Ошибка: Токен не найден. Установи переменную окружения TOKEN")
    raise SystemExit(1)

# --- Simple Flask web server so Render/Uptime pings can keep the service responsive ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is alive!"

def run_web():
    port = int(os.getenv("PORT", 8080))
    # Flask's built-in server is used for simplicity
    app_web.run(host='0.0.0.0', port=port)

# --- Telegram bot handlers ---
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
    # new_chat_members may not exist in some updates; guard it
    members = getattr(update.message, 'new_chat_members', []) if update.message else []
    for member in members:
        name = member.full_name or member.username or "друг"
        # Prefer mention by username if available
        mention = f"@{member.username}" if getattr(member, 'username', None) else name
        await update.message.reply_text(f'Привет, {mention}! Добро пожаловать в мой личный блог 🎶')

async def main():
    # Start Flask in a background thread so the web endpoint is available for pings
    threading.Thread(target=run_web, daemon=True).start()

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("музыка", music))
    app.add_handler(CommandHandler("видео", video))
    app.add_handler(CommandHandler("предложить", suggest))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот работает... (Telegram polling started)")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Завершение работы")    
