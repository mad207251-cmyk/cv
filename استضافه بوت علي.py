# ==========================================
#  استضافة بوتات تيليجرام الأسطورية 🤖
#  المطور: @SL_C6
#  قناة المطور: https://telegram.me/steamfree_456
# ==========================================

import os
import subprocess
import telebot
from telebot import types

# ضع توكن بوت الاستضافة الخاص بك هنا 👇
TOKEN = "8722562656:AAF1tkw-lr8rYUPR8WsynlRbisNNV-pAX4c"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

DEV_USERNAME = "@id11tt"
DEV_CHANNEL = "https://telegram.me/steamfree_456"

# مجلد حفظ الملفات والبوتات المرفوعة
UPLOAD_DIR = "hosted_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# لوحة التحكم الرئيسية (الأزرار الشفافة)
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📤 رفع ملف بوت", callback_data="upload"),
        types.InlineKeyboardButton("📁 الملفات المرفوعة", callback_data="list"),
        types.InlineKeyboardButton("▶️ تشغيل بوت", callback_data="run_menu"),
        types.InlineKeyboardButton("🗑 حذف بوت", callback_data="delete_menu"),
        types.InlineKeyboardButton("👤 المطور", url=f"https://t.me/{DEV_USERNAME.replace('@', '')}"),
        types.InlineKeyboardButton("📢 قناة المطور", url=DEV_CHANNEL)
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    welcome_msg = (
        f"أهلاً بك يا <b>{message.from_user.first_name}</b> في استضافتك الخاصة 🚀\n\n"
        f"قم برفع بوتاتك، شغلها، وتحكم بها بكل سهولة من الأزرار بالأسفل:"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if call.data == "upload":
        bot.answer_callback_query(call.id, "أرسل ملف البوت (.py) الآن ياغالي 📥")
    
    elif call.data == "list":
        files = os.listdir(UPLOAD_DIR)
        if files:
            text = "📁 <b>البوتات والملفات في الاستضافة:</b>\n\n"
            for i, f in enumerate(files, 1):
                text += f"{i}️⃣ <code>{f}</code>\n"
        else:
            text = "📁 عذراً، لا توجد أي بوتات مرفوعة حالياً."
        
        bot.edit_message_text(text, chat_id, message_id, reply_markup=main_menu())

    # قائمة تشغيل البوتات
    elif call.data == "run_menu":
        files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".py")]
        if not files:
            bot.answer_callback_query(call.id, "ماكو أي ملف بايثون (.py) مرفوع حتى أشغله!", show_alert=True)
            return
            
        markup = types.InlineKeyboardMarkup()
        for f in files:
            markup.add(types.InlineKeyboardButton(f"▶️ تشغيل: {f}", callback_data=f"run_{f}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("⚡️ <b>اختر البوت الذي تريد تشغيله:</b>", chat_id, message_id, reply_markup=markup)

    # تشغيل البوت الفعلي في الخلفية
    elif call.data.startswith("run_"):
        file_name = call.data.split("_", 1)[1]
        file_path = os.path.join(UPLOAD_DIR, file_name)
        try:
            # تشغيل البوت الثاني بشكل مستقل في السيرفر
            subprocess.Popen(["python", file_path])
            bot.answer_callback_query(call.id, f"✅ تم تشغيل البوت ({file_name}) بنجاح وبدأ يعمل!", show_alert=True)
        except Exception as e:
            bot.answer_callback_query(call.id, f"❌ فشل التشغيل: {str(e)}", show_alert=True)

    elif call.data == "delete_menu":
        files = os.listdir(UPLOAD_DIR)
        if not files:
            bot.answer_callback_query(call.id, "ماكو ملفات حتى أحذفها!", show_alert=True)
            return
            
        markup = types.InlineKeyboardMarkup()
        for f in files:
            markup.add(types.InlineKeyboardButton(f"🗑 حذف: {f}", callback_data=f"del_{f}"))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🗑 <b>اختر الملف المراد حذفه:</b>", chat_id, message_id, reply_markup=markup)

    elif call.data.startswith("del_"):
        file_name = call.data.split("_", 1)[1]
        file_path = os.path.join(UPLOAD_DIR, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            bot.answer_callback_query(call.id, f"✅ تم حذف {file_name} بنجاح")
        
        # تحديث القائمة
        files = os.listdir(UPLOAD_DIR)
        if not files:
            bot.edit_message_text("القائمة الرئيسية:", chat_id, message_id, reply_markup=main_menu())
        else:
            markup = types.InlineKeyboardMarkup()
            for f in files:
                markup.add(types.InlineKeyboardButton(f"🗑 حذف: {f}", callback_data=f"del_{f}"))
            markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
            bot.edit_message_text("🗑 <b>اختر الملف المراد حذفه:</b>", chat_id, message_id, reply_markup=markup)

    elif call.data == "back":
        bot.edit_message_text("القائمة الرئيسية للاستضافة 🤖:", chat_id, message_id, reply_markup=main_menu())

# استقبال الملفات المرفوعة وحفظها تلقائياً
@bot.message_handler(content_types=['document'])
def handle_files(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name
        
        save_path = os.path.join(UPLOAD_DIR, file_name)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        bot.reply_to(message, f"✅ <b>تم رفع البوت بنجاح!</b>\n📂 اسم الملف: <code>{file_name}</code>\n\nاضغط /start لفتح القائمة وتشغيله.", reply_markup=main_menu())
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء الرفع: {e}")

# تشغيل بوت الاستضافة الأساسي
if __name__ == "__main__":
    print(f"[-] Hosting Bot Started Successfully!")
    print(f"[-] Developer: {DEV_USERNAME}")
    bot.infinity_polling()
