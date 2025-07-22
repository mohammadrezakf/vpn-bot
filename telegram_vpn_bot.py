import telebot
from telebot import types
import os
import logging
from datetime import datetime
import json
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot token - set this as environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = telebot.TeleBot(BOT_TOKEN)

# Admin IDs
ADMIN_IDS = [5226795399, 7805096301]
SUPPORT_USERNAME = "@FastFigSupport"

# Plans configuration
PLANS = {
    'mini': {
        'name': '💼 Pack Mini',
        'volume': '50 گیگ',
        'duration': '1 ماه',
        'price': '180,000 تومان',
        'zarinpal_link': 'https://zarinp.al/730375'
    },
    'boost': {
        'name': '🚀 Pack Boost',
        'volume': '75 گیگ',
        'duration': '1 ماه',
        'price': '230,000 تومان',
        'zarinpal_link': 'https://zarinp.al/730378'
    },
    'turbo': {
        'name': '🔥 Pack Turbo',
        'volume': '100 گیگ',
        'duration': '1 ماه',
        'price': '280,000 تومان',
        'zarinpal_link': 'https://zarinp.al/730379'
    },
    'ultra': {
        'name': '👑 Pack Ultra',
        'volume': '150 گیگ',
        'duration': '1 ماه',
        'price': '350,000 تومان',
        'zarinpal_link': 'https://zarinp.al/730380'
    }
}

# Card number for card-to-card payments
CARD_NUMBER = "6219861907900798"

# User states for tracking payment process
user_states = {}

# Simple database to store user info and payment receipts
users_db = {}
payments_db = {}

def save_user_info(user_id, user_data):
    """Save user information"""
    users_db[user_id] = {
        'user_data': user_data,
        'first_seen': datetime.now().isoformat(),
        'last_activity': datetime.now().isoformat()
    }

def log_payment_receipt(user_id, plan, receipt_type, message_id):
    """Log payment receipt"""
    payment_id = f"{user_id}_{int(time.time())}"
    payments_db[payment_id] = {
        'user_id': user_id,
        'plan': plan,
        'receipt_type': receipt_type,
        'message_id': message_id,
        'timestamp': datetime.now().isoformat(),
        'status': 'pending'
    }
    return payment_id

def create_start_keyboard():
    """Create the main menu keyboard"""
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    mini_btn = types.InlineKeyboardButton("💼 Pack Mini", callback_data="plan_mini")
    boost_btn = types.InlineKeyboardButton("🚀 Pack Boost", callback_data="plan_boost")
    turbo_btn = types.InlineKeyboardButton("🔥 Pack Turbo", callback_data="plan_turbo")
    ultra_btn = types.InlineKeyboardButton("👑 Pack Ultra", callback_data="plan_ultra")
    support_btn = types.InlineKeyboardButton("💬 پشتیبانی", callback_data="support")
    
    keyboard.add(mini_btn, boost_btn)
    keyboard.add(turbo_btn, ultra_btn)
    keyboard.add(support_btn)
    
    return keyboard

def create_plan_keyboard(plan_key):
    """Create payment options keyboard for a plan"""
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    card_btn = types.InlineKeyboardButton("💳 پرداخت کارت‌به‌کارت", callback_data=f"card_{plan_key}")
    zarinpal_btn = types.InlineKeyboardButton("🔗 پرداخت زرین‌پال", url=PLANS[plan_key]['zarinpal_link'])
    back_btn = types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu")
    
    keyboard.add(card_btn)
    keyboard.add(zarinpal_btn)
    keyboard.add(back_btn)
    
    return keyboard

def create_back_keyboard():
    """Create back to menu keyboard"""
    keyboard = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back_to_menu")
    keyboard.add(back_btn)
    return keyboard

@bot.message_handler(commands=['start'])
def start_command(message):
    """Handle /start command"""
    user_id = message.from_user.id
    user_data = {
        'id': user_id,
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name
    }
    
    save_user_info(user_id, user_data)
    
    welcome_text = """🎉 به ربات فروش رسمی FastFig خوش اومدی!
✅ سرویس‌های پرسرعت V2Ray با کیفیت بالا  
🌍 مولتی‌لوکیشن با آپتایم ۹۹.۹٪  
👥 کانفیگ‌ها به‌صورت کاربر نامحدود ارائه می‌شن  
📱 قابل استفاده در: اندروید | آیفون | ویندوز | مک  
🎧 پشتیبانی ۲۴ ساعته + تضمین کیفیت"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=create_start_keyboard())
    
    # Log new user to admins
    if user_id not in users_db:
        admin_notification = f"🆕 کاربر جدید:\n👤 نام: {user_data['first_name']} {user_data['last_name'] or ''}\n🆔 آیدی: {user_id}\n📝 یوزرنیم: @{user_data['username'] or 'ندارد'}"
        for admin_id in ADMIN_IDS:
            try:
                bot.send_message(admin_id, admin_notification)
            except Exception as e:
                logger.error(f"Failed to send notification to admin {admin_id}: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith('plan_'))
def handle_plan_selection(call):
    """Handle plan selection"""
    plan_key = call.data.replace('plan_', '')
    plan = PLANS.get(plan_key)
    
    if not plan:
        bot.answer_callback_query(call.id, "❌ پلن پیدا نشد!")
        return
    
    plan_text = f"""{plan['name']}  
