import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import requests

TELEGRAM_TOKEN = "8826930371:AAGlN3toSH3ycoHPw4SBgQNb00NURlMtrGI"
NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "e7b3439cbc4b4bad8a1e96c060574f57"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

IDEA, AREA, ESTADO = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("¡Hola! Mándame una idea para tu GTD.")
    return IDEA

async def handle_idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['idea'] = update.message.text
    await update.message.reply_text(f"Idea: {update.message.text}\n\n¿Cuál es el área?\nOMG / SCR / DPM / NDS / OTH / PERSONAL")
    return AREA

async def
