import numpy as np
np.random.seed(0)
X1 = np.random.multivariate_normal([0,0], [[1,0],[0,1]], 100)
X2 = np.random.multivariate_normal([5,5], [[1,0],[0,1]], 100)
X = np.vstack([X1, X2])


# 计算多维高斯概率密度函数
def gaussian_pdf(x, mean, cov):
    D = x.shape[0]
    cov_det = np.linalg.det(cov)
    cov_inv = np.linalg.inv(cov)
    norm_const = 1.0 / np.sqrt((2 * np.pi)**D * cov_det)
    diff = x - mean
    return norm_const * np.exp(-0.5 * diff.T @ cov_inv @ diff)

class GMM:
    def __init__(self, n_components, tol=1e-6, max_iter=100):
        self.K = n_components
        self.tol = tol
        self.max_iter = max_iter

    def fit(self, X):
        # 初始化参数
        N, _ = X.shape
        self.p = np.ones(self.K) / self.K
        self.mu = X[np.random.choice(N, self.K, replace=False)]
        self.Sigma = np.array([np.cov(X, rowvar=False)] * self.K)

        log_likelihood_old = 0
        for _ in range(self.max_iter):
            # E-step
            gamma = np.zeros((N, self.K))
            for i in range(N):
                for k in range(self.K):
                    gamma[i, k] = self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
                gamma[i, :] /= np.sum(gamma[i, :])

            # M-step
            N_k = np.sum(gamma, axis=0)
            self.p = N_k / N
            self.mu = (gamma.T @ X) / N_k[:, np.newaxis]
            for k in range(self.K):
                diff = X - self.mu[k]
                self.Sigma[k] = (gamma[:, k][:, np.newaxis] * diff).T @ diff / N_k[k]

            # 计算对数似然函数判断是否收敛
            log_likelihood = 0
            for i in range(N):
                temp = 0
                for k in range(self.K):
                    temp += self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
                log_likelihood += np.log(temp)

            if np.abs(log_likelihood - log_likelihood_old) < self.tol:
                break
            log_likelihood_old = log_likelihood

        return self

    # 软预测函数
    def predict_proba(self, X):
        N = X.shape[0]
        gamma = np.zeros((N, self.K))
        for i in range(N):
            for k in range(self.K):
                gamma[i, k] = self.p[k] * gaussian_pdf(X[i], self.mu[k], self.Sigma[k])
            gamma[i, :] /= np.sum(gamma[i, :])
        return gamma

    # 硬预测函数
    def predict(self, X):
        return np.argmax(self.predict_proba(X), axis=1)


# 执行代码
if __name__ == "__main__":
    gmm = GMM(n_components=2)
    gmm.fit(X)

    labels = gmm.predict(X)
    print("混合系数 p:", gmm.p)
    print("均值 mu:", gmm.mu)
    print("协方差 Sigma:", gmm.Sigma)

