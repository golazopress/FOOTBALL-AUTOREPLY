import os
from dotenv import load_dotenv
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

load_dotenv()
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Your custom writing prompt
WRITING_PROMPT = """
From the perspective of a real human who has lived through it.
Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language.
Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing.
Avoid sounding robotic or overly polished—make it feel raw, passionate, and real.
Don't follow a rigid structure. Prioritize authenticity and relatability.
"""

# Handles /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚽ Send me a football topic and I'll write a blog for you.")

# Handles incoming messages (topics)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    full_prompt = f"Write a passionate, human-sounding football blog on this topic:\n\n{topic}\n\n{WRITING_PROMPT}"

    try:
        response = model.generate_content(full_prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error generating blog: {e}")

# Main app
def main():
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
