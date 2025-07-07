import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Your custom writing prompt
writing_style_prompt = """
From the perspective of a real human who has lived through it.
Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language.
Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing.
Avoid sounding robotic or overly polished—make it feel raw, passionate, and real.
Don't follow a rigid structure. Prioritize authenticity and relatability.
"""

async def generate_blog(topic):
    response = model.generate_content(f"{writing_style_prompt}\n\nWrite a blog about: {topic}")
    return response.text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text("✍️ Generating blog content...")
    try:
        blog = await generate_blog(topic)
        await update.message.reply_text(blog)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error generating blog: {e}")

def main():
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
