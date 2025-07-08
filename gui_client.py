import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QPushButton, QLabel, QLineEdit, QFileDialog, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from qwen2_5_VL_test import process_folder, process_image, draw_bbox

class ProcessingThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, folder_path, objects_list):
        super().__init__()
        self.folder_path = folder_path
        self.objects_list = objects_list

    def run(self):
        try:
            process_folder(self.folder_path, object_list=self.objects_list, txt_path='txt')
        except Exception as e:
            self.progress_signal.emit(f"错误: {str(e)}")
        finally:
            self.finished_signal.emit()

class MiningClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('数据集标注工具')
        self.setGeometry(300, 300, 800, 600)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建垂直布局
        layout = QVBoxLayout()
        
        # 创建文件夹选择部分
        folder_label = QLabel('选择图片文件夹:')
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        folder_button = QPushButton('浏览...')
        folder_button.clicked.connect(self.select_folder)
        
        # 创建物体输入部分
        objects_label = QLabel('输入需要标注的物体（用逗号分隔）:')
        self.objects_input = QLineEdit()
        self.objects_input.setPlaceholderText('例如: 冰人,火人,蓝色钻石,红色钻石')
        
        # 创建日志显示区域
        log_label = QLabel('运行日志:')
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        
        # 创建开始按钮
        self.start_button = QPushButton('开始处理')
        self.start_button.clicked.connect(self.start_processing)
        
        # 添加所有部件到布局
        layout.addWidget(folder_label)
        layout.addWidget(self.folder_path)
        layout.addWidget(folder_button)
        layout.addWidget(objects_label)
        layout.addWidget(self.objects_input)
        layout.addWidget(log_label)
        layout.addWidget(self.log_display)
        layout.addWidget(self.start_button)
        
        # 设置布局
        central_widget.setLayout(layout)
        
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择图片文件夹')
        if folder:
            self.folder_path.setText(folder)
            self.log_display.append(f'已选择文件夹: {folder}')
            
    def start_processing(self):
        folder = self.folder_path.text()
        objects = self.objects_input.text()
        
        if not folder:
            self.log_display.append('错误: 请选择图片文件夹')
            return
            
        if not objects:
            self.log_display.append('错误: 请输入需要标注的物体')
            return
        
        # 禁用开始按钮
        self.start_button.setEnabled(False)
        
        # 创建并启动处理线程
        self.processing_thread = ProcessingThread(folder, objects.split(','))
        self.processing_thread.progress_signal.connect(self.update_log)
        self.processing_thread.finished_signal.connect(self.processing_finished)
        self.processing_thread.start()
    
    def update_log(self, message):
        self.log_display.append(message)
        # 滚动到底部
        self.log_display.verticalScrollBar().setValue(
            self.log_display.verticalScrollBar().maximum()
        )
    
    def processing_finished(self):
        self.start_button.setEnabled(True)
        self.log_display.append("处理完成！")

def main():
    app = QApplication(sys.argv)
    ex = MiningClient()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main() 