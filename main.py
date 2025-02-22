# main.py
import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QFileDialog, QLabel, QTextEdit
)   
# 注意这里的导入，确保 src 目录在 Python 路径中
from src.train_model import train  # train() 函数需要支持接收 PDF 文件列表

class TrainingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF AI 训练与问答系统")
        self.setGeometry(100, 100, 600, 500)
        self.selected_files = []  # 存储选中的 PDF 文件路径
        self.initUI()
        
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        self.info_label = QLabel("选择 PDF 文件以进行训练：")
        layout.addWidget(self.info_label)
        
        self.select_button = QPushButton("选择 PDF 文件")
        self.select_button.clicked.connect(self.select_files)
        layout.addWidget(self.select_button)
        
        self.train_button = QPushButton("开始训练")
        self.train_button.clicked.connect(self.start_training)
        layout.addWidget(self.train_button)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
    
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择 PDF 文件", "", "PDF Files (*.pdf)"
        )
        if files:
            self.selected_files = files
            filenames = ", ".join(os.path.basename(f) for f in files)
            self.info_label.setText(f"已选文件: {filenames}")
            self.log_output.append("选中文件:\n" + "\n".join(files))
    
    def start_training(self):
        if not self.selected_files:
            self.log_output.append("未选择任何文件，请先选择 PDF 文件。")
            return
        
        self.log_output.append("开始训练...")
        # 将 self.selected_files 传入 train() 函数，
        # 你需要修改 train() 函数，让它接收 PDF 文件列表并执行相应预处理和训练
        try:
            train(self.selected_files)
            self.log_output.append("训练完成！")
        except Exception as e:
            self.log_output.append(f"训练出错: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = TrainingWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
