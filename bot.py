from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import time
import random

TOKEN = os.getenv("BOT_TOKEN")

ADMINS = [5543310890]

def is_admin(user_id):
    return user_id in ADMINS

konten = {}
jobs = {}
last_work = {}

START_GELD = 1000
COOLDOWN = 4 * 60 * 60

JOB_GEHÄLTER = {
    "polizist": 3000,
    "boss": 10000,
    "krankenpfleger": 2500
}

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in konten:
        konten[user] = START_GELD

    if user not in jobs:
        jobs[user] = "Arbeitslos"

    await update.message.reply_text(
        "🏙️ Willkommen im Real-Life RP Server!\n\n"
        "💼 JOBS:\n"
        "• /getjob_polizist (3000€)\n"
        "• /getjob_boss (10000€)\n"
        "• /getjob_krankenpfleger (2500€)\n\n"
        "💰 ECONOMY:\n"
        "• /konto - dein Geld & Job\n"
        "• /arbeiten - Geld verdienen (alle 4h)\n\n"
        "🛡️ ADMIN:\n"
        "• /cheatmoney (nur Admin)\n\n"
        "Starte jetzt dein Leben im RP!"
    )

# ---------------- KONTO ----------------
async def konto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if user not in konten:
        konten[user] = START_GELD

    job = jobs.get(user, "Arbeitslos")

    await update.message.reply_text(
        f"💳 Konto: {konten[user]} €\n"
        f"💼 Job: {job}"
    )

# ---------------- JOBS ----------------
async def set_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    cmd = update.message.text.lower()

    if user not in konten:
        konten[user] = START_GELD

    if "polizist" in cmd:
        jobs[user] = "Polizist"
        salary = JOB_GEHÄLTER["polizist"]

    elif "boss" in cmd:
        jobs[user] = "Boss"
        salary = JOB_GEHÄLTER["boss"]

    elif "krankenpfleger" in cmd:
        jobs[user] = "Krankenpfleger"
        salary = JOB_GEHÄLTER["krankenpfleger"]

    else:
        await update.message.reply_text("❌ Job nicht gefunden.")
        return

    await update.message.reply_text(
        f"✅ Du hast den Job bekommen: {jobs[user]}\n"
        f"💰 Gehalt: {salary} €"
    )

# ---------------- ARBEITEN ----------------
async def arbeiten(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    now = time.time()

    if user not in konten:
        konten[user] = START_GELD

    if user not in jobs:
        await update.message.reply_text("❌ Du hast keinen Job!")
        return

    if user in last_work:
        diff = now - last_work[user]
        if diff < COOLDOWN:
            rest = int((COOLDOWN - diff) / 60)
            await update.message.reply_text(
                f"⏳ Warte noch {rest} Minuten."
            )
            return

    job = jobs[user]
    geld = JOB_GEHÄLTER[job.lower()]

    konten[user] += geld
    last_work[user] = now

    await update.message.reply_text(
        f"💼 Du hast als {job} gearbeitet\n"
        f"💰 +{geld} € erhalten!"
    )
    
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Deine ID: {update.effective_user.id}")

async def cheatmoney(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    if not is_admin(user):
        await update.message.reply_text("❌ Kein Zugriff.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Nutze: /cheatmoney user_id betrag")
        return

    target_id = int(context.args[0])
    amount = int(context.args[1])

    if target_id not in konten:
        konten[target_id] = START_GELD

    konten[target_id] += amount

    await update.message.reply_text(
        f"💰 {amount} € wurden an User {target_id} gegeben."
    )

# ---------------- BOT ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("konto", konto))
app.add_handler(CommandHandler("arbeiten", arbeiten))

app.add_handler(CommandHandler("getjob_polizist", set_job))
app.add_handler(CommandHandler("getjob_boss", set_job))
app.add_handler(CommandHandler("getjob_krankenpfleger", set_job))
app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("cheatmoney", cheatmoney))

print("Bot läuft...")
app.run_polling()
print("Bot läuft...")
app.run_polling()
