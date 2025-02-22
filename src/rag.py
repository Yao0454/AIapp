# src/rag.py
from embedder import get_embedding
from vector_indexer import VectorIndexer

def retrieve_relevant_text(query, indexer: VectorIndexer):
    """利用嵌入模型获取查询向量，并在向量索引中检索最相似的文本片段"""
    query_emb = get_embedding(query)
    distances, results = indexer.search(query_emb, k=3)
    return results

def generate_answer(query, retrieved_texts):
    """
    构造 prompt，将检索到的文本片段作为上下文，
    并调用语言模型生成回答（此处仅返回构造的 prompt 作为示例）
    """
    context = "\n".join([text['text'] for text in retrieved_texts])
    prompt = f"根据以下上下文回答问题：\n{context}\n问题：{query}\n答案："
    # 在实际实现中，可将 prompt 输入模型生成答案
    return prompt

if __name__ == '__main__':
    # 示例：假定向量维度为384，创建并测试索引
    dim = 384
    indexer = VectorIndexer(dim)
    # 此处应加载或构建实际索引
    query = "什么是机器学习？"
    retrieved = retrieve_relevant_text(query, indexer)
    answer = generate_answer(query, retrieved)
    print(answer)
