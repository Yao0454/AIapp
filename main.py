import os
import time
import logging
import gradio as gr
from train import process_pdf
from search_engine import search

# 配置 logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def train_model(file_obj):
    """
    训练模型，返回训练过程的日志信息
    """
    if file_obj is None:
        return "请先上传 PDF 文件！"
        
    try:
        # 保存上传的文件
        file_path = os.path.join(UPLOAD_DIR, file_obj.name)
        with open(file_path, "wb") as f:
            f.write(file_obj.read())
            
        log = "📢 开始训练...\n"
        process_pdf(file_path)
        for i in range(1, 6):
            log += f"🛠️ 训练进度：{i * 20}%\n"
            logging.info(f"训练进度：{i * 20}%")
            time.sleep(1)
        log += "✅ 训练完成！\n"
        logging.info("训练完成！")
        return log
    except Exception as e:
        error_msg = f"❌ 训练失败：{str(e)}"
        logging.error(error_msg)
        return error_msg

def ask_question(query):
    """查询 PDF 训练数据"""
    if not query:
        return "请输入问题！"
    
    results = search(query)
    return "\n\n".join(results) if results else "未找到相关内容！"

with gr.Blocks() as app:
    gr.Markdown("# 📖 AI 课本助手")
    
    # 上传 PDF 并训练
    with gr.Row():
        pdf_input = gr.File(label="上传 PDF 课本", type="binary")
        train_button = gr.Button("训练")
    train_output = gr.Textbox(label="训练日志", interactive=False, lines=10)
    train_button.click(fn=train_model, inputs=pdf_input, outputs=train_output)
    
    # 询问 AI
    with gr.Row():
        question_input = gr.Textbox(label="输入你的问题")
        ask_button = gr.Button("查询")
    answer_output = gr.Textbox(label="AI 答案")
    ask_button.click(fn=ask_question, inputs=question_input, outputs=answer_output)

# 运行 Gradio WebUI
app.launch(share=True)
