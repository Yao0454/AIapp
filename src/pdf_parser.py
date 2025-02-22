import fitz  # PyMuPDF 解析 PDF
import pytesseract  # OCR 识别
from pdf2image import convert_from_path  # 将 PDF 页面转换为图像
from PIL import Image  # 处理图像

def parse_pdf(pdf_path, use_ocr=True):
    """ 解析 PDF，并在无文本时使用 OCR """
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()  # 尝试提取文本
        
        if not text and use_ocr:  # 如果没有文本，使用 OCR
            print(f"页面 {page_num + 1} 可能是图片，正在进行 OCR 识别...")
            images = convert_from_path(pdf_path, first_page=page_num + 1, last_page=page_num + 1)
            ocr_text = pytesseract.image_to_string(images[0], lang="chi_sim+eng")  # 识别中文 + 英文
            text = ocr_text.strip()

        pages.append({'page': page_num + 1, 'text': text})

    return pages
