import numpy as np
from scipy.optimize import minimize
from scipy.linalg import cho_factor, cho_solve
np.random.seed(42)
X_train = np.linspace(-5, 5, 20).reshape(-1, 1)
y_train = (X_train[:, 0] > 0).astype(int)


def rbf_kernel(X1, X2, length_scale=1.0, variance=1.0):
    X1 = np.atleast_2d(X1)
    X2 = np.atleast_2d(X2)
    sqdist = (
        np.sum(X1**2, 1).reshape(-1, 1)
        + np.sum(X2**2, 1)
        - 2 * X1 @ X2.T
    )
    return variance * np.exp(-0.5 / length_scale**2 * sqdist)

class GaussianProcessClassifier:
    def __init__(self, kernel, max_iter=20, tol=1e-6):
        self.kernel = kernel
        self.max_iter = max_iter
        self.tol = tol
        self.is_fit = False

    @staticmethod
    def sigmoid(a):
        return 1.0 / (1.0 + np.exp(-a))

    def fit(self, X_train, y_train):
        self.X_train = np.atleast_2d(X_train)
        self.y_train = y_train.reshape(-1, 1)
        n = len(y_train)

        def K_solve(v):
            return cho_solve(K_chol, v)

        self.K = self.kernel(self.X_train, self.X_train)
        f = np.zeros((n, 1))
        K_chol = cho_factor(self.K + 1e-6 * np.eye(n))
        for _ in range(self.max_iter):
            pi = self.sigmoid(f)
            W = (pi * (1 - pi)).flatten()

            grad = self.y_train - pi - K_solve(f)
            H = np.diag(W) + cho_solve(K_chol, np.eye(n))

            try:
                H_chol = cho_factor(H)
                delta = cho_solve(H_chol, grad)
            except:
                delta = np.linalg.solve(H, grad)

            f_new = f + delta
            if np.max(np.abs(delta)) < self.tol:
                f = f_new
                break
            f = f_new

        self.f_map = f
        self.W = (pi * (1 - pi)).flatten()

        H = np.diag(self.W) + cho_solve(K_chol, np.eye(n))
        H_chol = cho_factor(H)
        self.Sigma = cho_solve(H_chol, np.eye(n))

        self.K_chol = K_chol
        self.is_fit = True

    def predict(self, X_test):
        if not self.is_fit:
            raise RuntimeError("请先调用 fit() 训练模型。")

        X_test = np.atleast_2d(X_test)
        K_s = self.kernel(self.X_train, X_test)
        m_star = K_s.T @ cho_solve(self.K_chol, self.f_map)

        # predictive variance approx
        W_inv = np.diag(1.0 / (self.W + 1e-12))
        A = self.K + W_inv
        A_chol = cho_factor(A)

        v = cho_solve(A_chol, K_s)
        k_ss = self.kernel(X_test, X_test).diagonal()
        s2 = k_ss - np.sum(K_s * v, axis=0)

        # logistic integral approximation
        denom = np.sqrt(1 + np.pi * s2 / 8)
        prob = self.sigmoid(m_star.flatten() / denom)
        return prob

    def log_marginal_likelihood(self):
        f = self.f_map
        y = self.y_train
        W = self.W
        pi = self.sigmoid(f)

        log_lik = np.sum(
            y * np.log(pi + 1e-12) + (1 - y) * np.log(1 - pi + 1e-12)
        )

        K_chol = self.K_chol
        Kinv_f = cho_solve(K_chol, f)
        log_prior = -0.5 * f.T @ Kinv_f

        H = np.diag(W) + cho_solve(K_chol, np.eye(len(W)))
        H_chol = cho_factor(H)
        log_det_H = 2 * np.sum(np.log(np.diag(H_chol[0])))

        log_Z = log_lik + log_prior - 0.5 * log_det_H
        return log_Z.flatten()[0]

def optimize_rbf_hyperparameters(X_train, y_train):
    def objective(params):
        length_scale = np.exp(params[0])
        variance = np.exp(params[1])
        kernel = lambda X1, X2: rbf_kernel(
            X1, X2, length_scale=length_scale, variance=variance
        )
        gpc = GaussianProcessClassifier(kernel)
        gpc.fit(X_train, y_train)
        return -gpc.log_marginal_likelihood()

    res = minimize(
        objective,
        x0=np.log([1.0, 1.0]),
        bounds=[(-5, 5), (-5, 5)]
    )
    best_l, best_v = np.exp(res.x)
    return best_l, best_v


# 执行代码
if __name__ == "__main__":
    best_l, best_v = optimize_rbf_hyperparameters(X_train, y_train)
    print(f"最佳 length_scale = {best_l:.4f}, variance = {best_v:.4f}")
    kernel = lambda X1, X2: rbf_kernel(X1, X2, length_scale=best_l, variance=best_v)
    gpc = GaussianProcessClassifier(kernel)
    gpc.fit(X_train, y_train)

    X_test = np.linspace(-6, 6, 200).reshape(-1, 1)
    prob = gpc.predict(X_test)
    print("前 5 个预测概率：", prob[:5])
    print("Log Marginal Likelihood（Laplace）：", gpc.log_marginal_likelihood())
