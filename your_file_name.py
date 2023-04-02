import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a function to generate a response using OpenAI's GPT API
def generate_response(message_text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=message_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Define a function to handle incoming messages
def handle_message(update, context):
    message_text = update.message.text
    response_text = generate_response(message_text)
    update.message.reply_text(response_text)

# Set up Telegram bot
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=bot_token)
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Add message handler to Telegram bot
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
port = int(os.environ.get("PORT",8443))
updater.start_webhook(listen="0.0.0.0", port=port, url_path=bot_token)
updater.bot.setWebhook(os.getenv("APP_URL") + bot_token)
updater.idle()
