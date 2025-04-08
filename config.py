"""
ملف التكوين لبوت تيليجرام لتحميل محادثات Twitter Spaces الصوتية
"""

# توكن API لبوت تيليجرام
TELEGRAM_BOT_TOKEN = "8164143784:AAFGXalMO17K3iPP0t7TVGthcG9-l1tCsZg"

# مجلد لتخزين الملفات الصوتية المؤقتة
TEMP_FOLDER = "/home/ubuntu/twitter_spaces_bot/temp"

# الحد الأقصى لحجم الملف (بالبايت) الذي يمكن إرساله عبر تيليجرام (50 ميجابايت)
MAX_TELEGRAM_FILE_SIZE = 50 * 1024 * 1024
