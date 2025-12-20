import subprocess

VIDEO_URL = "https://www.dhs.gov/xlibrary/videos/18_0627_st_Tech_Talk_TPP.mp4"

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # 1) Download MP4
    run([
        "ffmpeg", "-y",
        "-i", VIDEO_URL,
        "-c", "copy",
        "webinar.mp4"
    ])

    # 2) Extract audio
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

    # 3) Whisper transcription
    run([
        "whisper", "audio.wav",
        "--language", "en",
        "--task", "transcribe",
        "--model", "small",
        "--output_format", "srt",
        "--output_dir", "."
    ])

if __name__ == "__main__":
    main()
