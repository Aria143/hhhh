import os
from telegram.ext import Updater, MessageHandler, Filters
from transformers import pipeline

# Load ChatGPT pipeline
chatbot = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

# Define function to handle incoming messages
def reply(update, context):
    # Get user's message
    user_message = update.message.text
    
    # Generate response using ChatGPT
    chatbot_response = chatbot(user_message, max_length=50)[0]['generated_text']
    
    # Send response back to user
    context.bot.send_message(chat_id=update.effective_chat.id, text=chatbot_response)

# Create a Telegram bot updater with your bot token
updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)

# Register a message handler for incoming messages
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

# Start the bot
updater.start_polling()

