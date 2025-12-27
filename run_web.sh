#!/bin/bash

# سكريپت تشغيل تطبيق الويب لتحميل محادثات Twitter Spaces الصوتية

cd "$(dirname "$0")"

echo "جاري تشغيل تطبيق الويب لتحميل محادثات Twitter Spaces..."
python3 app.py
