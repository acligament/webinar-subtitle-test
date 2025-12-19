import subprocess

VIDEO_URL = "https://www.dhs.gov/xlibrary/videos/18_0627_st_Tech_Talk_TPP.mp4"

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # 1) Download MP4 directly
    run([
        "ffmpeg", "-y",
        "-i", VIDEO_URL,
        "-c", "copy",
        "webinar.mp4"
    ])

    # 2) Extract audio (first 5 minutes for test)
    run([
        "ffmpeg",
        "-t", "300",
        "-i", "webinar.mp4",
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "audio.wav",
        "-y"
    ])

    # 3) Whisper transcription (English)
    run([
        "whisper", "audio.wav",
        "--language", "en",
        "--task", "transcribe",
        "--model", "small",
        "--output_format", "srt",
        "--output_dir", "."
    ])

    # 4) Burn subtitles into video
    run([
        "ffmpeg",
        "-i", "webinar.mp4",
        "-vf",
        "subtitles=audio_ja.srt:force_style='FontName=IPAexGothic,FontSize=18,FontScale=0.75,Outline=1,Alignment=2,MarginV=20'"
        "-c:a", "copy",
        "webinar_subtitled_test.mp4"
    ])

if __name__ == "__main__":
    main()
