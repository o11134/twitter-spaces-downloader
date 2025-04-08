#!/bin/bash

# سكريبت تشغيل بوت تيليجرام لتحميل محادثات Twitter Spaces الصوتية

cd "$(dirname "$0")"
cd src

echo "جاري تشغيل بوت تيليجرام لتحميل محادثات Twitter Spaces..."
python3 bot.py
