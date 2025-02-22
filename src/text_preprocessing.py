# src/text_preprocessing.py
import re

def clean_text(text):
    """清洗文本：去除多余空格、换行等"""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def split_text(text, chunk_size=500, overlap=50):
    """
    将文本分割为固定长度的片段，
    chunk_size：每个片段的词数，overlap：相邻片段的重叠词数
    """
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += (chunk_size - overlap)
    return chunks

if __name__ == '__main__':
    sample_text = "This is a sample text " * 100
    cleaned = clean_text(sample_text)
    chunks = split_text(cleaned)
    print(f"Total chunks: {len(chunks)}")
