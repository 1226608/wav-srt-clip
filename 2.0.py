import os,re,pysrt
from pydub import AudioSegment
def clean_filename(filename):
    return re.sub(r'[^\w _-]+', '', filename).strip()
def split_audio_by_srt(srt_file_path, input_file_path, output_dir):
    audio = AudioSegment.from_wav(input_file_path)
    subs = pysrt.open(srt_file_path)
    os.makedirs(output_dir, exist_ok=True)
    for sub in subs:
        start_time = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
        segment = audio[start_time:end_time]
        output_filename = clean_filename(f'{sub.index}_{sub.text}') + '.wav'
        output_path = os.path.join(output_dir, output_filename)
        segment.export(output_path, format="wav")
srt_file_path = "都.srt"
input_file_path = "都.wav"
output_dir = "存"
split_audio_by_srt(srt_file_path, input_file_path, output_dir)
