from pymongo import MongoClient
from telebot import TeleBot

# Bot token and MongoDB connection details
BOT_TOKEN = "your_bot_token"
MONGO_URI = "your_mongodb_connection_string"
DATABASE_NAME = "your_database_name"
COLLECTION_NAME = "your_collection_name"

bot = TeleBot(BOT_TOKEN)
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@bot.callback_query_handler(func=lambda call: True)
def handle_movie_click(call):
    try:
        # Extract movie name from the callback data
        movie_name = call.data  # Ensure call.data is set to the movie name

        # Query the database for the movie
        movie = collection.find_one({"file_name": movie_name})
        
        if movie:
            # Send the file to the user using the _id as the file_id
            bot.send_document(chat_id=call.from_user.id, document=movie["_id"])
            bot.answer_callback_query(call.id, "Movie sent to your private chat!")
        else:
            # Notify if the movie is not found
            bot.answer_callback_query(call.id, "Movie not found in the database.")
    except Exception as e:
        # Handle errors and notify the user
        bot.answer_callback_query(call.id, "Failed to send the movie. Please try again.")
        print(f"Error: {e}")

bot.polling()