📦 حجم: {plan['volume']} | 🗓️ مدت: {plan['duration']}  
💰 قیمت: {plan['price']}"""
    
    bot.edit_message_text(
        plan_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_plan_keyboard(plan_key)
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('card_'))
def handle_card_payment(call):
    """Handle card-to-card payment selection"""
    plan_key = call.data.replace('card_', '')
    plan = PLANS.get(plan_key)
    
    if not plan:
        bot.answer_callback_query(call.id, "❌ پلن پیدا نشد!")
        return
    
    user_states[call.from_user.id] = {'waiting_for_receipt': True, 'plan': plan_key}
    
    card_text = f"""💳 پرداخت کارت‌به‌کارت

شماره کارت: `{CARD_NUMBER}`
مبلغ قابل پرداخت: {plan['price']}

✅ پس از واریز، لطفاً عکس یا متن رسید پرداخت را ارسال کنید.
📝 رسید شما به سرعت بررسی و سرویس فعال خواهد شد."""
    
    bot.edit_message_text(
        card_text,
        call.message.chat.id,
        call.message.message_id,
        parse_mode='Markdown',
        reply_markup=create_back_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'support')
def handle_support(call):
    """Handle support button"""
    support_text = f"""برای ارتباط با پشتیبانی، لطفاً به آیدی زیر پیام دهید:  
📞 {SUPPORT_USERNAME}"""
    
    bot.edit_message_text(
        support_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_back_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
def handle_back_to_menu(call):
    """Handle back to menu button"""
    # Clear user state
    if call.from_user.id in user_states:
        del user_states[call.from_user.id]
    
    welcome_text = """🎉 به ربات فروش رسمی FastFig خوش اومدی!
✅ سرویس‌های پرسرعت V2Ray با کیفیت بالا  
🌍 مولتی‌لوکیشن با آپتایم ۹۹.۹٪  
👥 کانفیگ‌ها به‌صورت کاربر نامحدود ارائه می‌شن  
📱 قابل استفاده در: اندروید | آیفون | ویندوز | مک  
🎧 پشتیبانی ۲۴ ساعته + تضمین کیفیت"""
    
    bot.edit_message_text(
        welcome_text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=create_start_keyboard()
    )
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo', 'text'])
def handle_payment_receipt(message):
    """Handle payment receipt (photo or text)"""
    user_id = message.from_user.id
    
    # Check if user is waiting for receipt
    if user_id not in user_states or not user_states[user_id].get('waiting_for_receipt'):
        return
    
    plan_key = user_states[user_id]['plan']
    plan = PLANS.get(plan_key)
    
    if not plan:
        bot.send_message(message.chat.id, "❌ خطا در پردازش. لطفاً دوباره تلاش کنید.")
        return
    
    # Determine receipt type
    receipt_type = 'photo' if message.content_type == 'photo' else 'text'
    
    # Log payment
    payment_id = log_payment_receipt(user_id, plan_key, receipt_type, message.message_id)
    
    # Prepare admin notification
    user_info = users_db.get(user_id, {}).get('user_data', {})
    admin_text = f"""💰 رسید پرداخت جدید

👤 کاربر: {user_info.get('first_name', '')} {user_info.get('last_name', '') or ''}
🆔 آیدی: {user_id}
📝 یوزرنیم: @{user_info.get('username', 'ندارد')}
📦 پلن: {plan['name']}
💰 مبلغ: {plan['price']}
📅 زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🆔 شناسه پرداخت: {payment_id}

