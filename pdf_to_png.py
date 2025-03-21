import os
import fitz  # for python > 3.8, use pip install PyMuPDF
from PIL import Image


def pdf_to_images(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开PDF文件
    pdf_document = fitz.open(pdf_path)

    # 获取总页数
    total_pages = len(pdf_document)

    # 计算需要保留的页面范围
    start_page = 7  # 跳过前7页(目录)
    end_page = total_pages - 1  # 跳过最后一页
    for page_num in range(start_page, end_page):
        # 获取每一页的内容
        page = pdf_document.load_page(page_num)

        # 将页面转换为像素矩阵
        pix = page.get_pixmap()

        # 创建一个PIL图像对象
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # 保存图像到指定文件夹
        output_path = f"{output_folder}/page_{page_num + 1}.png"
        img.save(output_path)


# 使用示例
for ch in range(1, 46):
    ch = '0' + str(ch) if ch < 10 else ch
    pdf_path = f"data/pdfs/机器猫_{ch}.pdf"
    output_folder = f"data/images/ch_{ch}"
    pdf_to_images(pdf_path, output_folder)
    print(f"Finished converting {pdf_path} to images.")
