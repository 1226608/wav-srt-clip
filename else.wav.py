导入操作系统
进口再
从pydub导入AudioSegment
导入pysrt

def  clean_filename (文件名) :
    回归礁 sub ( r'[^\w _-]+' , '' , 文件名)。条( )

def  split_audio_by_srt ( srt_file_path, input_file_path, output_dir ) :
    如果 不是操作系统。路径。存在（ srt_file_path ） 或 不存在os. 路径。存在（输入文件路径）：
        print ( "导入的WAV文件或SRT文件不存在" )
        返回

    音频=音频段。from_wav (输入文件路径)
    音频长度=长度（音频）
    subs = pysrt. 打开（ srt_文件路径）

    操作系统。makedirs （ output_dir，exist_ok = True ）

    对于子中的子：
        start_time = (子开始.小时* 3600 + 子 .开始.分钟* 60 + 子 .开始.秒) * 1000 + 子 . 开始 . 秒 ) * 1000 + 子 . 开始。毫秒
        end_time = (子结束时间小时* 3600 + 子结束时间分钟* 60 +子结束时间秒) * 1000 + 子结束时间 秒 ) * 1000 + 子结束时间 结束。毫秒

        如果开始时间 > 音频长度或结束时间 > 音频长度：
            print ( f"忽略副标题{ sub.index }因为其时间范围在音频的长度之外" )
            继续

        片段=音频[开始时间:结束时间]

        输出文件名 = clean_filename ( f' {子索引} _ {子文本} ' ) + '.wav'
        输出路径 = os. 路径。加入（输出目录，输出文件名）

        部分。导出（输出路径，格式= “wav” ）

#对文件路径和名称使用函数参数
srt_file_path = "都.srt"
input_file_path = "都.wav"
output_dir = "存"
split_audio_by_srt(srt_file_path, input_file_path, output_dir)
