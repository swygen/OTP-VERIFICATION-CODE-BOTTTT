import telebot
import requests
import random
from flask import Flask, request, jsonify
from threading import Thread
from keep_alive import keep_alive

# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
# 🔥 CONFIGURATION (আপনার দেওয়া তথ্য)
# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
BOT_TOKEN = '8289077014:AAEDWa3psG8PxOKtWibsp-0uzzGkyEFCw3E' #
ADMIN_ID = 6243881362 #

# 🔑 SMS API CREDENTIALS (SendMySMS.net)
SMS_API_URL = "https://sendmysms.net/api.php" #
SMS_USER = "swygen"                             #
SMS_KEY = "353f2fdf74fd02928be4330f7efb78b7"    #

bot = telebot.TeleBot(BOT_TOKEN, parse_mode='Markdown')
app = Flask(__name__)

# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
# 📨 SMS SENDING FUNCTION
# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
def send_sms_gateway(phone, message):
    payload = {
        "user": SMS_USER,
        "key": SMS_KEY,
        "to": phone,
        "msg": message
    }
    try:
        # API Hit
        response = requests.post(SMS_API_URL, data=payload)
        return response.text
    except Exception as e:
        return str(e)

# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
# 🌐 WEBSITE API (Webhook)
# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
@app.route('/send_otp', methods=['GET'])
def api_handler():
    # 1. Get Phone Number from URL
    phone = request.args.get('phone')
    
    if not phone:
        return jsonify({"status": "error", "message": "Phone number missing"}), 400

    # 2. Generate 6 Digit OTP
    otp_code = str(random.randint(100000, 999999))
    
    # 3. Create Message Body
    msg_body = f"BD INVESTMENT Verification Code: {otp_code}
Valid for 10 minutes.
Do not share this code with anyone."
    
    # 4. Send SMS via Gateway
    resp = send_sms_gateway(phone, msg_body)
    
    # 5. Log to Admin Telegram
    try:
        bot.send_message(
            ADMIN_ID,
            f"📡 **New OTP Request**\n"
            f"📱 Phone: `{phone}`\n"
            f"🔢 OTP: `{otp_code}`\n"
            f"✅ Gateway Response: {resp}"
        )
    except: pass

    # 6. Return OTP to Website (For Verification Logic)
    return jsonify({
        "status": "success",
        "otp": otp_code,
        "message": "SMS Sent Successfully"
    }), 200

@app.route('/')
def index():
    return "✅ Bot is Running..."

# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
# 🤖 BOT COMMANDS
# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
@bot.message_handler(commands=['start'])
def start_msg(m):
    msg = (
        f"🤖 **SMS Gateway Bot Active**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✅ **Service:** Online (24/7)\n"
        f"📡 **Provider:** SendMySMS.net\n\n"
        f"⚠️ **গুরুত্বপূর্ণ নির্দেশ:**\n"
        f"১. Render ড্যাশবোর্ড থেকে আপনার অ্যাপের নতুন লিংকটি কপি করুন।\n"
        f"২. `login.html` ফাইলে সেই লিংকটি বসান।\n"
    )
    bot.send_message(m.chat.id, msg)

# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
# 🔥 RUN SERVER
# ━─━─━─━─━─━─━─━─━─━─━─━─━─━
def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    # Start Flask
    Thread(target=run_flask).start()
    # Start Keep Alive
    keep_alive()
    # Start Bot
    bot.infinity_polling(skip_pending=True)