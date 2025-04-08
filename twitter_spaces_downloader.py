"""
سكريبت تحميل محادثات Twitter Spaces
"""

import os
import re
import uuid
import requests
from urllib.parse import urlparse
import yt_dlp
import json
import time

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
    return '/spaces/' in parsed_url.path or '/i/spaces/' in parsed_url.path

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

def extract_space_id_from_url(url):
    """
    استخراج معرف المحادثة من الرابط
    
    المعلمات:
        url (str): رابط المحادثة
        
    العائد:
        str: معرف المحادثة أو None في حالة الفشل
    """
    # للروابط المباشرة للمحادثات
    if is_twitter_space_url(url):
        match = re.search(r'/spaces/([^/?]+)', url)
        if match:
            return match.group(1)
    
    # للروابط من التغريدات
    elif is_twitter_status_url(url):
        # قد نحتاج إلى استخراج رابط المحادثة من التغريدة
        # هذا يتطلب تحليل محتوى التغريدة
        pass
    
    return None

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
        unique_id = uuid.uuid4().hex
        output_filename = os.path.join(output_dir, f"space_{unique_id}")
        
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
            'verbose': True,  # تفعيل وضع التفصيل للتشخيص
            'cookiefile': None,  # لا نحتاج إلى ملف كوكيز
            'extractor_args': {
                'twitter': {
                    'api_key': 'AIzaSyDCvp5MTJLUdtBYEKYWXJrlLzu1zuKM6Xw',
                }
            }
        }
        
        # تحميل المحادثة
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # طباعة معلومات التحميل للتشخيص
            print(f"معلومات التحميل: {json.dumps(info, indent=2, ensure_ascii=False)}")
        
        # البحث عن الملف المحمل
        mp3_filename = output_filename + '.mp3'
        if os.path.exists(mp3_filename):
            return mp3_filename
        
        # البحث عن أي ملف تم إنشاؤه في المجلد بناءً على المعرف الفريد
        for file in os.listdir(output_dir):
            if unique_id in file and file.endswith(".mp3"):
                return os.path.join(output_dir, file)
        
        # البحث عن أي ملف تم إنشاؤه حديثًا في المجلد
        files = [(os.path.join(output_dir, f), os.path.getmtime(os.path.join(output_dir, f))) 
                for f in os.listdir(output_dir) if f.endswith('.mp3')]
        
        if files:
            # ترتيب الملفات حسب وقت التعديل (الأحدث أولاً)
            files.sort(key=lambda x: x[1], reverse=True)
            # إرجاع أحدث ملف
            return files[0][0]
                
        return None
    except Exception as e:
        print(f"خطأ في تحميل المحادثة: {str(e)}")
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
