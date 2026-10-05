import os
import telebot
from google import genai

# Railway Environment Variables theke token & API key newa
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# Professional Welcome Message
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Professional AI Agent Active**\n\n"
        "Apni amake ye-kono shomossa, research, data extraction ba information-er jonno bolte paren. "
        "Ami shob shomoy shothik ebong professional bhabe sahajjo korar jonno prostut!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# Message Handler with Professional Prompt Engineering
@bot.message_handler(func=lambda message: True)
def handle_ai_agent(message):
    user_text = message.text
    
    try:
        # Typing action dekhano
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Professional agent instructions (Research, Data extraction ebong formatting er jonno)
        system_instruction = (
            "You are an advanced, professional AI agent and research assistant. "
            "You can handle data extraction, deep research, and technical breakdown. "
            "Always reply in fluent, natural Bengali. Maintain a professional, polite, and expert tone."
        )
        
        full_prompt = f"{system_instruction}\n\nUser Query: {user_text}"
        
        # Gemini Model call (Stable version)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=full_prompt,
        )
        
        ai_reply = response.text
        bot.reply_to(message, ai_reply, parse_mode="Markdown")
        
    except Exception as e:
        error_message = f"⚠️️ Dukkito, ekti technical samoshya hoyeche: {str(e)}"
        bot.reply_to(message, error_message)

if __name__ == "__main__":
    print("Professional AI Agent is running smoothly...")
    bot.infinity_polling()
