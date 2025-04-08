# بوت تيليجرام لتحميل محادثات Twitter Spaces الصوتية

هذا المشروع عبارة عن بوت تيليجرام يساعدك في تحميل محادثات Twitter Spaces الصوتية المسجلة وتحويلها إلى ملفات MP3.

## المميزات

- تحميل محادثات Twitter Spaces المسجلة من خلال إرسال الرابط للبوت
- تحويل المحادثات إلى ملفات MP3 عالية الجودة
- واجهة سهلة الاستخدام عبر تيليجرام
- دعم للروابط من twitter.com و x.com

## المتطلبات

- Python 3.8 أو أحدث
- مكتبات Python: python-telegram-bot, yt-dlp, requests, beautifulsoup4, pydub
- FFmpeg

## التثبيت

1. قم بنسخ المستودع:
```
git clone https://github.com/yourusername/twitter_spaces_bot.git
cd twitter_spaces_bot
```

2. قم بتثبيت المكتبات المطلوبة:
```
pip install python-telegram-bot yt-dlp requests beautifulsoup4 pydub
```

3. قم بتثبيت FFmpeg:
   - على Ubuntu/Debian:
   ```
   sudo apt-get update && sudo apt-get install -y ffmpeg
   ```
   - على macOS (باستخدام Homebrew):
   ```
   brew install ffmpeg
   ```
   - على Windows: قم بتحميل FFmpeg من [الموقع الرسمي](https://ffmpeg.org/download.html) وإضافته إلى متغير PATH

4. قم بتعديل ملف `src/config.py` وإضافة توكن API الخاص ببوت التيليجرام الخاص بك:
```python
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

## كيفية الاستخدام

1. قم بتشغيل البوت:
```
./run_bot.sh
```
أو
```
cd src
python bot.py
```

2. افتح تيليجرام وابحث عن بوت التيليجرام الخاص بك

3. أرسل أمر `/start` لبدء استخدام البوت

4. أرسل رابط محادثة Twitter Spaces المسجلة إلى البوت

5. انتظر حتى يتم تحميل المحادثة ومعالجتها

6. سيقوم البوت بإرسال الملف الصوتي إليك

## الاستضافة

لاستضافة البوت على خادم، يمكنك استخدام إحدى الطرق التالية:

### استضافة على خادم VPS

1. قم بتثبيت المتطلبات على الخادم كما هو موضح في قسم التثبيت

2. استخدم أداة مثل `screen` أو `tmux` لتشغيل البوت في الخلفية:
```
screen -S twitter_spaces_bot
./run_bot.sh
```
ثم اضغط `Ctrl+A` ثم `D` للخروج من الجلسة مع استمرار تشغيل البوت

3. للعودة إلى الجلسة:
```
screen -r twitter_spaces_bot
```

### استخدام systemd (على أنظمة Linux)

1. قم بإنشاء ملف خدمة systemd:
```
sudo nano /etc/systemd/system/twitter-spaces-bot.service
```

2. أضف المحتوى التالي (قم بتعديل المسارات حسب الحاجة):
```
[Unit]
Description=Twitter Spaces Telegram Bot
After=network.target

[Service]
User=yourusername
WorkingDirectory=/path/to/twitter_spaces_bot
ExecStart=/usr/bin/python3 /path/to/twitter_spaces_bot/src/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. قم بتفعيل وتشغيل الخدمة:
```
sudo systemctl enable twitter-spaces-bot.service
sudo systemctl start twitter-spaces-bot.service
```

4. للتحقق من حالة البوت:
```
sudo systemctl status twitter-spaces-bot.service
```

## هيكل المشروع

```
twitter_spaces_bot/
├── src/
│   ├── bot.py                  # البوت الرئيسي
│   ├── spaces_downloader.py    # سكريبت تحميل محادثات Twitter Spaces
│   └── config.py               # ملف التكوين
├── tests/
│   └── test_spaces_downloader.py  # اختبارات
├── temp/                       # مجلد مؤقت لتخزين الملفات الصوتية
├── research_notes.md           # ملاحظات البحث
├── todo.md                     # قائمة المهام
├── run_bot.sh                  # سكريبت تشغيل البوت
└── README.md                   # هذا الملف
```

## الترخيص

هذا المشروع مرخص تحت رخصة MIT. انظر ملف LICENSE للمزيد من التفاصيل.

## المساهمة

المساهمات مرحب بها! يرجى إرسال طلب سحب أو فتح مشكلة للمناقشة.

## ملاحظات

- يرجى استخدام هذا البوت بمسؤولية واحترام حقوق الملكية الفكرية
- قد تتغير واجهة برمجة تطبيقات Twitter في المستقبل، مما قد يتطلب تحديث البوت
- هذا البوت مخصص للمحادثات المسجلة فقط ولا يمكنه تحميل المحادثات المباشرة
