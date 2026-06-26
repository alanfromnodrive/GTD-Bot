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
    await update.message.reply_text("Mándame una idea")
    return IDEA

async def handle_idea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['idea'] = update.message.text
    await update.message.reply_text("¿Área? OMG / SCR / DPM / NDS / OTH / PERSONAL")
    return AREA

async def handle_area(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    area = update.message.text.upper().strip()
    if area not in ["OMG", "SCR", "DPM", "NDS", "OTH", "PERSONAL"]:
        await update.message.reply_text("Área no válida")
        return AREA
    context.user_data['area'] = area
    await update.message.reply_text("¿Estado? INBOX / PROJECTS / NEXT ACTIONS / WAITING FOR / SOMEDAY/MAYBE / DONE")
    return ESTADO

async def handle_estado(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    estado = update.message.text.upper().strip()
    if estado not in ["INBOX", "PROJECTS", "NEXT ACTIONS", "WAITING FOR", "SOMEDAY/MAYBE", "DONE"]:
        await update.message.reply_text("Estado no válido")
        return ESTADO
    idea = context.user_data['idea']
    area = context.user_data['area']
    add_to_notion(idea, area, estado)
    await update.message.reply_text(f"✅ Agregada a {area}")
    return ConversationHandler.END

def add_to_notion(title, area, estado):
    url = "https://api.notion.com/v1/pages"
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Área": {"select": {"name": area}},
            "Estado": {"select": {"name": estado}},
            "Descripción": {"rich_text": [{"text": {"content": "Telegram"}}]}
        }
    }
    requests.post(url, headers=NOTION_HEADERS, json=payload)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            IDEA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_idea)],
            AREA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_area)],
            ESTADO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_estado)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == '__main__':
    main()
