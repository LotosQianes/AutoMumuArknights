from cnn_model import create_cnn_model
from inference import load_model, predict
import os
import cv2

def main():
	# 加载已经训练好的AI模型
    model_path = os.path.join(os.path.dirname(__file__), 'cnn_model', 'cnn_model.h5')  # 假设模型保存路径是这样
    model = load_model(model_path)
    if model is None:
        print("模型加载失败！")
        return

    # 对截图进行图像分类（假设你已获得截图路径）
    test_img_path = os.path.join(os.path.dirname(__file__),'..', 'data', 'training_data', 'game_icon', 'wake.png')
    test_img_path = os.path.abspath(test_img_path)

    # 读取图像（确保它是一个有效的图像文件）
    img = cv2.imread(test_img_path)
    if img is None:
        print(f"无法读取图像：{test_img_path}")
        return None

    img_name = predict(model, img)
    print("图像分类预测结果：", img_name)

if __name__ == "__main__":
    main()