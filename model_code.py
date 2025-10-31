import numpy as np
rng = np.random.RandomState(0)
obs_seq = np.random.randint(0, 3, size=50)


def _normalize(arr, axis=None, eps=1e-12):
    s = arr.sum(axis=axis, keepdims=True)
    s = np.maximum(s, eps)
    return arr / s

def _logsumexp(a, axis=None):
    a_max = np.max(a, axis=axis, keepdims=True)
    res = a_max + np.log(np.sum(np.exp(a - a_max), axis=axis, keepdims=True))
    if axis is None:
        return res.squeeze()
    return res

class HMM:
    def __init__(self, n_states, n_obs, seed=None):
        rng = np.random.RandomState(seed)
        self.n_states = n_states
        self.n_obs = n_obs
        # 初始化参数 π, A, B
        self.pi = _normalize(rng.rand(n_states))
        self.A = _normalize(rng.rand(n_states, n_states), axis=1)
        self.B = _normalize(rng.rand(n_states, n_obs), axis=1)

    # 发射概率
    def _emission_logprob(self, obs):
        assert obs.dtype.kind in 'iu', "Discrete observations must be integer dtype"
        logB = np.log(self.B[:, obs].T + 1e-12)
        return logB

    # 前向算法
    def _forward_log(self, obs):
        logA = np.log(self.A + 1e-12)
        logpi = np.log(self.pi + 1e-12)
        logB = self._emission_logprob(obs)
        T, S = logB.shape
        alpha = np.zeros((T, S))
        alpha[0] = logpi + logB[0]
        for t in range(1, T):
            a = alpha[t - 1][:, None] + logA
            alpha[t] = _logsumexp(a, axis=0).ravel() + logB[t]
        return alpha

    # 后向算法
    def _backward_log(self, obs):
        logA = np.log(self.A + 1e-12)
        logB = self._emission_logprob(obs)
        T, S = logB.shape
        beta = np.zeros((T, S))
        beta[T - 1] = 0.0
        for t in range(T - 2, -1, -1):
            b = logA + (logB[t + 1] + beta[t + 1])[None, :]
            beta[t] = _logsumexp(b, axis=1).ravel()
        return beta

    # 前后向算法（得到 gamma）
    def forward_backward(self, obs):
        alpha = self._forward_log(obs)
        beta = self._backward_log(obs)
        loggamma = alpha + beta
        loggamma -= _logsumexp(loggamma, axis=1)
        return np.exp(loggamma)

    # 计算对数似然
    def score(self, obs):
        alpha = self._forward_log(obs)
        return float(_logsumexp(alpha[-1]))

    # 维特比算法
    def viterbi(self, obs):
        logA = np.log(self.A + 1e-12)
        logpi = np.log(self.pi + 1e-12)
        logB = self._emission_logprob(obs)
        T, S = logB.shape
        delta = np.zeros((T, S))
        psi = np.zeros((T, S), dtype=int)
        delta[0] = logpi + logB[0]
        for t in range(1, T):
            val = delta[t - 1][:, None] + logA
            psi[t] = np.argmax(val, axis=0)
            delta[t] = np.max(val, axis=0) + logB[t]
        states = np.zeros(T, dtype=int)
        states[T - 1] = np.argmax(delta[T - 1])
        for t in range(T - 2, -1, -1):
            states[t] = psi[t + 1, states[t + 1]]
        return states

    # Baum-Welch（EM算法）
    def fit(self, sequences, max_iter=100, tol=1e-4, verbose=False):
        prev_ll = None
        for it in range(max_iter):
            pi_count = np.zeros(self.n_states)
            A_count = np.zeros((self.n_states, self.n_states))
            B_count = np.zeros((self.n_states, self.n_obs))
            total_ll = 0.0
            # E-step: compute posteriors of hidden states
            for obs in sequences:
                T = len(obs)
                alpha = self._forward_log(obs)
                beta = self._backward_log(obs)
                loggamma = alpha + beta
                loggamma -= _logsumexp(loggamma, axis=1)
                gamma = np.exp(loggamma)
                total_ll += _logsumexp(alpha[-1])
                logA = np.log(self.A + 1e-12)
                logB = self._emission_logprob(obs)
                xi_sum = np.zeros((self.n_states, self.n_states))
                for t in range(T - 1):
                    l = alpha[t][:, None] + logA + (logB[t + 1] + beta[t + 1])[None, :]
                    l -= _logsumexp(l)
                    xi_sum += np.exp(l)
                pi_count += gamma[0]
                A_count += xi_sum
                for t in range(T):
                    B_count[:, obs[t]] += gamma[t]
            # M-step: update parameters
            self.pi = _normalize(pi_count)
            self.A = _normalize(A_count, axis=1)
            self.B = _normalize(B_count, axis=1)
            total_ll = float(total_ll)
            if verbose:
                print(f"Iter {it+1}: log-likelihood = {total_ll:.6f}")
            if prev_ll is not None and abs(total_ll - prev_ll) < tol:
                break
            prev_ll = total_ll
        return self


# 执行代码
if __name__ == '__main__':
    model = HMM(n_states=2, n_obs=3, seed=0)
    model.fit([obs_seq], max_iter=50, verbose=True)

    print('Trained pi:', model.pi)
    print('Trained A :', model.A)
    print('Trained B :', model.B)
    print('Viterbi   :', model.viterbi(obs_seq)[:20])
    print('Log-lik   :', model.score(obs_seq))
