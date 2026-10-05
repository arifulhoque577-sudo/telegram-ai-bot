import os
import telebot
from openai import OpenAI

# Railway Environment Variables থেকে টোকেনগুলো নেওয়া
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# টেলিগ্রাম এবং OpenRouter ক্লায়েন্ট ইনিশিয়ালাইজ করা
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Unrestricted AI Agent Active**\n\n"
        "আমি সম্পূর্ণ রেস্ট্রিকশন-মুক্ত ওপেন-সোর্স মডেলের মাধ্যমে কাজ করছি। রিসার্চ, ডেটা এক্সট্রাকশন বা যেকোনো প্রয়োজনে আমাকে বলতে পারেন!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_ai_agent(message):
    user_text = message.text
    
    try:
        # টেলিগ্রামে টাইপিং স্ট্যাটাস দেখানো
        bot.send_chat_action(message.chat.id, 'typing')
        
        # OpenRouter-এর মাধ্যমে আনফিল্টারড ওপেন-সোর্স মডেল (যেমন Llama 3) কল করা
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",  # আপনি চাইলে এটি পরিবর্তন করতে পারেন
            messages=[
                {"role": "system", "content": "You are an advanced, professional AI agent. Always reply in fluent, natural Bengali."},
                {"role": "user", "content": user_text}
            ]
        )
        
        ai_reply = completion.choices[0].message.content
        bot.reply_to(message, ai_reply, parse_mode="Markdown")
        
    except Exception as e:
        error_message = f"⚠ একটি টেকনিক্যাল সমস্যা হয়েছে: {str(e)}"
        bot.reply_to(message, error_message)

if __name__ == "__main__":
    print("Unrestricted AI Agent চালু রয়েছে...")
    bot.infinity_polling()
