#!/usr/bin/env python3
"""
سكريبت مستقل لتحميل محادثات Twitter Spaces من روابط التغريدات
"""

import os
import sys
import argparse
import uuid
import yt_dlp

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
            'quiet': False,
            'no_warnings': False,
            'verbose': True
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

def main():
    """
    الدالة الرئيسية للسكريبت
    """
    parser = argparse.ArgumentParser(description='تحميل محادثات Twitter Spaces من روابط التغريدات')
    parser.add_argument('url', help='رابط التغريدة أو المحادثة')
    parser.add_argument('-o', '--output-dir', help='مجلد الإخراج (اختياري)')
    
    args = parser.parse_args()
    
    audio_file = download_twitter_space(args.url, args.output_dir)
    
    if audio_file:
        print(f"تم تحميل المحادثة بنجاح: {audio_file}")
        return 0
    else:
        print("فشل في تحميل المحادثة")
        return 1

if __name__ == "__main__":
    sys.exit(main())
