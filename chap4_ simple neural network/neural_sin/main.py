import numpy as np
import matplotlib.pyplot as plt


# 模型定义
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        # 隐藏层
        self.W1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros(hidden_size)
        #输出层
        self.W2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros(output_size)

    # ReLU 激活函数
    def relu(self, Z):
        return np.maximum(0, Z)
    
    # ReLU 求导
    def _relu(self, Z):
        return (Z > 0).astype(float)
    
    # 前向传播
    def forward(self, x):
        self.Z1 = np.dot(x, self.W1) + self.b1
        self.A1 = self.relu(self.Z1)
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        return self.Z2
    
    # 反向传播
    def backward(self, x, y, learn_rate):
        m = x.shape[0]

        # 输出层
        dZ2 = self.Z2 - y
        dW2 = self.A1.T.dot(dZ2) / m
        db2 = np.sum(dZ2, axis=0) / m
        
        # 隐藏层
        dZ1 = dZ2.dot(self.W2.T) * self._relu(self.Z1)
        dW1 = x.T.dot(dZ1) / m
        db1 = np.sum(dZ1, axis=0) / m

        # 梯度下降
        self.W1 -= learn_rate * dW1
        self.b1 -= learn_rate * db1
        self.W2 -= learn_rate * dW2
        self.b2 -= learn_rate * db2


# 目标函数
def target_function(x):
    return np.sin(x)

# 数据采样
X_train = np.linspace(-np.pi, np.pi, 800).reshape(-1, 1)
Y_train = target_function(X_train)
X_test = np.linspace(-np.pi, np.pi, 200).reshape(-1, 1)
Y_test = target_function(X_test)


# 模型训练
model = NeuralNetwork(input_size=1, hidden_size=200, output_size=1)

epochs = 50000
learn_rate = 0.01
decay_rate = 1e-12
losses = []

for e in range(epochs):
    # 前向传播
    Y_ = model.forward(X_train)

    # 计算损失（采用 MSE）
    loss = np.mean((Y_ - Y_train)**2)
    losses.append(loss)

    # 反向传播
    model.backward(X_train, Y_train, learn_rate=learn_rate)

    # 学习率衰减
    learn_rate *= (1. / (1. + decay_rate * e))

    # 每 1000 轮学习输出
    if e % 1000 == 0:
        print(f"Epoch {e}, Loss: {loss}, Learning Rate: {learn_rate}")


# 学习效果
Y_predict = model.forward(X_test)

# 可视化
# 可视化结果
plt.figure(figsize=(10, 6))
plt.scatter(X_test, Y_test, color='red', label='True Function', s=8)
plt.scatter(X_test, Y_predict, color='green', label='Model Prediction', s=8)
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.show()
