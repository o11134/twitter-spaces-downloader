"""
سكريبت تحميل محادثات Twitter Spaces
"""

import os
import re
import uuid
import requests
from urllib.parse import urlparse
import yt_dlp

def is_valid_twitter_url(url):
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

def is_twitter_space_url(url):
    """
    التحقق مما إذا كان الرابط هو رابط محادثة Twitter Spaces
    
    المعلمات:
        url (str): الرابط المراد التحقق منه
        
    العائد:
        bool: True إذا كان الرابط لمحادثة Spaces، False خلاف ذلك
    """
    # التحقق من أن الرابط هو رابط Twitter
    if not is_valid_twitter_url(url):
        return False
    
    # التحقق من أن الرابط يحتوي على "spaces" في المسار
    parsed_url = urlparse(url)
    return '/spaces/' in parsed_url.path

def is_twitter_status_url(url):
    """
    التحقق مما إذا كان الرابط هو رابط تغريدة Twitter
    
    المعلمات:
        url (str): الرابط المراد التحقق منه
        
    العائد:
        bool: True إذا كان الرابط لتغريدة، False خلاف ذلك
    """
    # التحقق من أن الرابط هو رابط Twitter
    if not is_valid_twitter_url(url):
        return False
    
    # التحقق من أن الرابط يحتوي على "status" في المسار
    parsed_url = urlparse(url)
    return '/status/' in parsed_url.path

def download_twitter_space(url, output_dir=None):
    """
    تحميل محادثة Twitter Spaces من رابط تغريدة أو رابط محادثة مباشرة
    
    المعلمات:
        url (str): رابط التغريدة أو المحادثة
        output_dir (str): مجلد الإخراج (اختياري)
        
    العائد:
        str: مسار الملف الصوتي المحمل أو None في حالة الفشل
    """
    try:
        # إنشاء مجلد الإخراج إذا لم يكن موجوداً
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "downloads")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # إنشاء اسم ملف فريد
        output_filename = os.path.join(output_dir, f"space_{uuid.uuid4().hex}.mp3")
        
        print(f"جاري تحميل المحادثة من الرابط: {url}")
        print(f"سيتم حفظ الملف في: {output_filename}")
        
        # إعداد خيارات yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_filename,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True
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
        
        # البحث عن أي ملف تم إنشاؤه في المجلد
        for file in os.listdir(output_dir):
            if file.startswith("space_") and file.endswith(".mp3"):
                return os.path.join(output_dir, file)
                
        return None
    except Exception as e:
        print(f"خطأ في تحميل المحادثة: {e}")
        return None

# اختبار الوظيفة إذا تم تشغيل الملف مباشرة
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        
        audio_file = download_twitter_space(url, output_dir)
        
        if audio_file:
            print(f"تم تحميل المحادثة بنجاح: {audio_file}")
        else:
            print("فشل في تحميل المحادثة")
    else:
        print("الرجاء تقديم رابط محادثة Twitter Spaces")