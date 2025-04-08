"""
البوت الرئيسي لتحميل محادثات Twitter Spaces الصوتية
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from spaces_downloader import TwitterSpacesDownloader
from config import TELEGRAM_BOT_TOKEN, TEMP_FOLDER, MAX_TELEGRAM_FILE_SIZE

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إنشاء مُنزِّل محادثات Twitter Spaces
downloader = TwitterSpacesDownloader(TEMP_FOLDER)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    التعامل مع أمر /start
    """
    user = update.effective_user
    await update.message.reply_text(
        f"✅ مرحبًا {user.first_name}! البوت يعمل بشكل صحيح! ✅\n\n"
        "🤖 أنا بوت تحميل محادثات Twitter Spaces الصوتية. 🎙️\n\n"
        "🔴 البوت جاهز الآن لاستقبال طلباتك! 🔴\n\n"
        "يمكنك إرسال رابط محادثة Twitter Spaces أو رابط تغريدة تحتوي على محادثة، وسأقوم بتحميلها وإرسالها لك كملف صوتي. 🔊\n\n"
        "للمساعدة، أرسل /help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    التعامل مع أمر /help
    """
    help_text = (
        "🔸 *كيفية استخدام البوت:*\n\n"
        "1️⃣ انسخ رابط محادثة Twitter Spaces المسجلة أو رابط تغريدة تحتوي على محادثة\n"
        "2️⃣ أرسل الرابط إلى هذا البوت\n"
        "3️⃣ انتظر حتى يتم تحميل المحادثة ومعالجتها\n"
        "4️⃣ سيتم إرسال الملف الصوتي إليك\n\n"
        "🔸 *الأوامر المتاحة:*\n"
        "/start - بدء استخدام البوت\n"
        "/help - عرض هذه الرسالة\n"
        "/about - معلومات عن البوت\n\n"
        "🔸 *ملاحظات:*\n"
        "- يمكن تحميل المحادثات المسجلة فقط\n"
        "- يمكنك إرسال رابط محادثة مباشرة مثل: https://twitter.com/i/spaces/1YqJDqDgBjExV\n"
        "- أو رابط تغريدة تحتوي على محادثة مثل: https://twitter.com/username/status/1234567890\n"
        "- الحد الأقصى لحجم الملف هو 50 ميجابايت\n"
        "- قد تستغرق عملية التحميل بعض الوقت حسب حجم المحادثة"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    التعامل مع أمر /about
    """
    about_text = (
        "🤖 *بوت تحميل محادثات Twitter Spaces*\n\n"
        "هذا البوت يساعدك في تحميل محادثات Twitter Spaces الصوتية المسجلة وتحويلها إلى ملفات MP3.\n\n"
        "🔧 *التقنيات المستخدمة:*\n"
        "- Python\n"
        "- python-telegram-bot\n"
        "- yt-dlp\n"
        "- FFmpeg\n\n"
        "📝 *الإصدار:* 1.1.0\n"
        "🆕 *التحديثات الأخيرة:*\n"
        "- دعم روابط التغريدات التي تحتوي على محادثات Twitter Spaces\n"
        "- تحسين عملية التحقق من الروابط\n"
        "- تحسين عملية التحميل"
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def process_space_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    معالجة رابط محادثة Twitter Spaces أو تغريدة تحتوي على محادثة
    """
    url = update.message.text.strip()
    
    # التحقق من صحة الرابط
    if not (downloader.is_valid_twitter_url(url)):
        await update.message.reply_text(
            "⚠️ الرابط غير صالح. يرجى إرسال رابط Twitter/X صالح.\n"
            "مثال لرابط محادثة: https://twitter.com/i/spaces/1YqJDqDgBjExV\n"
            "مثال لرابط تغريدة: https://twitter.com/username/status/1234567890"
        )
        return
    
    # إرسال رسالة انتظار
    wait_message = await update.message.reply_text(
        "⏳ جاري تحليل الرابط وتحميل محادثة Twitter Spaces... قد تستغرق هذه العملية بضع دقائق."
    )
    
    try:
        # تحميل المحادثة
        audio_file = downloader.download_twitter_space(url)
        
        if not audio_file:
            await wait_message.edit_text(
                "❌ فشل في تحميل المحادثة. قد تكون المحادثة غير متاحة أو تم حذفها، أو قد لا يحتوي الرابط على محادثة Twitter Spaces."
            )
            return
        
        # التحقق من حجم الملف
        file_size = os.path.getsize(audio_file)
        if file_size > MAX_TELEGRAM_FILE_SIZE:
            await wait_message.edit_text(
                f"⚠️ حجم الملف ({file_size / (1024 * 1024):.2f} ميجابايت) أكبر من الحد الأقصى المسموح به (50 ميجابايت).\n"
                "جاري تقسيم الملف..."
            )
            # هنا يمكن إضافة منطق لتقسيم الملف أو ضغطه
            # لكن هذا خارج نطاق النسخة الأولية
            return
        
        # إرسال الملف الصوتي
        await wait_message.edit_text("✅ تم تحميل المحادثة بنجاح! جاري إرسال الملف الصوتي...")
        
        with open(audio_file, 'rb') as audio:
            await update.message.reply_audio(
                audio=audio,
                caption="🎙️ محادثة Twitter Spaces",
                filename=os.path.basename(audio_file),
                performer="Twitter Spaces",
                title="Twitter Space Recording"
            )
        
        # حذف رسالة الانتظار
        await wait_message.delete()
        
        # حذف الملف المؤقت
        try:
            os.remove(audio_file)
        except Exception as e:
            logger.error(f"خطأ في حذف الملف المؤقت: {e}")
    
    except Exception as e:
        logger.error(f"خطأ في معالجة رابط المحادثة: {e}")
        await wait_message.edit_text(
            "❌ حدث خطأ أثناء معالجة المحادثة. يرجى المحاولة مرة أخرى لاحقًا."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    التعامل مع الأخطاء
    """
    logger.error(f"حدث خطأ: {context.error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى لاحقًا."
            )
    except Exception as e:
        logger.error(f"خطأ في معالج الأخطاء: {e}")

def main() -> None:
    """
    تشغيل البوت
    """
    # إنشاء تطبيق البوت
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # إضافة معالج الرسائل
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_space_url))
    
    # إضافة معالج الأخطاء
    application.add_error_handler(error_handler)
    
    # تشغيل البوت
    application.run_polling()
    
    logger.info("تم بدء تشغيل البوت")

if __name__ == '__main__':
    main()
