# Configuration file for FastFig VPN Bot
# فایل تنظیمات ربات FastFig

import os

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Admin Configuration  
ADMIN_IDS = [5226795399, 7805096301]
SUPPORT_USERNAME = "@FastFigSupport"

# Payment Configuration
CARD_NUMBER = "6219861907900798"
BANK_NAME = "بانک ملی"
CARD_OWNER = "FastFig VPN"

# Plans Configuration with detailed info
PLANS_CONFIG = {
    'mini': {
        'name': '💼 Pack Mini',
        'volume': '50 گیگ',
        'duration': '1 ماه',
        'price': '180,000 تومان',
        'price_numeric': 180000,
        'zarinpal_link': 'https://zarinp.al/730375',
        'servers': '10 سرور',
        'users': 'تا 3 کاربر',
        'speed': 'تا 100 مگ'
    },
    'boost': {
        'name': '🚀 Pack Boost', 
        'volume': '75 گیگ',
        'duration': '1 ماه',
        'price': '230,000 تومان',
        'price_numeric': 230000,
        'zarinpal_link': 'https://zarinp.al/730378',
        'servers': '15 سرور',
        'users': 'تا 5 کاربر', 
        'speed': 'تا 150 مگ'
    },
    'turbo': {
        'name': '🔥 Pack Turbo',
        'volume': '100 گیگ', 
        'duration': '1 ماه',
        'price': '280,000 تومان',
        'price_numeric': 280000,
        'zarinpal_link': 'https://zarinp.al/730379',
        'servers': '20 سرور',
        'users': 'تا 7 کاربر',
        'speed': 'تا 200 مگ'
    },
    'ultra': {
        'name': '👑 Pack Ultra',
        'volume': '150 گیگ',
        'duration': '1 ماه', 
        'price': '350,000 تومان',
        'price_numeric': 350000,
        'zarinpal_link': 'https://zarinp.al/730380',
        'servers': '25 سرور',
        'users': 'نامحدود',
        'speed': 'تا 300 مگ'
    }
}

# Messages Configuration
MESSAGES = {
    'welcome': """🎉 به ربات فروش رسمی FastFig خوش اومدی!
✅ سرویس‌های پرسرعت V2Ray با کیفیت بالا  
🌍 مولتی‌لوکیشن با آپتایم ۹۹.۹٪  
👥 کانفیگ‌ها به‌صورت کاربر نامحدود ارائه می‌شن  
📱 قابل استفاده در: اندروید | آیفون | ویندوز | مک  
🎧 پشتیبانی ۲۴ ساعته + تضمین کیفیت""",
    
    'plan_details': """📦 جزئیات بیشتر:
🌐 سرورها: {servers}
👥 کاربران همزمان: {users}
⚡ سرعت: {speed}
🔒 پروتکل: V2Ray + VMess
🛡️ امنیت: TLS 1.3
📍 لوکیشن: آلمان، هلند، آمریکا""",
    
    'card_payment': """💳 پرداخت کارت‌به‌کارت

🏦 بانک: {bank_name}
💳 شماره کارت: `{card_number}`
👤 صاحب کارت: {card_owner}
💰 مبلغ قابل پرداخت: {price}

✅ پس از واریز، لطفاً عکس یا متن رسید پرداخت را ارسال کنید.
📝 رسید شما به سرعت بررسی و سرویس فعال خواهد شد.
⏰ زمان فعال‌سازی: حداکثر 10 دقیقه""",
    
    'receipt_received': """✅ رسید پرداخت شما دریافت شد!
⏳ تا ۱۰ دقیقه دیگر سرویس شما فعال خواهد شد.
📞 برای پیگیری: {support_username}
🔔 بعد از تایید، کانفیگ‌ها ارسال خواهد شد.""",
    
    'payment_approved': """🎉 پرداخت شما تایید شد!
✅ سرویس شما فعال شده است.
📱 کانفیگ‌ها از طریق پشتیبانی ارسال خواهد شد.
📞 {support_username}
🔄 برای دریافت فوری: /start""",
    
    'payment_denied': """❌ پرداخت شما تایید نشد.
📞 برای بررسی با پشتیبانی تماس بگیرید: {support_username}
💡 ممکن است مبلغ کامل واریز نشده باشد.""",
    
    'support_info': """برای ارتباط با پشتیبانی، لطفاً به آیدی زیر پیام دهید:  
📞 {support_username}

⏰ ساعات پاسخگویی: ۸ صبح تا ۱۲ شب
💬 زمان پاسخ: کمتر از 30 دقیقه
🔧 خدمات: راه‌اندازی، آموزش، پشتیبانی فنی"""
}

# Bot Settings
BOT_SETTINGS = {
    'max_receipt_size': 20 * 1024 * 1024,  # 20MB
    'receipt_timeout': 600,  # 10 minutes
    'health_check_interval': 300,  # 5 minutes  
    'rate_limit_delay': 0.1,  # 100ms between messages
    'auto_restart': True,
    'log_level': 'INFO'
}

# Database Tables (for future SQLite integration)
DATABASE_SCHEMA = {
    'users': {
        'id': 'INTEGER PRIMARY KEY',
        'username': 'TEXT',
        'first_name': 'TEXT',
        'last_name': 'TEXT', 
        'first_seen': 'TIMESTAMP',
        'last_activity': 'TIMESTAMP',
        'is_active': 'BOOLEAN DEFAULT 1'
    },
    'payments': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'user_id': 'INTEGER',
        'plan': 'TEXT',
        'amount': 'INTEGER',
        'receipt_type': 'TEXT',
        'message_id': 'INTEGER',
        'status': 'TEXT DEFAULT "pending"',
        'created_at': 'TIMESTAMP',
        'approved_at': 'TIMESTAMP',
        'approved_by': 'INTEGER'
    },
    'configs': {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT', 
        'user_id': 'INTEGER',
        'plan': 'TEXT',
        'config_data': 'TEXT',
        'expires_at': 'TIMESTAMP',
        'is_active': 'BOOLEAN DEFAULT 1'
    }
}

# Zarinpal Configuration (if needed for API integration)
ZARINPAL_CONFIG = {
    'merchant_id': 'YOUR_MERCHANT_ID',
    'sandbox': True,  # Set to False for production
    'callback_url': 'https://your-domain.com/callback'
}

# Server Locations
SERVER_LOCATIONS = [
    "🇩🇪 آلمان - فرانکفورت",
    "🇳🇱 هلند - آمستردام", 
    "🇺🇸 آمریکا - نیویورک",
    "🇺🇸 آمریکا - لس‌آنجلس",
    "🇬🇧 انگلستان - لندن",
    "🇫🇷 فرانسه - پاریس",
    "🇸🇬 سنگاپور",
    "🇯🇵 ژاپن - توکیو"
]

# Custom keyboard layouts
KEYBOARD_LAYOUTS = {
    'main_menu': [
        [('💼 Pack Mini', 'plan_mini'), ('🚀 Pack Boost', 'plan_boost')],
        [('🔥 Pack Turbo', 'plan_turbo'), ('👑 Pack Ultra', 'plan_ultra')], 
        [('💬 پشتیبانی', 'support')]
    ],
    'payment_methods': [
        [('💳 پرداخت کارت‌به‌کارت', 'card_payment')],
        [('🔗 پرداخت زرین‌پال', 'zarinpal_payment')],
        [('🔙 بازگشت به منو', 'back_to_menu')]
    ]
}

# Logging Configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        }
    }
}