import numpy as np
from sklearn.datasets import make_classification
X, y = make_classification(
    n_samples=500,
    n_features=5,
    n_classes=2,
    n_informative=5,
    n_redundant=0,
    random_state=42
)


class GDA:
    def __init__(self):
        self.phi = None
        self.mu0 = None
        self.mu1 = None
        self.sigma = None

    # 求解出四个关键参数
    def fit(self, X, y):
        m, _ = X.shape

        # 1. 计算先验概率 phi
        self.phi = np.mean(y)

        # 2. 计算各类别均值 mu0, mu1
        self.mu0 = np.mean(X[y == 0], axis=0)
        self.mu1 = np.mean(X[y == 1], axis=0)

        # 3. 向量化计算协方差矩阵 Sigma
        diff0 = X[y == 0] - self.mu0
        diff1 = X[y == 1] - self.mu1
        self.sigma = (diff0.T @ diff0 + diff1.T @ diff1) / m

    # 求解出线性判别函数的两个参数
    def predict_proba(self, X):
        inv_sigma = np.linalg.inv(self.sigma)
        
        # 线性判别函数参数
        w = inv_sigma @ (self.mu1 - self.mu0)

        b = (
              np.log(self.phi / (1 - self.phi))
            + 0.5 * self.mu0.T @ inv_sigma @ self.mu0
            - 0.5 * self.mu1.T @ inv_sigma @ self.mu1
        )
        
        return 1 / (1 + np.exp(-(X @ w + b)))

    def predict(self, X):
        return (self.predict_proba(X) >= 0.5).astype(int)


# 执行代码
if __name__ == "__main__":    
    model = GDA()
    model.fit(X, y)
    y_pred = model.predict(X)
    print("准确率：", np.mean(y_pred == y))
