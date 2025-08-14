# main.py  (Railway-ready, no Flask, no UptimeRobot)
import os
from datetime import time as dt_time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ Укажите BOT_TOKEN в Railway → Variables")

# ---------- /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not user:
        return
    kb = [[InlineKeyboardButton("🧘‍♂️ Медитация", callback_data="meditation")]]
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы получить медитацию:",
        reply_markup=InlineKeyboardMarkup(kb))

# ---------- callback ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from_user = query.from_user
    if not from_user:
        return
    try:
        with open("my_meditation.mp3", "rb") as f:
            await context.bot.send_voice(
                chat_id=from_user.id,
                voice=f,
                caption="🎧 Приятной медитации!")
    except FileNotFoundError:
        await context.bot.send_message(
            chat_id=from_user.id,
            text="🎙️ Аудиофайл медитации не найден.")

# ---------- main ----------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 Bot polling...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
