import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from PIL import Image
import io

# 设置 tesseract 路径（根据你的操作系统进行设置）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows 示例

def extract_images_from_pdf(pdf_file):
    """提取 PDF 中的图片"""
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    images = []
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        image_list = page.get_images(full=True)
        
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(Image.open(io.BytesIO(image_bytes)))  # 保存为 PIL 图像对象
    return images

def ocr_images(images):
    """对提取的图片进行 OCR 识别"""
    ocr_text = []
    for image in images:
        text = pytesseract.image_to_string(image)
        ocr_text.append(text)
    return ocr_text