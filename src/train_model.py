# src/train_model.py
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from src.pdf_parser import parse_pdf
from src.text_preprocessing import clean_text, split_text

def train(pdf_files):
    all_texts = []
    for file in pdf_files:
        pages = parse_pdf(file, use_ocr=True)  # 确保开启 OCR
        for page in pages:
            if text := page['text']:  # 只有非空内容才加入训练数据
                all_texts.append(text)

    if not all_texts:
        raise ValueError("所有 PDF 页面均无有效文本，请检查文件格式！")

    print(f"最终提取文本量: {len(all_texts)}")
    
    # 此处构造数据集（示例中用简单的文本列表，实际需要构造合适的 Dataset）
    class PDFDataset(torch.utils.data.Dataset):
        def __init__(self, texts, tokenizer, max_length=64):
            self.texts = texts
            self.tokenizer = tokenizer
            self.max_length = max_length
        def __len__(self):
            return len(self.texts)
        def __getitem__(self, idx):
            encoding = self.tokenizer(
                self.texts[idx], return_tensors='pt',
                truncation=True, padding='max_length', max_length=self.max_length
            )
            encoding = {k: v.squeeze(0) for k, v in encoding.items()}
            encoding['labels'] = encoding['input_ids']
            return encoding

    model_name = "uer/gpt2-chinese-cluecorpussmall"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    dataset = PDFDataset(all_texts, tokenizer)
    
    training_args = TrainingArguments(
        output_dir='./models/fine_tuned_model',
        num_train_epochs=1,
        per_device_train_batch_size=2,
        save_steps=10,
        logging_steps=5,
        save_total_limit=2,
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer,
    )
    
    trainer.train()
    model.save_pretrained("./models/fine_tuned_model")
    tokenizer.save_pretrained("./models/fine_tuned_model")

if __name__ == '__main__':
    # 如果直接运行 train_model.py，可以传入一个测试文件列表
    train(["data/raw/example.pdf"])
