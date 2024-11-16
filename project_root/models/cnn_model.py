import tensorflow as tf
from tensorflow.keras import layers, models
 
def create_cnn_model(input_shape=(28, 28, 3), num_classes=9):
    model = models.Sequential()
 
    # 第一层卷积层 + 批归一化
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
 
    # 第二层卷积层 + 批归一化
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
 
    # 第三层卷积层 + 批归一化
    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling2D((2, 2)))
 
    # 展平层
    model.add(layers.Flatten())
 
    # 全连接层 + 批归一化 + Dropout
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.BatchNormalization())
    model.add(layers.Dropout(0.5))  # 添加Dropout层
 
    # 输出层
    model.add(layers.Dense(num_classes, activation='softmax'))
 
    # 编译模型
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
 
    return model