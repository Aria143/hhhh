import os
import openai
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

# Set up OpenAI API credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = "text-davinci-002"

# Set up Telegram bot credentials
bot_token = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=bot_token)

# Define handler functions for commands and messages
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a wierdo. What can I help you with?")

def chat(update, context):
    message = update.message.text
    response = openai.Completion.create(engine="davinci", prompt=message, max_tokens=1024, n=1, stop=None, temperature=0.7, model=model_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)

# Set up the Telegram bot updater and dispatcher
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Register the command and message handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chat))

# Start the bot
updater.start_polling()