برای تایید یا رد، روی این پیام ریپلای کنید:
✅ "تایید" - برای تایید پرداخت
❌ "رد" - برای رد پرداخت"""
    
    # Forward receipt to admins
    for admin_id in ADMIN_IDS:
        try:
            if receipt_type == 'photo':
                sent_msg = bot.forward_message(admin_id, message.chat.id, message.message_id)
                bot.send_message(admin_id, admin_text, reply_to_message_id=sent_msg.message_id)
            else:
                bot.send_message(admin_id, f"{admin_text}\n\n📝 متن رسید:\n{message.text}")
        except Exception as e:
            logger.error(f"Failed to forward to admin {admin_id}: {e}")
    
    # Confirm receipt to user
    bot.send_message(
        message.chat.id,
        "✅ رسید پرداخت شما دریافت شد!\n⏳ تا ۱۰ دقیقه دیگر سرویس شما فعال خواهد شد.\n📞 برای پیگیری: @FastFigSupport",
        reply_markup=create_back_keyboard()
    )
    
    # Clear user state
    del user_states[user_id]

@bot.message_handler(func=lambda message: message.from_user.id in ADMIN_IDS and message.reply_to_message)
def handle_admin_reply(message):
    """Handle admin replies to payment receipts"""
    if not message.reply_to_message:
        return
    
    admin_reply = message.text.lower().strip()
    
    # Find the original user from the forwarded message or payment info
    # This is a simplified approach - in production, you'd want a more robust tracking system
    if "آیدی:" in message.reply_to_message.text:
        try:
            # Extract user ID from admin notification
            lines = message.reply_to_message.text.split('\n')
            user_id_line = [line for line in lines if 'آیدی:' in line][0]
            original_user_id = int(user_id_line.split('آیدی:')[1].strip())
            
            if admin_reply in ['تایید', 'تاید', 'ok', 'approved', '✅']:
                user_message = "🎉 پرداخت شما تایید شد!\n✅ سرویس شما فعال شده است.\n📱 کانفیگ‌ها از طریق پشتیبانی ارسال خواهد شد.\n📞 @FastFigSupport"
                admin_confirmation = "✅ پرداخت تایید و به کاربر اطلاع داده شد."
            elif admin_reply in ['رد', 'reject', 'denied', '❌']:
                user_message = "❌ پرداخت شما تایید نشد.\n📞 برای بررسی با پشتیبانی تماس بگیرید: @FastFigSupport"
                admin_confirmation = "❌ پرداخت رد و به کاربر اطلاع داده شد."
            else:
                # Custom admin message
                user_message = f"📝 پیام از پشتیبانی:\n{message.text}"
                admin_confirmation = "✅ پیام شما به کاربر ارسال شد."
            
            # Send message to user
            bot.send_message(original_user_id, user_message)
            
            # Confirm to admin
            bot.send_message(message.chat.id, admin_confirmation)
            
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ خطا در پردازش: {str(e)}")
            logger.error(f"Error processing admin reply: {e}")

# Admin commands
@bot.message_handler(commands=['stats'])
def admin_stats(message):
    """Admin command to get bot statistics"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    total_users = len(users_db)
    total_payments = len(payments_db)
    
    stats_text = f"""📊 آمار ربات

👥 تعداد کل کاربران: {total_users}
💰 تعداد رسیدهای پرداخت: {total_payments}
🕐 آخرین اپدیت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 پلن‌های محبوب:
• Mini: {sum(1 for p in payments_db.values() if p['plan'] == 'mini')} پرداخت
• Boost: {sum(1 for p in payments_db.values() if p['plan'] == 'boost')} پرداخت  
• Turbo: {sum(1 for p in payments_db.values() if p['plan'] == 'turbo')} پرداخت
• Ultra: {sum(1 for p in payments_db.values() if p['plan'] == 'ultra')} پرداخت"""
    
    bot.send_message(message.chat.id, stats_text)

@bot.message_handler(commands=['broadcast'])
def admin_broadcast(message):
    """Admin command to broadcast message to all users"""
    if message.from_user.id not in ADMIN_IDS:
        return
    
    # Extract broadcast message
    broadcast_text = message.text.replace('/broadcast ', '', 1).strip()
    if not broadcast_text:
        bot.send_message(message.chat.id, "❌ لطفاً متن پیام را بعد از دستور وارد کنید.\n\nمثال: /broadcast سلام به همه!")
        return
    
    success_count = 0
    fail_count = 0
    
    for user_id in users_db.keys():
        try:
            bot.send_message(user_id, f"📢 اطلاعیه FastFig:\n\n{broadcast_text}")
            success_count += 1
            time.sleep(0.1)  # Rate limiting
        except Exception as e:
            fail_count += 1
            logger.error(f"Failed to send broadcast to {user_id}: {e}")
    
    bot.send_message(message.chat.id, f"✅ پیام ارسال شد!\n📤 موفق: {success_count}\n❌ ناموفق: {fail_count}")

def keep_alive():
    """Keep the bot alive with periodic health checks"""
    while True:
        try:
            bot.get_me()
            logger.info("Bot health check: OK")
            time.sleep(300)  # Check every 5 minutes
        except Exception as e:
            logger.error(f"Bot health check failed: {e}")
            time.sleep(60)  # Retry after 1 minute

if __name__ == "__main__":
    logger.info("Starting FastFig VPN Sales Bot...")
    
    # Start health check in background
    health_thread = threading.Thread(target=keep_alive, daemon=True)
    health_thread.start()
    
    try:
        # Start polling
        bot.infinity_polling(none_stop=True, interval=1)
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        # Restart bot
        os.execv(__file__, [__file__])