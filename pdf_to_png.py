import os
import fitz  # for python > 3.8, use pip install PyMuPDF
from PIL import Image


def pdf_to_images(pdf_path, output_folder, start_skip=0, end_skip=0):
    os.makedirs(output_folder, exist_ok=True)

    with fitz.open(pdf_path) as pdf_document:
        # 获取总页数
        total_pages = len(pdf_document)
    
        # 计算需要保留的页面范围
        start_page = start_skip
        end_page = total_pages - end_skip

        # 边界检查
        if start_page >= end_page:
            raise ValueError(
                f"无有效页面可处理: 起始页({start_page}) ≥ 结束页({end_page})"
                f"\n总页数: {total_pages}, 跳过开头{start_skip}页 + 结尾{end_skip}页"
            )

        for page_num in range(start_page, end_page):
            # 获取每一页的内容
            page = pdf_document.load_page(page_num)
    
            # 将页面转换为像素矩阵
            pix = page.get_pixmap()
    
            # 创建一个PIL图像对象
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
            # 保存图像到指定文件夹
            output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
            img.save(output_path)


if __name__=="__main__":
    for ch in range(1, 46):
        ch = '0' + str(ch) if ch < 10 else ch
        pdf_path = f"data/pdfs/机器猫_{ch}.pdf"
        output_folder = f"data/images/ch_{ch}"
        pdf_to_images(pdf_path, output_folder, start_skip=7, end_skip=1)
        print(f"Finished converting {pdf_path} to images.")
