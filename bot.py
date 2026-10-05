
import os
import telebot
from google import genai

# Railway থেকে টোকেনগুলো নেওয়া হবে
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# টেলিগ্রাম এবং জিমেইনের ক্লায়েন্ট ইনিশিয়ালাইজ করা
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "হ্যালো! আমি আপনার জিমেইনের এআই টেলিগ্রাম বট। আমাকে যেকোনো প্রশ্ন করতে পারেন!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    
    try:
        # ব্যবহারকারীকে বোঝানোর জন্য যে বট লিখছে
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Google Gemini AI থেকে রেসপন্স আনা (Gemini 2.5 Flash মডেল ব্যবহার করা হচ্ছে)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        
        ai_reply = response.text
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        bot.reply_to(message, f"দুঃখিত, একটি সমস্যা হয়েছে: {str(e)}")

if __name__ == "__main__":
    print("AI Bot is running...")
    bot.infinity_polling()
