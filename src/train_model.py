# src/train_model.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

def train(texts, num_train_epochs=3, output_dir='./model_output', checkpoint_dir='./checkpoints'):
    if not texts:
        raise ValueError("没有提供任何文本进行训练！")

    print(f"最终提取文本量: {len(texts)}")
    
    # 构造数据集
    class PDFDataset(torch.utils.data.Dataset):
        def __init__(self, texts, tokenizer, max_length=64):
            self.texts = texts
            self.tokenizer = tokenizer
            self.max_length = max_length
        def __len__(self):
            return len(self.texts)
        def __getitem__(self, idx):
            encoding = self.tokenizer(
                self.texts[idx]['text'], return_tensors='pt',
                truncation=True, padding='max_length', max_length=self.max_length
            )
            encoding = {k: v.squeeze(0) for k, v in encoding.items()}
            encoding['labels'] = encoding['input_ids']
            return encoding

    model_name = "uer/gpt2-chinese-cluecorpussmall"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    dataset = PDFDataset(texts, tokenizer)

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=4,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir='./logs',
        logging_steps=200,
        load_best_model_at_end=False,  # 禁用此选项，因为没有评估
        save_strategy="no",  # 禁用保存策略
        evaluation_strategy="no"  # 禁用评估
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        tokenizer=tokenizer
    )

    # 检查是否存在有效的检查点
    if os.path.isdir(checkpoint_dir) and os.listdir(checkpoint_dir):
        trainer.train(resume_from_checkpoint=checkpoint_dir)
    else:
        trainer.train()

    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)

# 示例调用
if __name__ == '__main__':
    sample_texts = [{'text': '这是一个测试文本。'}]
    train(sample_texts, num_train_epochs=5)
