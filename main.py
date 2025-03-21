import os
import json
from typing import List, Dict
from ocr import detect_text


def process_images_in_folder(
    root_folder='panels',
    index_file='./data/panels/panel_index_dialoge.json',
):
    # 存储面板路径和对应的文字内容
    panel_texts: Dict[str, str] = {}

    # 检查是否已经存在索引文件
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            panel_texts = json.load(f)
        print(f"Loaded existing index from {index_file}")

    # 遍历根文件夹及其子文件夹中的所有图像文件
    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if not filename.endswith(('.jpg', '.png', '.jpeg')):
                continue

            image_path: str = os.path.abspath(os.path.join(dirpath, filename))

            # 如果图像已经在索引中，则跳过
            if image_path in panel_texts:
                continue

            try:
                # 提取对话
                text = detect_text(image_path)

                if not text.strip():
                    continue

                # 存储面板路径和文字内容
                panel_texts[image_path] = text

                # 保存索引文件
                with open(index_file, 'w', encoding='utf-8') as f:
                    json.dump(panel_texts, f, ensure_ascii=False, indent=4)
                print(f"Updated index with {image_path}.")
            except Exception as e:
                print(f"Error processing image {filename}: {e}")


def search_panels_by_text(panel_texts, query) -> list:
    results = []
    for panel_path, text in panel_texts.items():
        if query.lower() in text.lower():
            results.append(panel_path)
    return results


if __name__ == "__main__":
    panel_texts: Dict[str, str] = {}

    # 处理图像并提取文字
    root_folder = './data/panels'
    index_file = './data/panel_index.json'  # 指定 JSON 文件保存路径
    process_images_in_folder(root_folder, index_file)

    # 加载最新的索引文件
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            panel_texts = json.load(f)
        print(f"Reloaded updated index from {index_file}")

    # 搜索包含特定文字的面板
    query = input("Enter the text to search for: ")
    matching_panels: List[str] = search_panels_by_text(panel_texts, query)

    if matching_panels:
        print(f"Found {len(matching_panels)} panels:")
        for panel_path in matching_panels:
            print(f'{panel_path} with text {panel_texts[panel_path]}')
    else:
        print("No panels found.")
