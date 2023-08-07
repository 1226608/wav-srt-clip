import os,re,pysrt,time
from pydub import AudioSegment

def clean_filename(filename):
    return re.sub(r'[^\w _-]+', '', filename).strip()

def split_audio_by_srt(srt_file_path, input_file_path, output_dir):
    start_time = time.time()
    audio = AudioSegment.from_wav(input_file_path)
    subs = pysrt.open(srt_file_path)
    os.makedirs(output_dir, exist_ok=True)

    for sub in subs:
        start_time_sub = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time_sub = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
        segment = audio[start_time_sub:end_time_sub]
        output_filename = clean_filename(f'{sub.index}_{sub.text}') + '.wav'
        output_path = os.path.join(output_dir, output_filename)
        segment.export(output_path, format="wav")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"处理完成,耗时: {elapsed_time}秒")

srt_file_path = "都.srt"
input_file_path = "都.wav"
output_dir = "存"
split_audio_by_srt(srt_file_path, input_file_path, output_dir)
