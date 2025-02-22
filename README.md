# PDF AI Trainer (基于 PyQt6 + PyTorch)

## 📌 项目简介
本项目基于 `PyQt6` 构建 GUI，使用 `PyTorch` 进行训练，结合 `PyMuPDF` 解析 PDF，并支持 OCR 识别扫描版 PDF（使用 `pdf2image` + `pytesseract`）。

---

## 🚀 功能
- **📂 选择 PDF**：从 GUI 选择多个 PDF 并进行训练
- **🔍 自动 OCR**：如果 PDF 不是文本，将自动进行 OCR 识别
- **🧠 训练 AI 模型**：使用 `transformers` 进行训练
- **📖 依据 PDF 内容回答问题**：训练后模型可以基于 PDF 知识回答问题
- **💾 模型保存与加载**：训练完成后，模型可保存并在 GUI 中调用、

