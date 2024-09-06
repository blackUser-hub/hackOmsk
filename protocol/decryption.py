import pandas as pd
from datetime import timedelta
from docx import *

df = pd.read_csv("output.csv", sep=',', encoding='utf-8')

def format_time(seconds):
    td = timedelta(seconds=seconds)
    minutes, seconds = divmod(td.total_seconds(), 60)
    return f"{int(minutes):02}:{int(seconds):02}"


doc = Document("decryption.docx")
formatted_texts = []
current_speaker_id = -1
for _, row in df.iterrows():
    speaker_id = int(row['speaker'].replace("SPEAKER_0", "")) + 1
    speaker = f"Спикер {speaker_id}:"
    start_time = format_time(row['start'])
    end_time = format_time(row['end'])
    if speaker_id != current_speaker_id:
        formatted_texts.append(f"{speaker}\n({start_time} - {end_time}) {row['text']}")
        current_speaker_id = speaker_id
    else:
        formatted_texts.append(f"({start_time} - {end_time}) {row['text']}")

for line in formatted_texts:
    doc.add_paragraph(line)
doc.save("decryption.docx")