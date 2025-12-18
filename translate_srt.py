from openai import OpenAI
import re

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def translate_text(text):
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Translate the following English subtitles into natural Japanese for a scientific webinar."},
            {"role": "user", "content": text}
        ]
    )
    return resp.choices[0].message.content.strip()

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
