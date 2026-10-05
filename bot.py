import os
import telebot
from openai import OpenAI
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# User-der chat history/memory store korar jonno dictionary
user_sessions = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    user_sessions[chat_id] = [
        {"role": "system", "content": "You are an advanced, professional AI agent. Always reply in fluent, natural Bengali and remember previous context of the conversation."}
    ]
    welcome_text = (
        "🤖 **Context-Aware AI Agent Active**\n\n"
        "Ami ekhon theke apnar ager shob kotha ebong massage mone rakhte parbo. Bolun, ki sahajjo korte pari?"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_ai_agent(message):
    user_text = message.text
    chat_id = message.chat.id
    
    # Jodi prothom bar hoy, tahole session initialize kore nibe
    if chat_id not in user_sessions:
        user_sessions[chat_id] = [
            {"role": "system", "content": "You are an advanced, professional AI agent. Always reply in fluent, natural Bengali and remember previous context of the conversation."}
        ]
    
    try:
        # User jodi chobi ba visual kichu create korte bole
        if "chobi" in user_text.lower() or "draw" in user_text.lower() or "image" in user_text.lower() or "photo" in user_text.lower():
            bot.send_chat_action(chat_id, 'upload_photo')
            image_prompt = requests.utils.quote(user_text)
            image_url = f"https://image.pollinations.ai/prompt/{image_prompt}"
            bot.send_photo(chat_id, image_url, caption="🎨 Apnar onurodh kora chobi!")
            return

        bot.send_chat_action(chat_id, 'typing')
        
        # User-er massage-ti history-te add kora
        user_sessions[chat_id].append({"role": "user", "content": user_text})
        
        # OpenRouter-e shob history shohit pathano
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=user_sessions[chat_id]
        )
        
        ai_reply = completion.choices[0].message.content
        
        # AI-er reply-o history-te add kore rakha, jate porer bar mone rakhe
        user_sessions[chat_id].append({"role": "assistant", "content": ai_reply})
        
        # History beshi boro hoye gele memory clean korar babostha (optional, last 20 messages rakha)
        if len(user_sessions[chat_id]) > 20:
            user_sessions[chat_id] = [user_sessions[chat_id][0]] + user_sessions[chat_id][-19:]

        bot.reply_to(message, ai_reply, parse_mode="Markdown")
        
    except Exception as e:
        error_message = f"⚠ Ekti technical shomossha hoyeche: {str(e)}"
        bot.reply_to(message, error_message)

if __name__ == "__main__":
    print("Memory-enabled AI Agent cholche...")
    bot.infinity_polling()
