import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from cnn_model import create_cnn_model

def train_model(train_dir, validation_dir, model_save_path):
    """
    训练CNN模型，并保存到指定路径。

    :param train_dir: 训练集的路径
    :param validation_dir: 验证集的路径
    :param model_save_path: 训练完成后保存模型的路径
    """

    # 设置训练参数
    input_shape = (28, 28, 3)  # 输入图像的尺寸
    num_classes = 1     # 类别数量，根据你的数据集来设置

    # 创建数据生成器
    train_datagen = ImageDataGenerator(rescale=1./255)  # 归一化
    validation_datagen = ImageDataGenerator(rescale=1./255)

    # 确认数据路径是否正确
    print(f"训练集路径: {train_dir}")
    print(f"验证集路径: {validation_dir}")

    # 从目录中加载训练数据
    try:
        train_generator = train_datagen.flow_from_directory(
            train_dir,                   # 训练集的路径
            target_size=(28, 28),        # 调整图片大小
            batch_size=32,               # 每次训练32张图片
            class_mode='categorical'     # 分类任务，标签会自动转换为one-hot编码
        )
    except Exception as e:
        print(f"加载训练数据时出错: {e}")
        return

    # 从目录中加载验证数据
    try:
        validation_generator = validation_datagen.flow_from_directory(
            validation_dir,              # 验证集的路径
            target_size=(28, 28),        # 调整图片大小
            batch_size=32,               # 每次验证32张图片
            class_mode='categorical'     # 分类任务，标签会自动转换为one-hot编码
        )
    except Exception as e:
        print(f"加载验证数据时出错: {e}")
        return

    # 创建模型
    model = create_cnn_model(input_shape=input_shape, num_classes=num_classes)

    # 训练模型
    model.fit(
        train_generator,             # 训练数据生成器
        epochs=30,                   # 训练30个epochs
        validation_data=validation_generator,  # 验证数据
        validation_steps=50         # 验证步数，根据验证集的大小设置
    )

    # 保存模型
    model.save(model_save_path)  # 保存模型到指定路径
    print(f"模型已保存至 {model_save_path}")

if __name__ == "__main__":
    # 获取当前脚本所在的路径
    current_dir = os.path.dirname(__file__)
    # 指定训练和验证数据的路径
    train_data_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'training_data'))
    validation_data_path = os.path.abspath(os.path.join(current_dir, '..', 'data', 'test_data'))

    # 模型保存路径
    model_save_path = os.path.join(os.path.dirname(__file__), 'cnn_model', 'cnn_model.h5')

    # 调用训练函数
    train_model(train_data_path, validation_data_path, model_save_path)