import os
import re
from openai import OpenAI

client = OpenAI()  # ← api_key は env から自動で読む

def translate_text(text):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Translate the following English subtitles into natural Japanese "
                    "suitable for a scientific webinar. "
                    "Keep technical terms in English where appropriate."
                )
            },
            {
                "role": "user",
                "content": text
            }
        ],
    )

    return response.output_text.strip()

with open("audio.srt", "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
buffer = []

for line in lines:
    if re.match(r"^\d+$", line) or "-->" in line or line.strip() == "":
        if buffer:
            ja = translate_text(" ".join(buffer))
            out.append(ja + "\n")
            buffer = []
        out.append(line)
    else:
        buffer.append(line.strip())

with open("audio_ja.srt", "w", encoding="utf-8") as f:
    f.writelines(out)
