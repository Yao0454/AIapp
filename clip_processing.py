import torch
import clip
import numpy as np
from PIL import Image

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def encode_text(text):
    """使用 CLIP 计算文本特征"""
    text_features = model.encode_text(clip.tokenize(text).to(device))
    return text_features.detach().cpu().numpy()

def encode_image(image):
    """使用 CLIP 计算图像特征"""
    image = preprocess(image).unsqueeze(0).to(device)
    image_features = model.encode_image(image)
    return image_features.detach().cpu().numpy()
