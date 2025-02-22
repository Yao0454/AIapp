# src/vector_indexer.py
import os
import faiss
import numpy as np
import pickle

class VectorIndexer:
    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []  # 存储每个向量对应的文本、来源、页码等信息
    
    def add_vectors(self, vectors, metadata_list):
        """将向量与对应元数据加入索引"""
        self.index.add(vectors)
        self.metadata.extend(metadata_list)
    
    def save(self, index_path, meta_path):
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        faiss.write_index(self.index, index_path)
        with open(meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)
    
    def load(self, index_path, meta_path):
        if not os.path.exists(index_path):
            print(f"Index file {index_path} does not exist. Creating a new one.")
            self.index = faiss.IndexFlatL2(self.dim)
            faiss.write_index(self.index, index_path)
        else:
            self.index = faiss.read_index(index_path)
        
        if not os.path.exists(meta_path):
            print(f"Metadata file {meta_path} does not exist. Creating a new one.")
            self.metadata = []
            with open(meta_path, 'wb') as f:
                pickle.dump(self.metadata, f)
        else:
            with open(meta_path, 'rb') as f:
                self.metadata = pickle.load(f)
    
    def search(self, query_vector, k=5):
        """返回与 query_vector 最相似的 k 个向量对应的元数据"""
        query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return distances, results

if __name__ == '__main__':
    # 测试示例：生成随机向量并构建索引
    dim = 384  # 根据嵌入模型的输出维度
    indexer = VectorIndexer(dim)
    vectors = np.random.rand(10, dim).astype('float32')
    metadata_list = [{'text': f"Sample text {i}", 'source': 'example.pdf', 'page': i+1} for i in range(10)]
    indexer.add_vectors(vectors, metadata_list)
    query_vector = np.random.rand(dim).astype('float32')
    distances, results = indexer.search(query_vector, k=3)
    print("Results:", results)
