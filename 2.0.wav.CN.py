import os,re,pysrt,time
from pydub import AudioSegment

def 清理文件名(文件名):
    return re.sub(r'[^\w _-]+', '', 文件名).strip()

def 根据字幕分割音频(字幕文件路径, 输入文件路径, 输出目录):
    开始时间 = time.time()
    音频 = AudioSegment.from_wav(输入文件路径)
    字幕 = pysrt.open(字幕文件路径)
    os.makedirs(输出目录, exist_ok=True)

    for 每条字幕 in 字幕:
        开始时间 = (每条字幕.start.hours * 3600 + 每条字幕.start.minutes * 60 + 每条字幕.start.seconds) * 1000 + 每条字幕.start.milliseconds
        结束时间 = (每条字幕.end.hours * 3600 + 每条字幕.end.minutes * 60 + 每条字幕.end.seconds) * 1000 + 每条字幕.end.milliseconds
        片段 = 音频[开始时间:结束时间]
        输出文件名 = 清理文件名(f'{每条字幕.index}_{每条字幕.text}') + '.wav'
        输出路径 = os.path.join(输出目录, 输出文件名)
        片段.export(输出路径, format="wav")

    结束时间 = time.time()
    耗时 = 结束时间 - 开始时间
    print(f"处理完成,耗时: {耗时}秒")

字幕文件路径 = "都.srt"
输入文件路径 = "都.wav"
输出目录 = "存"
根据字幕分割音频(字幕文件路径, 输入文件路径, 输出目录)
