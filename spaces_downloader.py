"""
سكريبت تحميل محادثات Twitter Spaces الصوتية
"""

import os
import re
import uuid
import requests
from bs4 import BeautifulSoup
import yt_dlp
import subprocess
from urllib.parse import urlparse

class TwitterSpacesDownloader:
    """
    فئة لتحميل محادثات Twitter Spaces الصوتية المسجلة
    """
    
    def __init__(self, temp_folder):
        """
        تهيئة المُنزِّل مع تحديد مجلد مؤقت لتخزين الملفات
        
        المعلمات:
            temp_folder (str): مسار المجلد المؤقت لتخزين الملفات الصوتية
        """
        self.temp_folder = temp_folder
        os.makedirs(temp_folder, exist_ok=True)
    
    def is_valid_twitter_url(self, url):
        """
        التحقق مما إذا كان الرابط هو رابط Twitter/X صالح
        
        المعلمات:
            url (str): الرابط المراد التحقق منه
            
        العائد:
            bool: True إذا كان الرابط صالحًا، False خلاف ذلك
        """
        # التحقق من أن الرابط هو رابط Twitter/X
        parsed_url = urlparse(url)
        return parsed_url.netloc in ['twitter.com', 'x.com', 'www.twitter.com', 'www.x.com']
    
    def is_valid_twitter_space_url(self, url):
        """
        التحقق مما إذا كان الرابط هو رابط صالح لمحادثة Twitter Spaces
        
        المعلمات:
            url (str): الرابط المراد التحقق منه
            
        العائد:
            bool: True إذا كان الرابط صالحًا، False خلاف ذلك
        """
        # التحقق من أن الرابط هو رابط Twitter
        if not self.is_valid_twitter_url(url):
            return False
        
        # التحقق من أن الرابط يحتوي على "spaces" في المسار
        parsed_url = urlparse(url)
        return '/spaces/' in parsed_url.path
    
    def is_twitter_status_url(self, url):
        """
        التحقق مما إذا كان الرابط هو رابط تغريدة Twitter
        
        المعلمات:
            url (str): الرابط المراد التحقق منه
            
        العائد:
            bool: True إذا كان الرابط لتغريدة، False خلاف ذلك
        """
        # التحقق من أن الرابط هو رابط Twitter
        if not self.is_valid_twitter_url(url):
            return False
        
        # التحقق من أن الرابط يحتوي على "status" في المسار
        parsed_url = urlparse(url)
        return '/status/' in parsed_url.path
    
    def extract_space_from_tweet(self, tweet_url):
        """
        محاولة استخراج رابط محادثة Twitter Spaces من تغريدة
        
        المعلمات:
            tweet_url (str): رابط التغريدة
            
        العائد:
            str: رابط محادثة Twitter Spaces أو None إذا لم يتم العثور عليه
        """
        try:
            # استخدام yt-dlp للتعامل مع رابط التغريدة مباشرة
            # yt-dlp قادر على استخراج روابط الوسائط المتعددة من التغريدات
            return tweet_url
        except Exception as e:
            print(f"خطأ في استخراج محادثة Spaces من التغريدة: {e}")
            return None
    
    def extract_m3u8_url_from_page(self, space_url):
        """
        استخراج رابط ملف m3u8 من صفحة محادثة Twitter Spaces
        
        المعلمات:
            space_url (str): رابط محادثة Twitter Spaces
            
        العائد:
            str: رابط ملف m3u8 أو None إذا لم يتم العثور عليه
        """
        try:
            # استخدام selenium أو أدوات المطور للحصول على رابط m3u8
            # هذه الطريقة تتطلب تفاعلًا مع المتصفح وهي معقدة للتنفيذ هنا
            # بدلاً من ذلك، سنستخدم yt-dlp مباشرة للتعامل مع هذه العملية
            return None
        except Exception as e:
            print(f"خطأ في استخراج رابط m3u8: {e}")
            return None
    
    def download_space_using_ytdlp(self, url):
        """
        تحميل محادثة Twitter Spaces باستخدام yt-dlp
        
        المعلمات:
            url (str): رابط محادثة Twitter Spaces أو تغريدة تحتوي على محادثة
            
        العائد:
            str: مسار الملف الصوتي المحمل أو None في حالة الفشل
        """
        try:
            # إنشاء اسم ملف فريد
            output_filename = os.path.join(self.temp_folder, f"space_{uuid.uuid4().hex}.mp3")
            
            # إعداد خيارات yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_filename,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': False,  # تغيير إلى False للحصول على معلومات التصحيح
                'no_warnings': False,  # تغيير إلى False للحصول على معلومات التصحيح
                'verbose': True  # إضافة للحصول على معلومات تفصيلية
            }
            
            # تحميل المحادثة
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # التحقق من وجود الملف
            if os.path.exists(output_filename):
                return output_filename
            
            # البحث عن الملف في حالة تغيير الامتداد
            mp3_filename = output_filename.replace('.mp3', '') + '.mp3'
            if os.path.exists(mp3_filename):
                return mp3_filename
            
            # البحث عن أي ملف تم إنشاؤه في المجلد المؤقت
            for file in os.listdir(self.temp_folder):
                if file.startswith("space_") and file.endswith(".mp3"):
                    return os.path.join(self.temp_folder, file)
                
            return None
        except Exception as e:
            print(f"خطأ في تحميل المحادثة: {e}")
            return None
    
    def download_space_using_m3u8(self, m3u8_url):
        """
        تحميل محادثة Twitter Spaces باستخدام رابط m3u8 مباشرة
        
        المعلمات:
            m3u8_url (str): رابط ملف m3u8
            
        العائد:
            str: مسار الملف الصوتي المحمل أو None في حالة الفشل
        """
        try:
            # إنشاء اسم ملف فريد
            output_filename = os.path.join(self.temp_folder, f"space_{uuid.uuid4().hex}")
            mp3_filename = output_filename + '.mp3'
            
            # استخدام ffmpeg لتحميل وتحويل الملف الصوتي
            command = [
                'ffmpeg', '-i', m3u8_url, 
                '-c:a', 'libmp3lame', '-q:a', '2', 
                mp3_filename
            ]
            
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # التحقق من وجود الملف
            if os.path.exists(mp3_filename):
                return mp3_filename
                
            return None
        except Exception as e:
            print(f"خطأ في تحميل المحادثة باستخدام m3u8: {e}")
            return None
    
    def download_twitter_space(self, url):
        """
        تحميل محادثة Twitter Spaces من الرابط المقدم
        
        المعلمات:
            url (str): رابط محادثة Twitter Spaces أو تغريدة تحتوي على محادثة
            
        العائد:
            str: مسار الملف الصوتي المحمل أو None في حالة الفشل
        """
        # التحقق من نوع الرابط
        if self.is_valid_twitter_space_url(url):
            print("الرابط هو رابط محادثة Twitter Spaces")
            space_url = url
        elif self.is_twitter_status_url(url):
            print("الرابط هو رابط تغريدة Twitter، جاري محاولة استخراج محادثة Spaces")
            space_url = self.extract_space_from_tweet(url)
            if not space_url:
                print("لم يتم العثور على محادثة Spaces في التغريدة")
                return None
        elif self.is_valid_twitter_url(url):
            print("الرابط هو رابط Twitter ولكنه ليس رابط محادثة Spaces أو تغريدة")
            # محاولة استخدام الرابط مباشرة
            space_url = url
        else:
            print("الرابط غير صالح")
            return None
        
        # محاولة تحميل المحادثة باستخدام yt-dlp مباشرة
        print(f"جاري محاولة تحميل المحادثة من الرابط: {space_url}")
        audio_file = self.download_space_using_ytdlp(space_url)
        if audio_file:
            return audio_file
        
        # إذا فشلت الطريقة الأولى، نحاول استخراج رابط m3u8
        m3u8_url = self.extract_m3u8_url_from_page(space_url)
        if m3u8_url:
            audio_file = self.download_space_using_m3u8(m3u8_url)
            if audio_file:
                return audio_file
        
        # إذا فشلت جميع المحاولات
        print("فشل في تحميل محادثة Twitter Spaces")
        return None

# اختبار الفئة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    from config import TEMP_FOLDER
    
    downloader = TwitterSpacesDownloader(TEMP_FOLDER)
    
    # اختبار التحميل باستخدام رابط محادثة Twitter Spaces
    test_url = "https://twitter.com/i/spaces/example"
    audio_file = downloader.download_twitter_space(test_url)
    
    if audio_file:
        print(f"تم تحميل المحادثة بنجاح: {audio_file}")
    else:
        print("فشل في تحميل المحادثة")
