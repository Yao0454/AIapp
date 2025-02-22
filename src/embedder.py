# src/embedder.py
from sentence_transformers import SentenceTransformer

model_name = 'all-MiniLM-L6-v2'  # 可根据需要选择其他模型
model = SentenceTransformer(model_name)

def get_embedding(text):
    """返回文本的向量嵌入"""
    embedding = model.encode(text)
    return embedding

if __name__ == '__main__':
    sample_text = "This is a test sentence."
    emb = get_embedding(sample_text)
    print(emb.shape)
