import os
from pymongo import MongoClient
from telebot import TeleBot

# Fetch variables from the environment
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Bot token from Koyeb
MONGO_URI = os.getenv("MONGO_URI")  # MongoDB connection string
DATABASE_NAME = os.getenv("DATABASE_NAME")  # Database name
COLLECTION_NAME = os.getenv("COLLECTION_NAME")  # Collection name

bot = TeleBot(BOT_TOKEN)
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@bot.callback_query_handler(func=lambda call: True)
def handle_movie_click(call):
    try:
        # Extract the movie name from the button click
        movie_name = call.data  # This should match the file_name in your database

        # Check if the movie exists in the database
        movie = collection.find_one({"file_name": movie_name})
        
        if movie:
            # Log the movie details to check if it's being fetched correctly
            print(f"Fetched Movie: {movie}")
            
            # Send the movie file to the user
            bot.send_document(chat_id=call.from_user.id, document=movie["_id"])
            bot.answer_callback_query(call.id, "Movie sent to your private chat!")
        else:
            # If the movie is not found, send a message
            bot.answer_callback_query(call.id, "Movie not found in the database.")
            print("Movie not found in the database.")
    except Exception as e:
        # Handle errors
        bot.answer_callback_query(call.id, "An error occurred. Please try again.")
        print(f"Error: {e}")

bot.polling()
