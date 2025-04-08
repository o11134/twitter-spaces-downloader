import os
import uuid
import json
from flask import Flask, render_template, request, jsonify, send_from_directory, Response, url_for
from werkzeug.utils import secure_filename
import time

app = Flask(__name__, static_folder='static')

# تكوين المجلدات
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'downloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 ميجابايت كحد أقصى

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# معالجة طلب التحميل
@app.route('/download', methods=['POST'])
def download():
    if request.is_json:
        data = request.get_json()
        url = data.get('url')
    else:
        url = request.form.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'الرجاء إدخال رابط صالح'})
    
    # التحقق من صحة الرابط
    if not ('twitter.com' in url or 'x.com' in url):
        return jsonify({'success': False, 'error': 'الرجاء إدخال رابط Twitter/X صالح'})
    
    try:
        # استدعاء وظيفة تحميل محادثة Twitter Spaces
        from twitter_spaces_downloader import download_twitter_space
        
        # تحميل المحادثة
        audio_file = download_twitter_space(url, UPLOAD_FOLDER)
        
        if not audio_file:
            return jsonify({'success': False, 'error': 'فشل في تحميل المحادثة. قد تكون المحادثة غير متاحة أو تم حذفها.'})
        
        # إنشاء رابط التحميل
        filename = os.path.basename(audio_file)
        download_url = f'/download_file/{filename}'
        
        # التأكد من وجود الملف وحجمه
        file_size = os.path.getsize(audio_file)
        
        return jsonify({
            'success': True,
            'download_url': download_url,
            'filename': filename,
            'file_size': file_size
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'حدث خطأ: {str(e)}'})

# تحميل الملف
@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        # التأكد من وجود الملف
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'الملف غير موجود'}), 404
            
        # إرسال الملف مع تعيين نوع المحتوى بشكل صريح
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename, 
            as_attachment=True,
            mimetype='audio/mpeg'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': f'حدث خطأ أثناء تحميل الملف: {str(e)}'}), 500

# مسار لتتبع تقدم التحميل (محاكاة)
@app.route('/progress/<task_id>')
def progress(task_id):
    def generate():
        progress = 0
        while progress < 100:
            progress += 10
            time.sleep(0.5)  # تسريع المحاكاة
            yield f"data: {json.dumps({'progress': progress})}\n\n"
        yield f"data: {json.dumps({'progress': 100, 'complete': True})}\n\n"
    return Response(generate(), mimetype='text/event-stream')

# تشغيل التطبيق
if __name__ == '__main__':
    # استخدام متغير البيئة PORT الذي توفره منصة Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
