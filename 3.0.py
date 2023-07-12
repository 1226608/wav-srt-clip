import os
import re
from pydub import AudioSegment
import pysrt

def clean_filename(filename):
    return re.sub(r'[^\w _-]+', '', filename).strip()

def split_audio_by_srt(srt_file_path, input_file_path, output_dir):
    if not os.path.exists(srt_file_path) or not os.path.exists(input_file_path):
        print("导入的WAV文件或SRT文件不存在")
        return

    audio = AudioSegment.from_wav(input_file_path)
    audio_length = len(audio)
    subs = pysrt.open(srt_file_path)

    os.makedirs(output_dir, exist_ok=True)

    for sub in subs:
        start_time = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds

        if start_time > audio_length or end_time > audio_length:
            print(f"忽略副标题 {sub.index} 因为其时间范围在音频的长度之外")
            continue

        segment = audio[start_time:end_time]

        output_filename = clean_filename(f'{sub.index}_{sub.text}') + '.wav'
        output_path = os.path.join(output_dir, output_filename)

        segment.export(output_path, format="wav")

#对文件路径和名称使用函数参数
srt_file_path = "都.srt"
input_file_path = "都.wav"
output_dir = "存"
split_audio_by_srt(srt_file_path, input_file_path, output_dir)
