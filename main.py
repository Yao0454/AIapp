import sys
import os
import numpy as np
import faiss
import pickle
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QFileDialog, QLabel, QTextEdit, QCheckBox, QLineEdit, QSpinBox, QHBoxLayout
)
from PyQt6.QtCore import QThread, pyqtSignal

from src.pdf_parser import parse_pdf
from src.text_preprocessing import clean_text, split_text
from src.embedder import get_embedding
from src.vector_indexer import VectorIndexer
from src.rag import retrieve_relevant_text, generate_answer
from src.train_model import train

class PDFProcessingThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal(list)

    def __init__(self, pdf_files, use_ocr):
        super().__init__()
        self.pdf_files = pdf_files
        self.use_ocr = use_ocr

    def run(self):
        all_texts = []
        for pdf in self.pdf_files:
            self.log_signal.emit(f"正在解析 {pdf} ...")
            parsed_pages = parse_pdf(pdf, self.use_ocr)
            for page in parsed_pages:
                cleaned_text = clean_text(page['text'])
                chunks = split_text(cleaned_text)
                all_texts.extend({'text': chunk, 'source': pdf, 'page': page['page']} for chunk in chunks)
            self.log_signal.emit(f"{pdf} 解析完成！")
        self.done_signal.emit(all_texts)

class TrainingThread(QThread):
    log_signal = pyqtSignal(str)
    done_signal = pyqtSignal()

    def __init__(self, texts, indexer, num_train_epochs, checkpoint_dir):
        super().__init__()
        self.texts = texts
        self.indexer = indexer
        self.num_train_epochs = num_train_epochs
        self.checkpoint_dir = checkpoint_dir

    def run(self):
        embeddings = []
        metadata_list = []
        for item in self.texts:
            self.log_signal.emit(f"嵌入文本: {item['text'][:30]}...")
            emb = get_embedding(item['text'])
            embeddings.append(emb)
            metadata_list.append(item)
        
        embeddings = np.array(embeddings, dtype='float32')
        self.indexer.add_vectors(embeddings, metadata_list)
        self.indexer.save("./models/vector_index/vector.index", "./models/vector_index/metadata.pkl")
        self.log_signal.emit("训练完成，索引已保存！")

        # 调用训练函数
        train(self.texts, self.num_train_epochs, output_dir="./model_output", checkpoint_dir=self.checkpoint_dir)
        self.done_signal.emit()

class RAGGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RAG PDF AI")
        self.setGeometry(100, 100, 700, 600)

        self.selected_files = []
        self.indexer = VectorIndexer(384)
        self.indexer.load("./models/vector_index/vector.index", "./models/vector_index/metadata.pkl")  # 预加载已有索引

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 文件选择部分
        file_layout = QHBoxLayout()
        self.label = QLabel("选择 PDF 文件：")
        file_layout.addWidget(self.label)
        self.select_button = QPushButton("选择 PDF 文件")
        self.select_button.clicked.connect(self.select_files)
        file_layout.addWidget(self.select_button)
        layout.addLayout(file_layout)

        # OCR 选项
        self.ocr_checkbox = QCheckBox("启用 OCR 识别（处理扫描版 PDF）")
        layout.addWidget(self.ocr_checkbox)

        # 解析按钮
        self.parse_button = QPushButton("解析 PDF")
        self.parse_button.clicked.connect(self.start_pdf_processing)
        layout.addWidget(self.parse_button)

        # 训练设置部分
        train_layout = QHBoxLayout()
        self.epochs_label = QLabel("训练次数:", self)
        train_layout.addWidget(self.epochs_label)
        self.epochs_input = QSpinBox(self)
        self.epochs_input.setMinimum(1)
        self.epochs_input.setValue(3)
        train_layout.addWidget(self.epochs_input)
        self.checkpoint_label = QLabel("检查点路径:", self)
        train_layout.addWidget(self.checkpoint_label)
        self.checkpoint_input = QLineEdit(self)
        self.checkpoint_input.setText("./checkpoints")
        train_layout.addWidget(self.checkpoint_input)
        layout.addLayout(train_layout)

        # 训练按钮
        self.train_button = QPushButton("训练模型")
        self.train_button.clicked.connect(self.start_training)
        self.train_button.setEnabled(False)  # 解析后才可用
        layout.addWidget(self.train_button)

        # 加载模型按钮
        self.load_model_button = QPushButton("加载模型")
        self.load_model_button.clicked.connect(self.load_model)
        layout.addWidget(self.load_model_button)

        # 选择模型文件夹按钮
        self.select_model_button = QPushButton("选择模型文件夹")
        self.select_model_button.clicked.connect(self.select_model_folder)
        layout.addWidget(self.select_model_button)

        # 查询部分
        query_layout = QHBoxLayout()
        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("请输入问题...")
        query_layout.addWidget(self.question_input)
        self.ask_button = QPushButton("查询")
        self.ask_button.clicked.connect(self.ask_question)
        self.ask_button.setEnabled(False)  # 训练完成后可用
        query_layout.addWidget(self.ask_button)
        layout.addLayout(query_layout)

        # 日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择 PDF 文件", "", "PDF Files (*.pdf)")
        if files:
            self.selected_files = files
            self.label.setText(f"已选文件: {', '.join(os.path.basename(f) for f in files)}")
            self.log_output.append(f"选中文件:\n{'\n'.join(files)}")

    def start_pdf_processing(self):
        if not self.selected_files:
            self.log_output.append("请先选择 PDF 文件。")
            return

        use_ocr = self.ocr_checkbox.isChecked()
        self.log_output.append("开始解析 PDF ...")
        self.parse_thread = PDFProcessingThread(self.selected_files, use_ocr)
        self.parse_thread.log_signal.connect(self.log_output.append)
        self.parse_thread.done_signal.connect(self.on_pdf_processed)
        self.parse_thread.start()

    def on_pdf_processed(self, texts):
        self.texts = texts
        self.log_output.append("PDF 解析完成，可以开始训练！")
        self.train_button.setEnabled(True)

    def start_training(self):
        if not hasattr(self, 'texts') or not self.texts:
            self.log_output.append("没有解析到文本，无法训练！")
            return

        num_train_epochs = self.epochs_input.value()
        checkpoint_dir = self.checkpoint_input.text()

        self.log_output.append(f"开始训练，训练次数: {num_train_epochs}，检查点路径: {checkpoint_dir} ...")
        self.train_thread = TrainingThread(self.texts, self.indexer, num_train_epochs, checkpoint_dir)
        self.train_thread.log_signal.connect(self.log_output.append)
        self.train_thread.done_signal.connect(self.on_training_done)
        self.train_thread.start()

    def on_training_done(self):
        self.log_output.append("训练完成，可以进行查询！")
        self.ask_button.setEnabled(True)

    def load_model(self):
        self.indexer.load("./models/vector_index/vector.index", "./models/vector_index/metadata.pkl")
        self.log_output.append("模型加载完成，可以进行查询！")
        self.ask_button.setEnabled(True)

    def select_model_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择模型文件夹", "")
        if folder:
            index_path = os.path.join(folder, "vector.index")
            meta_path = os.path.join(folder, "metadata.pkl")
            if os.path.exists(index_path) and os.path.exists(meta_path):
                self.indexer.load(index_path, meta_path)
                self.log_output.append(f"模型加载完成，可以进行查询！\n模型路径: {folder}")
                self.ask_button.setEnabled(True)
            else:
                self.log_output.append("所选文件夹中不存在有效的模型文件。")

    def ask_question(self):
        query = self.question_input.text().strip()
        if not query:
            self.log_output.append("请输入问题！")
            return

        self.log_output.append(f"查询: {query}")
        retrieved_texts = retrieve_relevant_text(query, self.indexer)
        answer = generate_answer(query, retrieved_texts)
        self.log_output.append(f"答案: {answer}")

def main():
    app = QApplication(sys.argv)
    window = RAGGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()