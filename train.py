import os
import json
import faiss
import numpy as np
from pdf_text_extraction import extract_text_from_pdf
from image_extraction import extract_images_from_pdf
from clip_processing import encode_text, encode_image

# 创建存储模型数据的文件夹
MODEL_DIR = "model_data"
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.join(MODEL_DIR, "images"), exist_ok=True)

# FAISS 向量数据库
dim = 512  # CLIP 生成的特征向量维度
index = faiss.IndexFlatL2(dim)

# 训练数据
text_data = []
text_features = []
image_features = []

def process_pdf(pdf_path):
    """处理 PDF 提取文本和图像特征"""
    global text_data, text_features, image_features

    # 提取文本并计算特征
    text = extract_text_from_pdf(pdf_path)
    text_data.append({"pdf": pdf_path, "text": text})
    text_feature = encode_text(text)
    text_features.append(text_feature)

    # 提取图片并计算特征
    images = extract_images_from_pdf(pdf_path)
    for idx, img_obj in enumerate(images):
        img_feature = encode_image(img_obj["image"])
        image_features.append(img_feature)

        # 保存图片
        img_save_path = os.path.join(MODEL_DIR, "images", f"{os.path.basename(pdf_path)}_{idx}.png")
        img_obj["image"].save(img_save_path)

    # 添加到 FAISS 索引
    index.add(np.array(text_features))
    index.add(np.array(image_features))

    # 保存训练数据
    with open(os.path.join(MODEL_DIR, "trained_data.json"), "w", encoding="utf-8") as f:
        json.dump(text_data, f, ensure_ascii=False, indent=4)

    np.save(os.path.join(MODEL_DIR, "text_features.npy"), np.array(text_features))
    np.save(os.path.join(MODEL_DIR, "image_features.npy"), np.array(image_features))
    
    faiss.write_index(index, os.path.join(MODEL_DIR, "faiss_index.bin"))

    print(f"📚 训练完成！数据已存入 {MODEL_DIR}/")

