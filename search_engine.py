import os
import json

MODEL_DIR = "model_data"
TRAINED_DATA_PATH = os.path.join(MODEL_DIR, "trained_data.json")

def load_trained_data():
    """加载训练数据，如果文件不存在，则创建一个空的 trained_data.json"""
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)  # 如果 model_data 目录不存在，则创建

    if not os.path.exists(TRAINED_DATA_PATH):
        # 如果 trained_data.json 不存在，创建一个空文件
        with open(TRAINED_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=4, ensure_ascii=False)

    # 读取训练数据
    with open(TRAINED_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

trained_data = load_trained_data()

def search(query):
    """在训练数据中查找匹配的内容"""
    results = trained_data.get(query, "未找到相关信息")
    return results
