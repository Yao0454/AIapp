# src/gui/main_window.py
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLabel
from pdf_parser import parse_pdf

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 问答系统")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        self.loadButton = QPushButton("加载 PDF 文件")
        self.loadButton.clicked.connect(self.load_pdf)
        self.layout.addWidget(self.loadButton)

        self.questionLabel = QLabel("输入问题:")
        self.layout.addWidget(self.questionLabel)

        self.questionEdit = QTextEdit()
        self.layout.addWidget(self.questionEdit)

        self.askButton = QPushButton("提问")
        self.askButton.clicked.connect(self.ask_question)
        self.layout.addWidget(self.askButton)

        self.answerEdit = QTextEdit()
        self.answerEdit.setReadOnly(True)
        self.layout.addWidget(self.answerEdit)

        self.setLayout(self.layout)
        self.pdf_data = None

    def load_pdf(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        if file_path:
            self.answerEdit.append(f"已加载文件: {file_path}")
            self.pdf_data = parse_pdf(file_path)
            # 此处可调用文本预处理、分段、嵌入生成及索引构建流程

    def ask_question(self):
        question = self.questionEdit.toPlainText()
        self.answerEdit.append(f"提问: {question}")
        # 此处可整合 RAG 模块，根据问题检索文本并生成回答
        answer = "这里是模型生成的回答。（示例）"
        self.answerEdit.append(f"回答: {answer}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
