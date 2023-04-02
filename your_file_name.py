import os
import logging
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from transformers import pipeline, set_seed

# Set the logging level
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Set the ChatGPT pipeline
generator = pipeline("text-generation", "EleutherAI/gpt-neo-2.7B")

# Set the seed for the random number generator (optional)
set_seed(42)

# Define a function to generate text using ChatGPT
def generate_text(update: Update, context: CallbackContext) -> None:
    # Get the message from the user
    message = update.message.text

    # Generate a response using ChatGPT
    response = generator(message, max_length=100)[0]['generated_text']

    # Send the response back to the user
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text=response)

# Define the main function
def main() -> None:
    # Get the Telegram bot token from the environment variable
    token = os.environ.get('TELEGRAM_BOT_TOKEN')

    # Create the Updater and pass the Telegram bot token
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register the generate_text handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, generate_text))

    # Start the Bot
    updater.start_polling()

    # Run the Bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
