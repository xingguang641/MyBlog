import numpy as np
from scipy.optimize import minimize
np.random.seed(42)
X_train = np.linspace(-5, 5, 12).reshape(-1, 1)
y_train = np.sin(X_train) + 0.3 * np.random.randn(*X_train.shape)


# 定义 RBF 核函数
def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1); X2 = np.atleast_2d(X2)
    sqdist = np.sum(X1**2, 1).reshape(-1, 1) + np.sum(X2**2, 1) - 2 * X1 @ X2.T
    return variance * np.exp(-0.5 / (length_scale**2) * sqdist)

class GaussianProcessRegressor:
    def __init__(self, kernel, noise=1e-6):
        self.kernel = kernel
        self.noise = noise
        self.is_fit = False

    def fit(self, X_train, y_train):
        self.X_train = np.atleast_2d(X_train)
        self.y_train = np.atleast_2d(y_train).reshape(-1, 1)
        K = self.kernel(self.X_train, self.X_train)
        K_y = K + self.noise * np.eye(len(self.X_train))
        self.L = np.linalg.cholesky(K_y)
        self.alpha = np.linalg.solve(self.L.T, np.linalg.solve(self.L, self.y_train))
        self.is_fit = True

    def predict(self, X_test, return_cov=False):
        if not self.is_fit:
            raise RuntimeError("模型尚未训练，请先调用 fit()。")
        X_test = np.atleast_2d(X_test)
        K_s = self.kernel(self.X_train, X_test)
        K_ss = self.kernel(X_test, X_test)
        mu = K_s.T @ self.alpha
        v = np.linalg.solve(self.L, K_s)
        cov = K_ss - v.T @ v
        if return_cov:
            return mu.ravel(), cov
        else:
            return mu.ravel()

    def log_marginal_likelihood(self):
        y = self.y_train
        L = self.L
        n = len(y)
        term1 = -0.5 * y.T @ self.alpha
        term2 = -np.sum(np.log(np.diag(L)))
        term3 = -0.5 * n * np.log(2 * np.pi)
        return (term1 + term2 + term3).ravel()[0]

# 超参数优化函数
def optimize_rbf_hyperparameters(X_train, y_train, noise=0.1**2):
    def objective(params):
        # 对数变换保证参数 >0
        length_scale = np.exp(params[0])
        variance = np.exp(params[1])
        kernel = lambda X1, X2: rbf_kernel(X1, X2, length_scale=length_scale, variance=variance)
        gp = GaussianProcessRegressor(kernel=kernel, noise=noise)
        gp.fit(X_train, y_train)
        return -gp.log_marginal_likelihood()

    res = minimize(objective, x0=np.log([1.0, 1.0]), bounds=[(-5, 5), (-5, 5)])
    best_length_scale, best_variance = np.exp(res.x)
    return best_length_scale, best_variance

# 执行代码
noise = 0.1**2
if __name__ == "__main__":
    # 优化所有核参数
    best_l, best_v = optimize_rbf_hyperparameters(X_train, y_train, noise=noise)
    print(f"优化得到的 length_scale: {best_l:.4f}, variance: {best_v:.4f}")
    # 使用优化后的核参数重新训练模型
    gp = GaussianProcessRegressor(
        kernel=lambda x, y: rbf_kernel(x, y, length_scale=best_l, variance=best_v),
        noise=noise
    )
    gp.fit(X_train, y_train)

    # 预测过程
    X_test = np.linspace(-6, 6, 200).reshape(-1, 1)
    mean, cov = gp.predict(X_test, return_cov=True)
    std = np.sqrt(np.diag(cov))
    print("Posterior mean (前5个):", mean[:5])
    print("Posterior std  (前5个):", std[:5])
    print("Log Marginal Likelihood:", gp.log_marginal_likelihood())
