from paddleocr import PaddleOCR, draw_ocr
import cv2

class OCR:
    def __init__(self, use_gpu=False, lang='ch'):
        """
        初始化OCR对象
        :param use_gpu: 是否使用GPU
        :param lang: 语言类型（'ch'为中文，'en'为英文）
        """
        self.ocr = PaddleOCR(use_gpu=use_gpu, lang=lang)

    def recognize(self, img):
        """
        识别图像中的文字
        :param img: 待识别的图像（numpy数组格式）
        :return: 识别结果，包括边界框、文字和置信度
        """
        # 转换图像为PaddleOCR支持的格式
        if isinstance(img, str):  # 如果输入是文件路径
            img = cv2.imread(img)
        if img is None:
            raise ValueError("输入的图像为空，请检查路径或图像内容！")
        
        # 调用PaddleOCR进行文字识别
        results = self.ocr.ocr(img, cls=True)
        return results

    def draw_results(self, img, results, output_path=None):
        """
        绘制文字识别结果（带边框和文字）
        :param img: 原始图像
        :param results: OCR识别结果
        :param output_path: 保存绘制结果的路径，如果为None则不保存
        :return: 绘制了边框和文字的图像
        """
        # 提取边界框、文本和置信度
        boxes = [line[0] for line in results[0]]
        texts = [line[1][0] for line in results[0]]
        scores = [line[1][1] for line in results[0]]

        # 绘制边框和文字
        img_with_boxes = draw_ocr(img, boxes, texts, scores, font_path='path/to/simfang.ttf')

        if output_path:
            cv2.imwrite(output_path, img_with_boxes)

        return img_with_boxes

    def get_texts_and_boxes(self, results):
        """
        提取OCR识别的文本和边界框
        :param results: OCR识别结果
        :return: 文本及其对应边界框的列表
        """
        texts_and_boxes = []
        for line in results[0]:
            box = line[0]  # 边界框
            text = line[1][0]  # 识别出的文字
            confidence = line[1][1]  # 置信度
            texts_and_boxes.append((text, box, confidence))
        return texts_and_boxes