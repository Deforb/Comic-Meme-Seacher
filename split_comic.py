import os
from typing import List, Tuple
import cv2
import numpy as np
from numpy.typing import NDArray


def preprocess_image(image: NDArray) -> NDArray:
    """对输入图像进行预处理，包括灰度转换、模糊、边缘检测和膨胀操作。

    Args:
        image: 输入的BGR格式图像数组

    Returns:
        处理后的二值化边缘图像
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 100, 200)
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(edges, kernel, iterations=1)


def get_valid_contours(
    dilated_edges: NDArray, min_area: int, max_area: int
) -> List[Tuple[int, int, int, int]]:
    """从二值化图像中检测并筛选有效的轮廓。

    Args:
        dilated_edges: 二值化的边缘图像
        min_area: 最小面积阈值
        max_area: 最大面积阈值

    Returns:
        有效面板的边界框列表，每个元素为 (x, y, width, height)
    """
    contours, _ = cv2.findContours(
        dilated_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    valid_panels = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if min_area < area < max_area and 0.1 < float(w) / h < 10:
            valid_panels.append((x, y, w, h))
    return valid_panels


def split_comic_variable_grid(
    image_path: str,
    output_folder: str = 'data/panels',
    min_area: int = 5000,
    max_area: int = 1000000,
) -> None:
    """将漫画页面分割成独立的面板。

    Args:
        image_path: 输入图像的路径
        output_folder: 输出面板的保存目录
        min_area: 最小面板面积
        max_area: 最大面板面积
    """
    os.makedirs(output_folder, exist_ok=True)

    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        return

    dilated_edges = preprocess_image(image)
    valid_panels = get_valid_contours(dilated_edges, min_area, max_area)

    # 保存每个面板到输出文件夹
    for idx, (x, y, w, h) in enumerate(valid_panels):
        panel = image[y : y + h, x : x + w]
        output_path = os.path.join(output_folder, f'panel_{idx + 1}.jpg')
        cv2.imwrite(output_path, panel)


if __name__=="__main__":
    for chapter in range(1, 46):
        chapter: str = '0' + str(chapter) if chapter < 10 else str(chapter)
        for page in range(8, 200):
            image_path: str = f'./data/images/ch_{chapter}/page_{page}.png'
            if page > 190 and not os.path.exists(image_path):
                break
            split_comic_variable_grid(
                image_path=image_path,
                output_folder=f'./data/panels/ch_{chapter}/page_{page}',
            )
        print(f'Finish chapter_{chapter}')
