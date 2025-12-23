import re
from openai import OpenAI

client = OpenAI()

# 入力（Whisperの出力）
INPUT = "audio.srt"
OUTPUT = "audio_ko.srt"

with open(INPUT, "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
buffer = []

def translate_text(text):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=(
            "Translate the following English subtitle into simple, clear korean "
            "that a Korean high school student can easily understand.\n"
            "Use short sentences, avoid difficult words, and explain concepts plainly.\n\n"
            f"{text}"
        )
    )
    return response.output_text.strip()

for line in lines:
    if re.match(r"^\d+$", line) or "-->" in line or line.strip() == "":
        if buffer:
            out.append(translate_text(" ".join(buffer)) + "\n")
            buffer = []
        out.append(line)
    else:
        buffer.append(line.strip())

# ループ終了後に残った字幕を処理
if buffer:
    out.append(translate_text(" ".join(buffer)) + "\n")

# ★ここが無いと絶対にファイルは作られません
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.writelines(out)

print("audio_ko.srt written") 

print("Files after translation:")
import os
print(os.listdir("."))
