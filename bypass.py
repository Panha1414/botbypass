import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keep_alive import keep_alive  # នាំចូលមុខងារដាស់ Server ពី keep_alive.py

# ១. បំពេញ Token របស់ Bot អ្នកនៅទីនេះ
BOT_TOKEN = '8823039793:AAHPx4gdhwc9RFBHTvQqRTx75EGD9sq6TVw'

# ២. ព័ត៌មាន Channel និង YouTube របស់អ្នក
CHANNEL_USERNAME = 'https://t.me/SPROBLOX'
YOUTUBE_LINK = 'https://www.youtube.com/@Sp_roblox1'

# ៣. លីង Bot របស់គេដែលអ្នកចង់បញ្ជូនសមាជិកទៅ
BYPASS_BOT_LINK = 'https://t.me/bypasstools_bot'

bot = telebot.TeleBot(BOT_TOKEN)

def check_membership(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        if status in ['member', 'administrator', 'creator']:
            return True
        return False
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False

def get_verification_markup():
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("1️⃣ Join Telegram Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
    markup.row(InlineKeyboardButton("2️⃣ Subscribe YouTube", url=YOUTUBE_LINK))
    markup.row(InlineKeyboardButton("✅ ខ្ញុំបានធ្វើរួចរាល់ (Verify)", callback_data="check_verify"))
    return markup

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    if not check_membership(user_id):
        bot.reply_to(message, "⚠️ សួស្តី! សូម Join Channel និង Subscribe YouTube ជាមុនសិន ដើម្បីអាចប្រើប្រាស់មុខងារ Bypass បាន!", reply_markup=get_verification_markup())
    else:
        bot.reply_to(message, f"✅ សួស្តី! អ្នកបានផ្ទៀងផ្ទាត់រួចរាល់។\n\n👉 សូមចុចទីនេះដើម្បីចូលទៅកាន់ Bot ទម្លុះលីង៖ {BYPASS_BOT_LINK}")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    # ឆែកមើលបើមិនទាន់ Join ឱ្យលោតប៊ូតុង
    if not check_membership(user_id):
        bot.reply_to(message, "⚠️ អ្នកមិនទាន់បាន Join Channel ទេ! សូមបំពេញលក្ខខណ្ឌសិន៖", reply_markup=get_verification_markup())
    else:
        # បើ Join ហើយ ប្រាប់ឱ្យគេទៅប្រើ Bot របស់គេ
        bot.reply_to(message, f"✅ ការផ្ទៀងផ្ទាត់ជោគជ័យ!\n\nដើម្បីទម្លុះលីង (Bypass) សូមចុចចូលទៅកាន់ Bot នេះរួចផ្ញើលីងរបស់អ្នកចូលទីនោះ៖\n👉 **[@bypasstools_bot]({BYPASS_BOT_LINK})**", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "check_verify")
def verify_callback(call):
    user_id = call.from_user.id
    try:
        if check_membership(user_id):
            bot.answer_callback_query(call.id, "✅ អរគុណសម្រាប់ការ Join!", show_alert=True)
            # លុបប៊ូតុង Join ចោល ហើយប្តូរទៅជាសារប្រាប់លីង Bot ថ្មី
            success_text = f"✅ ការផ្ទៀងផ្ទាត់ជោគជ័យ!\n\n👉 សូមចុចទីនេះដើម្បីចូលទៅកាន់ Bot ទម្លុះលីង៖ {BYPASS_BOT_LINK}"
            bot.edit_message_text(success_text, chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "❌ អ្នកមិនទាន់បាន Join Channel Telegram ទេ! សូម Join សិន។", show_alert=True)
    except Exception as e:
        print(f"Callback Verify Error: {e}")
        bot.answer_callback_query(call.id, "⚠️ Bot មិនទាន់ក្លាយជា Admin ក្នុង Channel ទេ។", show_alert=True)

if __name__ == "__main__":
    print("✅ ចាប់ផ្តើមដំណើរការ Web Server (ដើម្បីកុំឱ្យ Render បិទ)...")
    keep_alive() # ហៅមុខងារដាស់ Server
    
    print("✅ Gateway Bot កំពុងដំណើរការ...")
    bot.infinity_polling()
