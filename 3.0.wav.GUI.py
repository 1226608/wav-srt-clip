import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os,re,pysrt,time
from pydub import AudioSegment

class 窗口(QWidget):

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(660, 240))

        font = QFont("微软雅黑", 10)
        self.setFont(font)
        self.import_wav_button = QPushButton("一:选择导入WAV文件", self)
        self.import_wav_button.clicked.connect(self.import_wav_file_path_button)
        self.import_wav_button.setGeometry(10, 10, 200, 30)

        self.import_srt_button = QPushButton("二:选择导入SRT文件", self)
        self.import_srt_button.clicked.connect(self.import_srt_file_path_button)
        self.import_srt_button.setGeometry(230, 10, 200, 30)

        self.export_button = QPushButton('三:选择导出文件夹', self)
        self.export_button.clicked.connect(self.export_folder_path_button)
        self.export_button.setGeometry(450, 10, 200, 30)

        self.text_editbox = QLineEdit('你的自定义内容',self)
        self.text_editbox.setGeometry(230, 90, 200, 30)

        self.prefix_combobox = QComboBox(self)
        self.prefix_combobox.setGeometry(10, 50, 200, 30)
        self.prefix_combobox.addItem("将自定义文字设为开头")
        self.prefix_combobox.addItem("将序号设为开头")
        self.prefix_combobox.addItem("将字幕内容设为开头")
        self.prefix_combobox.addItem("不设置开头")

        self.middle_combobox = QComboBox(self)
        self.middle_combobox.setGeometry(230, 50, 200, 30)
        self.middle_combobox.addItem("将自定义文字设为中间")
        self.middle_combobox.addItem("将序号设为中间")
        self.middle_combobox.addItem("将字幕内容设为中间")
        self.middle_combobox.addItem("不设置中间")

        self.suffix_combobox = QComboBox(self)
        self.suffix_combobox.setGeometry(450, 50, 200, 30)
        self.suffix_combobox.addItem("将自定义文字设为结尾")
        self.suffix_combobox.addItem("将序号设为结尾")
        self.suffix_combobox.addItem("将字幕内容设为结尾")
        self.suffix_combobox.addItem("不设置结尾")

        self.start_button = QPushButton('开始处理', self)
        self.start_button.clicked.connect(self.start)
        self.start_button.setGeometry(450, 90, 200, 30)#设置按钮位置和大小

    def import_wav_file_path_button(self):
        file_filter = "WAV Files (*.wav)"
        global import_wav_file_path
        import_wav_file_path, _ = QFileDialog.getOpenFileName(self, '选择WAV文件', '', file_filter)
        if import_wav_file_path:
            print('选择了WAV文件的路径:', import_wav_file_path)

    def import_srt_file_path_button(self):
        file_filter = "SRT Files (*.srt)"
        global import_srt_file_path
        import_srt_file_path, _ = QFileDialog.getOpenFileName(self, '选择SRT文件', '', file_filter)
        if import_srt_file_path:
            print('选择了WAV文件的路径:', import_srt_file_path)
            return import_srt_file_path

    def export_folder_path_button(self):
        global export_folder_path
        export_folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹', '/')
        if export_folder_path:
            print('选择了文件夹的路径:', export_folder_path)
            return export_folder_path

    def start(self):
        try:
            if import_wav_file_path and import_srt_file_path and export_folder_path:
                prefix_index = self.prefix_combobox.currentIndex()
                middle_index = self.middle_combobox.currentIndex()
                suffix_index = self.suffix_combobox.currentIndex()
                custom_text = self.text_editbox.text()

                if prefix_index == 3 and middle_index == 3 and suffix_index == 3:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return
                elif prefix_index == 0 and middle_index == 3 and suffix_index == 3:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return
                elif prefix_index == 0 and middle_index == 0 and suffix_index == 3:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return
                elif prefix_index == 0 and middle_index == 0 and suffix_index == 0:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return
                elif prefix_index == 3 and middle_index == 0 and suffix_index == 0:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return
                elif prefix_index == 3 and middle_index == 3 and suffix_index == 0:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return
                elif prefix_index == 3 and middle_index == 0 and suffix_index == 3:
                    QMessageBox.warning(self, '警告', '不允许的组合', QMessageBox.Yes)
                    return

                if len(os.listdir(export_folder_path)) == 0:
                        srt_file_path = import_srt_file_path
                        input_file_path = import_wav_file_path
                        output_dir = export_folder_path
                        split_audio_by_srt(srt_file_path, input_file_path, output_dir, prefix_index, middle_index, suffix_index, custom_text)
                else:
                    QMessageBox.warning(self, '提示', '导出文件夹需要是空的', QMessageBox.Yes)
                    print('导出文件夹需要是空的')
            else:
                print("未选择")
        except NameError:
            print("未选择")
            QMessageBox.warning(self, '提示', '三个都需要选择', QMessageBox.Yes)

def 运行():
    app = QApplication(sys.argv)
    窗口d = 窗口()
    窗口d.show()
    sys.exit(app.exec_())

def clean_filename(filename):
    filename = re.sub(r'_+', '_', filename)
    if filename.startswith('_'):
        filename = filename[1:]
    if filename.endswith('_'):
        filename = filename[:-1]
    return filename

#开始处理
def split_audio_by_srt(srt_file_path, input_file_path, output_dir, prefix_index, middle_index, suffix_index, custom_text):
    start_time = time.time()
    audio = AudioSegment.from_wav(input_file_path)
    subs = pysrt.open(srt_file_path)
    os.makedirs(output_dir, exist_ok=True)

    for sub in subs:
        start_time_sub = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
        end_time_sub = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
        segment = audio[start_time_sub:end_time_sub]

        prefix = get_filename_prefix(sub, prefix_index, custom_text)
        middle = get_filename_middle(sub, middle_index, custom_text)
        suffix = get_filename_suffix(sub, suffix_index, custom_text)

        output_filename = clean_filename(f"{prefix}_{middle}_{suffix}") + ".wav"
        output_path = os.path.join(output_dir, output_filename)
        segment.export(output_path, format="wav")

    end_time = time.time()
    global elapsed_time
    elapsed_time = end_time - start_time
    print(f"处理完成,耗时: {elapsed_time}秒")
    QMessageBox.warning(None, '提示', f"处理完成,耗时: {elapsed_time}秒", QMessageBox.Yes)

def get_filename_prefix(sub, index, custom_text):
    if index == 0:
        return custom_text
    elif index == 1:
        return str(sub.index)
    elif index == 2:
        return sub.text
    else:
        return ""

def get_filename_middle(sub, index, custom_text):
    if index == 0:
        return custom_text
    elif index == 1:
        return str(sub.index)
    elif index == 2:
        return sub.text
    else:
        return ""

def get_filename_suffix(sub, index, custom_text):
    if index == 0:
        return custom_text
    elif index == 1:
        return str(sub.index)
    elif index == 2:
        return sub.text
    else:
        return ""

if __name__ == '__main__':
    运行()