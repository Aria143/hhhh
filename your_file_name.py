import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import argparse

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telegram bot')
    parser.add_argument('--port', type=int, default=8443,
                        help='The port number for the webhook (default: 8443)')
    args = parser.parse_args()

    # Start the bot using a webhook with the specified port number
    updater.start_webhook(listen="0.0.0.0",
                          port=args.port,
                          url_path=bot_token)
    updater.bot.setWebhook(url="https://hgfhhj.herokuapp.com/" + bot_token)

    # Start the server
    updater.idle()
