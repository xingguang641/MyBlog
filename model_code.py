import numpy as np

class ExtendedKalmanFilter:
    def __init__(self, f, F_jacobian, h, H_jacobian, Q, R, x0, P0):
        self.f = f; self.F_jacobian = F_jacobian; self.Q = Q
        self.h = h; self.H_jacobian = H_jacobian; self.R = R

        self.x = x0 # 后验均值
        self.P = P0 # 后验协方差

    def predict(self, u=None):
        if u is None:
            u = np.zeros((1,))
        # 状态预测
        self.x = self.f(self.x, u)
        # 协方差预测
        F = self.F_jacobian(self.x, u)
        self.P = F @ self.P @ F.T + self.Q
        return self.x, self.P

    def update(self, z):
        # 雅可比矩阵
        H = self.H_jacobian(self.x)
        # 卡尔曼增益
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        # 状态更新
        y = z - self.h(self.x)
        self.x = self.x + K @ y
        # 协方差更新
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ H) @ self.P
        return self.x, self.P, K


