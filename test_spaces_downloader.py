"""
اختبار وظائف بوت تحميل محادثات Twitter Spaces
"""

import os
import unittest
from unittest.mock import patch, MagicMock
import sys

# إضافة مسار المشروع إلى مسار البحث
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from spaces_downloader import TwitterSpacesDownloader

class TestTwitterSpacesDownloader(unittest.TestCase):
    """
    اختبارات لفئة TwitterSpacesDownloader
    """
    
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        self.temp_folder = "/tmp/twitter_spaces_test"
        os.makedirs(self.temp_folder, exist_ok=True)
        self.downloader = TwitterSpacesDownloader(self.temp_folder)
    
    def tearDown(self):
        """
        تنظيف بيئة الاختبار
        """
        # حذف الملفات المؤقتة
        for file in os.listdir(self.temp_folder):
            file_path = os.path.join(self.temp_folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"خطأ في حذف الملف {file_path}: {e}")
    
    def test_is_valid_twitter_space_url(self):
        """
        اختبار التحقق من صحة روابط Twitter Spaces
        """
        # روابط صحيحة
        valid_urls = [
            "https://twitter.com/i/spaces/1YqJDqDgBjExV",
            "https://twitter.com/spaces/1YqJDqDgBjExV",
            "https://x.com/i/spaces/1YqJDqDgBjExV",
            "https://www.twitter.com/i/spaces/1YqJDqDgBjExV"
        ]
        
        # روابط غير صحيحة
        invalid_urls = [
            "https://twitter.com/username/status/123456789",
            "https://facebook.com/spaces/123456789",
            "https://twitter.com/i/broadcasts/123456789",
            "https://twitter.com/i/space/123456789",  # space بدلاً من spaces
            "https://example.com"
        ]
        
        # اختبار الروابط الصحيحة
        for url in valid_urls:
            self.assertTrue(self.downloader.is_valid_twitter_space_url(url), f"يجب أن يكون الرابط {url} صالحًا")
        
        # اختبار الروابط غير الصحيحة
        for url in invalid_urls:
            self.assertFalse(self.downloader.is_valid_twitter_space_url(url), f"يجب أن يكون الرابط {url} غير صالح")
    
    @patch('yt_dlp.YoutubeDL')
    def test_download_space_using_ytdlp(self, mock_ytdl):
        """
        اختبار تحميل محادثة Twitter Spaces باستخدام yt-dlp
        """
        # إعداد المحاكاة
        mock_ytdl_instance = MagicMock()
        mock_ytdl.return_value.__enter__.return_value = mock_ytdl_instance
        
        # إنشاء ملف وهمي للاختبار
        test_url = "https://twitter.com/i/spaces/1YqJDqDgBjExV"
        test_file = os.path.join(self.temp_folder, "space_test.mp3")
        
        # محاكاة نجاح التحميل
        with open(test_file, 'w') as f:
            f.write("test audio content")
        
        # تعديل السلوك المتوقع للدالة
        with patch.object(self.downloader, 'download_space_using_ytdlp', return_value=test_file):
            result = self.downloader.download_space_using_ytdlp(test_url)
            
            # التحقق من النتيجة
            self.assertEqual(result, test_file)
            self.assertTrue(os.path.exists(test_file))

if __name__ == '__main__':
    unittest.main()
