import导入pysrt
import导入日期时间
from从 pydub 导入 AudioSegmentimport AudioSegment

defdef parse_srt_file(srt_file_path):parse_srt_file(srt_file_path):
    subs = pysrt.open(srt_file_path)open(srt_file_path)
    句子=[][]
    对于子中的子：for sub in subs:
        开始时间 = sub.start.to_time()start.to_time()
        end_time = sub.end.to_time()end.to_time()
        内容 = sub.text_without_tags.strip()text_without_tags.strip()
        Sentences.append((开始时间、结束时间、内容))append((start_time, end_time, content))
    返回句子return sentences

defdef Convert_to_milliseconds(时间):convert_to_milliseconds(time):
    小时 = 时间.小时 * 3600000hour * 3600000
    分钟 = 时间.分钟 * 60000minute * 60000
    秒 = 时间.秒 * 1000second * 1000
    毫秒 = 时间.微秒 // 1000microsecond // 1000
    返回小时+分钟+秒+毫秒return hours + minutes + seconds + milliseconds

defdef cut_audio（输入文件路径，输出文件路径，开始时间，结束时间）：cut_audio(input_file_path, output_file_path, start_time, end_time):
    音频 = AudioSegment.from_wav(input_file_path)from_wav(input_file_path)
    start_time_ms = 转换_to_毫秒(start_time)convert_to_milliseconds(start_time)
    end_time_ms = 转换为毫秒(end_time)convert_to_milliseconds(end_time)
    句子音频=音频[开始时间_毫秒:结束时间_毫秒][start_time_ms:end_time_ms]
    Sentence_audio.export（输出文件路径，格式=“wav”）export(output_file_path, format="wav")

defdef main():main():
    srt_file_path = "都.srt""都.srt"
    input_file_path = "都.wav""都.wav"
    输出目录=“存”"存"

    句子 = parse_srt_file(srt_file_path)parse_srt_file(srt_file_path)

    对于 i，枚举（句子）中的（开始时间、结束时间、内容）：for i, (start_time, end_time, content) in enumerate(sentences):
        输出文件路径 = f"{输出目录}/{内容}.wav"f"{output_dir}/{content}.wav"
        cut_audio（输入文件路径，输出文件路径，开始时间，结束时间）cut_audio(input_file_path, output_file_path, start_time, end_time)
        print(f"已保存的句子 {i}: {output_file_path}")print(f"Saved sentence {i}: {output_file_path}")

if如果 __name__ == "__main__":"__main__":
    主要的（）main()
