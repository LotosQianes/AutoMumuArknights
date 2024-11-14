import tensorflow as tf
import os
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2

def load_model(model_path):
    """ 加载训练好的模型 """
    if not os.path.exists(model_path):
        print(f"模型文件 {model_path} 不存在！")
        return None
    return tf.keras.models.load_model(model_path)

def predict(model, img, target_size=(28, 28)):
    """ 用训练好的模型对单张图像进行预测 """

    # 调整图像大小（如果需要）
    img_resized = cv2.resize(img, target_size)

    # 转换为 NumPy 数组并扩展维度
    img_array = np.expand_dims(img_resized, axis=0)

    # 正则化处理
    img_array = img_array / 255.0

    # 进行预测
    predictions = model.predict(img_array)

    # 假设模型返回的是类别的概率分布，可以获取最可能的类别索引
    predicted_class = np.argmax(predictions, axis=1)[0]

    return predicted_class