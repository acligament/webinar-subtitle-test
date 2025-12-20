import subprocess
import os

print("burn.py started")
print("CWD:", os.getcwd())
print("Files:", os.listdir("."))

if not os.path.exists("audio_ja.srt"):
    raise FileNotFoundError("audio_ja.srt not found before burning")

subtitle = os.path.abspath("audio_ja.srt")

subprocess.run([
    "ffmpeg",
    "-i", "webinar.mp4",
    "-vf",
    f"subtitles={subtitle}:force_style='subtitles=audio_ja.srt:force_style='FontName=IPAexGothic,FontScale=0.6,Outline=1,Alignment=2,MarginV=20'",
    "-c:a", "copy",
    "webinar_subtitled_test.mp4"
], check=True)

print("Burn finished successfully")
