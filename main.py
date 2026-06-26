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

IDEA, AREA = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("¡Hola! Mándame una idea para tu GTD.")
    return IDEA

async def handle_idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['idea'] = update.message.text
    await update.message.reply_text(f"Idea: {update.message.text}\n\n¿Cuál es el área?\nOMG / SCR / DPM / NDS / OTH / PERSONAL")
    return AREA

async def handle_area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    area = update.message.text.upper().strip()
    areas = ["OMG", "SCR", "DPM", "NDS", "OTH", "PERSONAL"]
    
    if area not in areas:
        await update.message.reply_text("Área no válida. Intenta: OMG / SCR / DPM / NDS / OTH / PERSONAL")
        return AREA
    
    idea = context.user_data.get('idea', '')
    add_to_notion(idea, area)
    await update.message.reply_text(f"✅ Idea agregada a {area}")
    return ConversationHandler.END

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
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            IDEA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea)],
            AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_area)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
