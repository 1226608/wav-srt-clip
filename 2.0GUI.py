import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os,re,pysrt,time
from pydub import AudioSegment

class 窗口(QWidget):#定义了一个名为"窗口"的类，它继承自"QWidget"

    def __init__(self):#__init__方法是类的构造函数，当创建"窗口"对象时会被调用
        super().__init__()
        #窗口属性
        self.setFixedSize(QSize(400, 300))#窗口的大小
        self.setAttribute(Qt.WA_TranslucentBackground)#窗口背景设为透明
        self.setWindowFlags(Qt.FramelessWindowHint)#窗口设为无边框
        #按钮外观
        skin = 'background-color:rgb(192,192,192);border-radius:10px;border:4px groove gray;border-style:outset;'
        font = QFont("黑体", 12)

        self.label = QLabel("按照SRT分割WAV",self)
        self.label.setIndent(150)
        self.label.setFont(QFont('微软雅黑', 12))  # 设置标签字体
   
        self.import_wav_button = QPushButton("选择导入WAV文件", self)
        self.import_wav_button.clicked.connect(self.import_wav_file_path_button)
        self.import_wav_button.setGeometry(30, 50, 160, 40)#设置按钮位置和大小
        self.import_wav_button.setStyleSheet(skin)
        self.import_wav_button.setFont(font)

        self.import_srt_button = QPushButton("选择导入SRT文件", self)
        self.import_srt_button.clicked.connect(self.import_srt_file_path_button)
        self.import_srt_button.setGeometry(30, 130, 160, 40)#设置按钮位置和大小
        self.import_srt_button.setStyleSheet(skin)
        self.import_srt_button.setFont(font)

        self.export_button = QPushButton('选择导出文件夹', self)
        self.export_button.clicked.connect(self.export_folder_path_button)
        self.export_button.setGeometry(210, 90, 160, 40)#设置按钮位置和大小
        self.export_button.setStyleSheet(skin)
        self.export_button.setFont(font)

        self.start_button = QPushButton('开始处理', self)
        self.start_button.clicked.connect(self.start)
        self.start_button.setGeometry(130, 200, 160, 40)#设置按钮位置和大小
        self.start_button.setStyleSheet(skin)
        self.start_button.setFont(font)

        self.quit_button = QPushButton("X", self)
        self.quit_button.clicked.connect(self.quit)
        self.quit_button.setGeometry(350, 10, 40, 40)#设置按钮位置和大小
        self.quit_button.setStyleSheet(skin)
        self.quit_button.setFont(QFont("微软雅黑", 13))

    def import_wav_file_path_button(self):
        # 设置文件过滤器为WAV文件
        file_filter = "WAV Files (*.wav)"
        # 弹出文件选择对话框
        global import_wav_file_path
        import_wav_file_path, _ = QFileDialog.getOpenFileName(self, '选择WAV文件', '', file_filter)
        # 如果选择了文件，将文件路径打印出来
        if import_wav_file_path:
            print('选择了WAV文件的路径:', import_wav_file_path)

    def import_srt_file_path_button(self):
        # 设置文件过滤器为WAV文件
        file_filter = "SRT Files (*.srt)"
        # 弹出文件选择对话框
        global import_srt_file_path
        import_srt_file_path, _ = QFileDialog.getOpenFileName(self, '选择SRT文件', '', file_filter)
        # 如果选择了文件，将文件路径打印出来
        if import_srt_file_path:
            print('选择了WAV文件的路径:', import_srt_file_path)
            return import_srt_file_path

    def export_folder_path_button(self):
        # 弹出文件夹选择对话框
        global export_folder_path
        export_folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹', '/')
        # 如果选择了文件夹路径，将路径打印出来
        if export_folder_path:
            print('选择了文件夹的路径:', export_folder_path)
            return export_folder_path
    
    def start(self):
        try:
            if import_wav_file_path and import_srt_file_path and export_folder_path:
                if len(os.listdir(export_folder_path)) == 0:
                        srt_file_path = import_srt_file_path
                        input_file_path = import_wav_file_path
                        output_dir = export_folder_path
                        split_audio_by_srt(srt_file_path, input_file_path, output_dir)
                else:
                    QMessageBox.warning(self, '提示', '导出文件夹需要是空的', QMessageBox.Yes)
                    print('导出文件夹需要是空的')
            else:
                print("未选择")
        except NameError:
            print("未选择")
            QMessageBox.warning(self, '提示', '三个都需要选择', QMessageBox.Yes) 
    def quit(self):
        QApplication.quit()
    开始坐标 = None
    结束坐标 = None
    跟踪 = False
    #移动窗口
    def mouseMoveEvent(self, e: QMouseEvent):#鼠标移动
        self.结束坐标 = e.pos() - self.开始坐标
        self.move(self.pos() + self.结束坐标)

    def mousePressEvent(self, e: QMouseEvent):#鼠标按下
        if e.button() == Qt.LeftButton:
            self._跟踪 = True
            self.开始坐标 = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e: QMouseEvent):#鼠标松开
        if e.button() == Qt.LeftButton:
            self.跟踪 = False
            self.开始坐标 = None
            self.结束坐标 = None

    #窗口外观
    def paintEvent(self, event):#paintEvent方法是一个事件处理方法，在窗口需要重新绘制时会被调用
        painter = QPainter(self)#在这个方法中，创建了一个QPainter对象，用于进行绘制操作
        painter.setRenderHint(QPainter.Antialiasing)#设置了抗锯齿渲染
        roundedRect = self.rect()#通过drawRoundedRect方法绘制了一个圆角矩形
        painter.setBrush(QBrush(QColor(255, 255, 255, 255)))#使用setBrush设置了绘制的颜色和透明度
        painter.drawRoundedRect(roundedRect, 10, 10)#绘制了一个圆角矩形
def 运行():
    app = QApplication(sys.argv)#创建了一个QApplication对象，用于管理应用程序的事件循环
    窗口d = 窗口()#创建"窗口"对象
    窗口d.show()#显示"窗口"对象
    sys.exit(app.exec_())#启动了应用程序的事件循环
def clean_filename(filename):
    return re.sub(r'[^\w _-]+', '', filename).strip()
#开始处理
def split_audio_by_srt(srt_file_path, input_file_path, output_dir,):
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
    global elapsed_time
    elapsed_time = end_time - start_time
    print(f"处理完成,耗时: {elapsed_time}秒")
    QMessageBox.warning(None, '提示', f"处理完成,耗时: {elapsed_time}秒", QMessageBox.Yes) 

if __name__ == '__main__':#判断当前模块是否是主模块，并调用"运行"函数来启动应用程序
    运行()
