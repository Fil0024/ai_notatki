import os
import sys
from yt_dlp import YoutubeDL
import whisper
from utils import get_root_path

def download_audio_from_youtube(url: str) -> str:
    root = get_root_path()
    audio_dir = os.path.join(root, "audio")
    os.makedirs(audio_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(audio_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info.get('id')
    mp3_path = os.path.join(audio_dir, f"{video_id}.mp3")
    return mp3_path


def transcribe_audio_local(mp3_path: str, model_name: str = "turbo") -> str:
    root = get_root_path()
    out_dir = os.path.join(root, "transcriptions")
    os.makedirs(out_dir, exist_ok=True)

    base = os.path.splitext(os.path.basename(mp3_path))[0]
    txt_path = os.path.join(out_dir, f"{base}.txt")

    model = whisper.load_model(model_name)
    result = model.transcribe(mp3_path)
    text = result.get('text', '').strip()

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return txt_path


if __name__ == "__main__":

    url = "https://www.youtube.com/watch?v=x7-1-JCLEeI&ab_channel=JakubUrbanik"
    model_name = "turbo"

    print("Pobieranie audio z YouTube...")
    audio_file = download_audio_from_youtube(url)
    print(f"Pobrano audio do: {audio_file}")

    print(f"Rozpoczynam transkrypcję lokalną modelem '{model_name}'...")
    txt_file = transcribe_audio_local(audio_file, model_name)
    print(f"Transkrypcja zapisana do: {txt_file}")