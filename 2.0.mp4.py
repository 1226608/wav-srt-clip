import os
import re
import pysrt
import time
from moviepy.editor import VideoFileClip

def clean_filename(filename):
    return re.sub(r'[^\w _-]+', '', filename).strip()

def split_video_by_srt(srt_file_path, input_file_path, output_dir):
    start_time = time.time()
    video = VideoFileClip(input_file_path)
    subs = pysrt.open(srt_file_path)
    os.makedirs(output_dir, exist_ok=True)

    for sub in subs:
        start_time_sub = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) + sub.start.milliseconds / 1000
        end_time_sub = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) + sub.end.milliseconds / 1000
        segment = video.subclip(start_time_sub, end_time_sub)
        output_filename = clean_filename(f'{sub.index}_{sub.text}') + '.mp4'
        output_path = os.path.join(output_dir, output_filename)
        segment.write_videofile(output_path, codec="libx264", audio_codec="aac")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"处理完成，耗时: {elapsed_time}秒")

srt_file_path = "字幕.srt"
input_file_path = "视频.mp4"
output_dir = "导出"
split_video_by_srt(srt_file_path, input_file_path, output_dir)
