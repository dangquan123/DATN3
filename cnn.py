import cv2
import numpy as np
import matplotlib.pyplot as plt

# np.random.seed(47)
img = cv2.imread('dog.jpg')
img = cv2.resize(img, (200,200))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)/255 # chuẩn hóa dữ liệu, hạ các giá trị của dữ liệu xuống để tránh overflow
kernel = np.random.randn(3, 3)


class conv2d():
    def __init__(self, input, kernelSize, padding=0, stride=1):
        self.stride = stride
        self.kernelSize = kernelSize
        self.input = np.pad(input, ((padding, padding), (padding, padding)), 'constant')
        self.height, self.width = input.shape
        self.kernel = kernel

        self.result = np.zeros((int((self.height - self.kernelSize)/self.stride) + 1,
                                int((self.width - self.kernelSize)/self.stride) + 1))
    def getRoi(self):
        for row in range(0, (int((self.height - self.kernelSize)/self.stride) + 1)):
            for col in range(0, (int((self.width - self.kernelSize)/self.stride) + 1)):
                roi = self.input[row*self.stride: row*self.stride + self.kernelSize,
                      col*self.stride: col*self.stride + self.kernelSize]
                yield row, col, roi
    def operater(self):
        for row, col, roi in self.getRoi():
            self.result[row, col] = np.sum(roi * self.kernel)

        return self.result

class ReLu:
    def __init__(self, input_data):
        self.input = input_data
        self.height, self.width = input_data.shape
        self.result = np.zeros((self.height, self.width))

    def operate(self):
        for row in range(self.height):
            for col in range(self.width):
                self.result[row, col] = 0 if self.input[row, col] < 0 else self.input[row, col]
        return self.result

class leakyReLu:
    def __init__(self, input_data):
        self.input = input_data
        self.height, self.width = input_data.shape
        self.result = np.zeros((self.height, self.width))

    def operate(self):
        for row in range(self.height):
            for col in range(self.width):
                self.result[row, col] = 0.1 if self.input[row, col] < 0 else self.input[row, col]
        return self.result

for i in range(1,10):
    conv2d_instance = conv2d(img_gray, 3, stride=i)
    img_cnn_conv2d = conv2d_instance.operater()
    conv2d_relu_instance = ReLu(img_cnn_conv2d)
    img_conv2d_cnn_relu = conv2d_relu_instance.operate()
    #
    plt.subplot(3,3,i)
    plt.imshow(img_conv2d_cnn_relu, cmap="gray")
    print("......",end="")
plt.show()

