import pysrt
import datetime
from pydub import AudioSegment

def parse_srt_file(srt_file_path):
    subs = pysrt.open(srt_file_path)
    sentences = []
    for sub in subs:
        start_time = sub.start.to_time()
        end_time = sub.end.to_time()
        content = sub.text_without_tags.strip()
        sentences.append((start_time, end_time, content))
    return sentences

def convert_to_milliseconds(time):
    hours = time.hour * 3600000
    minutes = time.minute * 60000
    seconds = time.second * 1000
    milliseconds = time.microsecond // 1000
    return hours + minutes + seconds + milliseconds

def cut_audio(input_file_path, output_file_path, start_time, end_time):
    audio = AudioSegment.from_wav(input_file_path)
    start_time_ms = convert_to_milliseconds(start_time)
    end_time_ms = convert_to_milliseconds(end_time)
    sentence_audio = audio[start_time_ms:end_time_ms]
    sentence_audio.export(output_file_path, format="wav")

def main():
    srt_file_path = "都.srt"
    input_file_path = "都.wav"
    output_dir = "存"

    sentences = parse_srt_file(srt_file_path)

    for i, (start_time, end_time, content) in enumerate(sentences):
        output_file_path = f"{output_dir}/{content}.wav"
        cut_audio(input_file_path, output_file_path, start_time, end_time)
        print(f"Saved sentence {i}: {output_file_path}")

if __name__ == "__main__":
    main()
