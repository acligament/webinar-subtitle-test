import subprocess

YOUTUBE_URL = "https://www.youtube.com/watch?v=4CO8d2NyfaU"

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # 1) Download audio
    run([
        "yt-dlp", "-x", "--audio-format", "mp3",
        "-o", "audio.%(ext)s", YOUTUBE_URL
    ])

    # 2) Convert audio for Whisper
    run([
        "ffmpeg",
        "-t", "300",          # ← ここがポイント（300秒 = 5分）
        "-i", "audio.mp3",
        "-ac", "1",
        "-ar", "16000",
        "audio.wav",
        "-y"
    ])

    # 3) Transcribe with Whisper (SRT)
    run([
        "whisper", "audio.wav",
        "--language", "ja",
        "--task", "transcribe",
        "--model", "small",
        "--output_format", "srt",
        "--output_dir", "."
    ])

    # 4) Download video
    run([
        "yt-dlp", "-f", "mp4",
        "-o", "webinar.mp4", YOUTUBE_URL
    ])

    # 5) Burn subtitles into video
    run([
        "ffmpeg", "-i", "webinar.mp4",
        "-vf",
        "subtitles=audio.srt:force_style='FontName=IPAGothic,FontSize=26,Outline=1,Alignment=2,MarginV=60'",
        "-c:a", "copy",
        "webinar_subtitled_test.mp4"
    ])

if __name__ == "__main__":
    main()
