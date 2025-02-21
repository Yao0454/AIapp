from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from pdf_text_extraction import extract_text_from_pdf
from image_extraction import extract_images_from_pdf, ocr_images
from clip_processing import process_image_and_text
import io

# FastAPI实例
app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(question: Question, file: UploadFile = File(...)):
    # 从上传的 PDF 文件中提取文本和图像
    pdf_content = await file.read()
    book_text = extract_text_from_pdf(pdf_content)
    images = extract_images_from_pdf(pdf_content)

    # 使用 OCR 识别图像中的文本
    ocr_texts = ocr_images(images)
    combined_text = book_text + "\n".join(ocr_texts)  # 合并PDF中的文本和OCR识别的文本

    # 对用户的提问进行简单处理并返回相关答案
    answer = "这是一个简单的答案"  # 模拟一个简单答案逻辑，可以基于更多的文本和问答模型改进
    similarity_scores = []

    # 如果问题涉及到图像（例如图像描述），计算图像与文本的相似度
    for image in images:
        text = question.question  # 假设问题是描述图像内容
        image_text_similarity, text_image_similarity = process_image_and_text(image, text)
        similarity_scores.append((image, image_text_similarity.item()))

    # 返回最相关的图像的相似度结果
    best_match_image = max(similarity_scores, key=lambda x: x[1]) if similarity_scores else None
    result = {
        "answer": answer,
        "best_match_image": str(best_match_image[0]) if best_match_image else None,
        "similarity_score": best_match_image[1] if best_match_image else None
    }

    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)