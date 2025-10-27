import numpy as np

# 假设 X: (n_samples, n_features), y: (n_samples,) 且值为 +1/-1
def linear_svm_train(X, y, lr=0.001, epochs=1000):
    n_samples, n_features = X.shape
    alpha = np.zeros(n_samples)

    # 梯度上升求解对偶问题
    for _ in range(epochs):
        for i in range(n_samples):
            # 对 α_i 的梯度
            grad = 1 - np.sum(alpha * y * y[i] * np.dot(X, X[i]))
            alpha[i] += lr * grad
            alpha[i] = max(alpha[i], 0)  # 保证 α_i >= 0

    # 计算 w
    w = np.sum((alpha * y)[:, None] * X, axis=0)

    # 找一个支持向量求 b
    sv_idx = np.where(alpha > 1e-5)[0][0]
    b = y[sv_idx] - np.dot(w, X[sv_idx])

    return w, b

def linear_svm_predict(X, w, b):
    return np.sign(np.dot(X, w) + b)
