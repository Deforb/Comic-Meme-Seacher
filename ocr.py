import os
from paddleocr import PaddleOCR
import logging

logging.getLogger('ppocr').setLevel(logging.ERROR)

_ocr_engine = None


def initialize_ocr() -> None:
    """初始化PaddleOCR引擎（延迟加载）"""
    global _ocr_engine
    if _ocr_engine is None:
        _ocr_engine = PaddleOCR(
            use_angle_cls=False,
            lang='ch',
            show_log=False,
            enable_mkldnn=True,
        )


def detect_text(image_path: str, confidence_threshold: float = 0.6) -> str:
    """
    检测图片中的文字（从右到左，从上到下排序）

    Args:
        image_path: 图片文件路径
        confidence_threshold: 识别置信度阈值

    Returns:
        排序后的文本列表（可能为空列表）
    """
    global _ocr_engine
    initialize_ocr()

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")

    detection_result = _ocr_engine.ocr(image_path)[0]

    if not detection_result:
        return ''

    # 按x降序（右到左），y升序（上到下）
    sorted_results = sorted(
        detection_result,
        key=lambda x: (-x[0][0][0], x[0][0][1]),
    )
    print(sorted_results)
    # 提取文本并保持排序
    final_text = ''.join(
        line[1][0] for line in sorted_results if line[1][1] >= confidence_threshold
    )
    return final_text


if __name__ == '__main__':
    test_cases = [
        # 'data/panels/ch_24/page_139/panel_6.jpg',  # conf:0.5
        # 'data/panels/ch_24/page_80/panel_3.jpg',  # conf:0.73
        # 'data/panels/ch_24/page_139/panel_1.jpg',  # conf:0.63
        'data/panels/ch_24/page_78/panel_3.jpg',  # conf:0.63
    ]

    for path in test_cases:
        detected_text = detect_text(path)
        result = detected_text if detected_text else "未检测到有效文字"
        print(f"{os.path.basename(path)}: {result}")
