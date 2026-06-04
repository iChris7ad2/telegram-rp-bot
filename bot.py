from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

konten = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in konten:
        konten[user] = 1000

    await update.message.reply_text(
        "🏙️ Willkommen im RP!\n"
        "Du hast 1000 € Startgeld bekommen.\n"
        "Schreibe /konto"
    )

async def konto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in konten:
        konten[user] = 1000

    await update.message.reply_text(
        f"💳 Dein Kontostand: {konten[user]} €"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("konto", konto))

print("Bot läuft...")
app.run_polling()
