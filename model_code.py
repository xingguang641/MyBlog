import numpy as np
np.random.seed(0)
X = np.random.randn(100, 2)
true_w = np.array([2, -1])
sigmoid = lambda x: 1 / (1 + np.exp(-x))
y = (sigmoid(X @ true_w) > 0.5).astype(int)


# 激活函数
sigmoid = lambda x: 1 / (1 + np.exp(-x))
# 损失函数
loss_func = lambda X, y, w: -np.mean(
    y * np.log(sigmoid(X @ w)) + (1 - y) * np.log(1 - sigmoid(X @ w))
)
# 梯度下降
gradient = lambda X, y, w: X.T @ (sigmoid(X @ w) - y) / len(y)
def grad_desc(cur_w, alpha, X, y):
    grad = gradient(X, y, cur_w)
    updated_w = cur_w - alpha * grad
    return updated_w
# 主函数
def main(X, y, initial_w, alpha, num_iter):
    w = initial_w
    # 定义一个list保存所有的损失函数值，用来显示下降的过程
    cost_list = []
    for i in range(num_iter):
        cost_list.append(loss_func(X, y, w))
        w, b = grad_desc(w, alpha, X, y)
    return [w, b, cost_list]


# 设置超参数
alpha = 0.1
initial_w = np.zeros(X.shape[1])
num_iter = 1000
# 执行代码
if __name__ == "__main__":
    w, cost_list = main(X, y, initial_w, alpha, num_iter)
    print("\n训练结束")
    print("w =", w)
    cost = loss_func(X, y, w)
    print("cost =", cost)


