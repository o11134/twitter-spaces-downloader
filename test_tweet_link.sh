#!/bin/bash

# سكريبت اختبار بوت تيليجرام لتحميل محادثات Twitter Spaces الصوتية

cd "$(dirname "$0")"

echo "جاري اختبار تحميل محادثة Twitter Spaces من رابط تغريدة..."
python3 -c "
from src.spaces_downloader import TwitterSpacesDownloader
from src.config import TEMP_FOLDER

downloader = TwitterSpacesDownloader(TEMP_FOLDER)
test_url = 'https://x.com/dbasdosari1/status/1908973036621144202'
print(f'اختبار الرابط: {test_url}')
print(f'هل الرابط صالح لـ Twitter: {downloader.is_valid_twitter_url(test_url)}')
print(f'هل الرابط هو رابط تغريدة: {downloader.is_twitter_status_url(test_url)}')
print('جاري محاولة تحميل المحادثة...')
audio_file = downloader.download_twitter_space(test_url)
if audio_file:
    print(f'تم تحميل المحادثة بنجاح: {audio_file}')
else:
    print('فشل في تحميل المحادثة')
"
