import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json

TELEGRAM_TOKEN = "8826930371:AAGlN3toSH3ycoHPw4SBgQNb00NURlMtrGI"
NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "e7b3439cbc4b4bad8a1e96c060574f57"

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("¡Hola! Soy tu bot GTD.\nMandame una idea y te pediré el área.\nÁreas: OMG, SCR, DPM, NDS, OTH, PERSONAL")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    idea = update.message.text
    context.user_data['current_idea'] = idea
    await update.message.reply_text(f"Idea: {idea}\n\n¿Cuál es el área?\nOMG / SCR / DPM / NDS / OTH / PERSONAL")

async def handle_area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    area = update.message.text.upper().strip()
    areas = ["OMG", "SCR", "DPM", "NDS", "OTH", "PERSONAL"]
    
    if area not in areas:
        await update.message.reply_text("Área no válida. Intenta de nuevo.")
        return
    
    idea = context.user_data.get('current_idea', '')
    add_to_notion(idea, area)
    await update.message.reply_text(f"✅ Idea agregada a {area}")

def add_to_notion(title: str, area: str):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Área": {"select": {"name": area}},
            "Estado": {"select": {"name": "INBOX"}},
            "Descripción": {"rich_text": [{"text": {"content": "Capturada desde Telegram"}}]}
        }
    }
    try:
        requests.post(url, headers=NOTION_HEADERS, json=payload)
    except:
        pass

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
