import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

# Load your Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Your custom blog prompt
BLOG_PROMPT = """
From the perspective of a real human who has lived through it.
Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language.
Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing.
Avoid sounding robotic or overly polished—make it feel raw, passionate, and real.
Don't follow a rigid structure. Prioritize authenticity and relatability.
"""

# Function to generate blog content
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text(f"✍️ Generating blog for:\n\n{topic}")
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(BLOG_PROMPT + "\n\nTopic: " + topic)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating blog:\n{e}")

# Start the bot
def main():
    telegram_token = os.getenv("TELEGRAM_REPLY_BOT_TOKEN")

    if not telegram_token:
        raise Exception("TELEGRAM_REPLY_BOT_TOKEN is not set in the environment")

    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Auto-reply bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
