import numpy as np

class ParticleFilter:
    def __init__(self, N, f, h, Q, R, x0_prior):
        self.N = N
        self.f = f; self.Q = Q
        self.h = h; self.R = R

        # 初始化粒子集合
        self.particles = x0_prior(N)
        self.weights = np.ones(N) / N

    def predict(self):
        for i in range(self.N):
            w = np.random.multivariate_normal(np.zeros(self.Q.shape[0]), self.Q)
            self.particles[i] = self.f(self.particles[i]) + w

    def update(self, z):
        for i in range(self.N):
            v = z - self.h(self.particles[i])
            # 高斯观测似然
            likelihood = np.exp(-0.5 * v.T @ np.linalg.inv(self.R) @ v)
            likelihood /= np.sqrt((2*np.pi)**len(z) * np.linalg.det(self.R))
            self.weights[i] *= likelihood
        # 归一化权重
        self.weights /= np.sum(self.weights)

    def resample(self):
        indices = np.random.choice(self.N, size=self.N, p=self.weights)
        self.particles = self.particles[indices]
        self.weights.fill(1.0 / self.N)

    def estimate(self):
        return np.average(self.particles, weights=self.weights, axis=0)
