from typing import List
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
train_sents = [
    ['John', 'loves', 'Mary'],
    ['Mary', 'hates', 'Bob'],
    ['Bob', 'likes', 'Alice'],
]
train_tags = [
    ['NNP', 'VBZ', 'NNP'],
    ['NNP', 'VBZ', 'NNP'],
    ['NNP', 'VBZ', 'NNP'],
]


def default_feature_extractor(sentence: List[str], i: int, prev_tag: str) -> dict:
    token = sentence[i]
    features = {}
    features[f"word={token}"] = 1
    features[f"word_lower={token.lower()}"] = 1
    if len(token) >= 3:
        features[f"suffix3={token[-3:]}"] = 1
    features[f"is_title={token[0].isupper()}"] = 1
    features[f"is_digit={token.isdigit()}"] = 1
    # 前后词
    if i > 0:
        features[f"prev_word={sentence[i-1]}"] = 1
    else:
        features["BOS"] = 1
    if i < len(sentence)-1:
        features[f"next_word={sentence[i+1]}"] = 1
    else:
        features["EOS"] = 1
    # 把前一标签也作为一个特征（MEMM 的关键点）
    features[f"prev_tag={prev_tag}"] = 1
    return features

class MEMM:
    def __init__(self, feature_extractor=default_feature_extractor, solver='lbfgs', max_iter=200):
        self.feature_extractor = feature_extractor
        self.vec = DictVectorizer(sparse=True)
        self.clf = LogisticRegression(multi_class='multinomial', solver=solver, max_iter=max_iter)
        self.label_to_index = {}
        self.index_to_label = []
        self.fitted = False

    def _gather_training_instances(self, sents: List[List[str]], tags: List[List[str]]):
        X_dicts = []; y = []
        for sent, tag_seq in zip(sents, tags):
            for i in range(len(sent)):
                prev_tag = tag_seq[i-1] if i > 0 else '<START>'
                feats = self.feature_extractor(sent, i, prev_tag)
                X_dicts.append(feats)
                y.append(tag_seq[i])
        return X_dicts, y

    def fit(self, sents: List[List[str]], tags: List[List[str]]):
        X_dicts, y = self._gather_training_instances(sents, tags)
        # 记录标签映射
        labels = sorted(set(y))
        self.index_to_label = labels
        self.label_to_index = {lab: i for i, lab in enumerate(labels)}
        # vectorize
        X = self.vec.fit_transform(X_dicts)
        y_idx = np.array([self.label_to_index[lab] for lab in y])
        # 训练分类器
        self.clf.fit(X, y_idx)
        self.fitted = True
        return self

    def _local_log_probs(self, sentence: List[str], position: int, prev_tag: str) -> np.ndarray:
        feats = self.feature_extractor(sentence, position, prev_tag)
        X = self.vec.transform([feats])
        logp = self.clf.predict_log_proba(X)[0]
        return logp

    def viterbi(self, sentence: List[str]) -> List[str]:
        assert self.fitted, "模型尚未训练，请先调用 fit()"
        n_tags = len(self.index_to_label)
        T = len(sentence)
        # dp[t, j] = 最佳路径到位置 t 且标签为 j 的对数概率
        dp = np.full((T, n_tags), -np.inf)
        backptr = np.zeros((T, n_tags), dtype=int)
        # 初始步 t=0，prev_tag = '<START>'
        for j in range(n_tags):
            cur_tag = self.index_to_label[j]
            logp = self._local_log_probs(sentence, 0, '<START>')
            dp[0, j] = logp[j]
            backptr[0, j] = -1

        # 递推
        for t in range(1, T):
            for j in range(n_tags):
                cur_tag = self.index_to_label[j]
                best_score = -np.inf
                best_prev = 0
                # 对每个可能的前一标签 i
                for i in range(n_tags):
                    prev_tag = self.index_to_label[i]
                    # 计算在 prev_tag 下转移到 cur_tag 的 log 概率
                    logp = self._local_log_probs(sentence, t, prev_tag)
                    score = dp[t-1, i] + logp[j]
                    if score > best_score:
                        best_score = score
                        best_prev = i
                dp[t, j] = best_score
                backptr[t, j] = best_prev

        # 回溯
        best_last = int(np.argmax(dp[T-1]))
        tags_idx = [best_last]
        for t in range(T-1, 0, -1):
            best_prev = backptr[t, tags_idx[-1]]
            tags_idx.append(int(best_prev))
        tags_idx.reverse()
        return [self.index_to_label[i] for i in tags_idx]

    def predict(self, sentence: List[str]) -> List[str]:
        return self.viterbi(sentence)


# 执行代码
if __name__ == '__main__':
    memm = MEMM()
    memm.fit(train_sents, train_tags)

    test = ['Alice', 'loves', 'Bob']
    print('Test sentence:', test)
    pred = memm.predict(test)
    print('Predicted tags:', pred)



