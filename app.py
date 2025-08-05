from flask import Flask, render_template, request
import yt_dlp
import os
from pathlib import Path

app = Flask(__name__)

# Get system's Downloads folder
downloads_path = str(Path.home() / "Downloads")

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return info.get('title', 'Video')

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        video_url = request.form['video_url']
        try:
            video_title = download_video(video_url)
            message = f'✅ "{video_title}" downloaded successfully to your Downloads folder!'
        except Exception as e:
            message = f'❌ Error: {str(e)}'
    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Enables network access on local LAN
