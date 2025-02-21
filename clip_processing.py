from transformers import CLIPProcessor, CLIPModel
from PIL import Image

# 加载 CLIP 模型和处理器
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")

def process_image_and_text(image: Image, text: str):
    """处理图像和文本并返回相似度"""
    inputs = clip_processor(text=text, images=image, return_tensors="pt", padding=True)
    outputs = clip_model(**inputs)
    logits_per_image = outputs.logits_per_image  # 图像与文本的相似度
    logits_per_text = outputs.logits_per_text  # 文本与图像的相似度
    return logits_per_image.softmax(dim=-1), logits_per_text.softmax(dim=-1)