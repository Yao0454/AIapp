from pdf2image import convert_from_path


try:
    images = convert_from_path("C:/Users/yaoyi/Downloads/Documents/1.pdf")
    print(f"转换成功，PDF 共 {len(images)} 页")
except Exception as e:
    print(f"转换失败: {e}")