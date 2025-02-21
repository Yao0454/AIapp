import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_file):
    """从上传的PDF文件中提取文本"""
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")  # 提取页面的文本内容
    return text