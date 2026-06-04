from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import time
import random

TOKEN = os.getenv("BOT_TOKEN")

konten = {}
last_work = {}

START_GELD = 1000
COOLDOWN = 4 * 60 * 60  # 4 Stunden in Sekunden

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in konten:
        konten[user] = START_GELD

    await update.message.reply_text(
        "🏙️ Willkommen im RP!\n"
        "Du hast 1000 € Startgeld.\n"
        "Commands:\n"
        "/konto\n"
        "/arbeiten"
    )

async def konto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in konten:
        konten[user] = START_GELD

    await update.message.reply_text(
        f"💳 Dein Kontostand: {konten[user]} €"
    )

async def arbeiten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    now = time.time()

    if user not in konten:
        konten[user] = START_GELD

    if user in last_work:
        diff = now - last_work[user]

        if diff < COOLDOWN:
            rest = int((COOLDOWN - diff) / 60)
            await update.message.reply_text(
                f"⏳ Du bist müde.\n"
                f"Bitte warte noch {rest} Minuten."
            )
            return

    geld = random.randint(100, 400)
    konten[user] += geld
    last_work[user] = now

    await update.message.reply_text(
        f"💼 Du hast gearbeitet und {geld} € verdient!"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("konto", konto))
app.add_handler(CommandHandler("arbeiten", arbeiten))

print("Bot läuft...")
app.run_polling()
