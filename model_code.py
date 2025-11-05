import numpy as np
from collections import defaultdict
train_data = [
    (['The', 'capital', 'of', 'France'], ['B-LOC', 'O', 'O', 'B-LOC']),
    (['The', 'president', 'of', 'USA'], ['B-LOC', 'O', 'O', 'B-LOC']),
    (['I', 'love', 'Paris'], ['O', 'O', 'B-LOC'])
]


# 特征提取函数
def extract_features(sentence, index):
    features = {
        'word': sentence[index],
        'is_capitalized': sentence[index][0].isupper(),
        'is_digit': sentence[index].isdigit(),
        'word[-3:]': sentence[index][-3:],
    }
    # 上一个词
    if index > 0:
        features['prev_word'] = sentence[index - 1]
    # 下一个词
    if index < len(sentence) - 1:
        features['next_word'] = sentence[index + 1]
    return features

class CRF:
    def __init__(self):
        self.weights = defaultdict(float)
        self.transition_weights = defaultdict(float)
    
    def _features_to_key(self, features):
        return tuple(sorted(features.items()))
    
    def _get_feature_score(self, features):
        feature_key = self._features_to_key(features)
        return self.weights.get(feature_key, 0)

    def train(self, data, epochs=10, learning_rate=0.1):
        for epoch in range(epochs):
            for sentence, labels in data:
                # 计算每个单词的特征和标签得分
                for i in range(len(sentence)):
                    features = extract_features(sentence, i)
                    feature_score = self._get_feature_score(features)
                    feature_key = self._features_to_key(features)
                    # 计算特征的得分并更新权重
                    self.weights[feature_key] += learning_rate
                # 更新转移权重
                for i in range(1, len(labels)):
                    transition_key = (labels[i-1], labels[i])
                    self.transition_weights[transition_key] += learning_rate
            # 打印当前轮次的训练进度
            print(f'Epoch {epoch + 1} complete.')

    def viterbi_decode(self, sentence):
        n = len(sentence)
        dp = np.zeros((n, len(self.transition_weights)))
        backpointer = np.zeros((n, len(self.transition_weights)), dtype=int)
        # 初始化第一列：根据特征和初始转移权重
        for i in range(len(self.transition_weights)):
            features = extract_features(sentence, 0)
            dp[0][i] = self._get_feature_score(features) + self.transition_weights.get(('<START>', i), 0)
        # 动态规划：计算每个位置的最优标签路径
        for i in range(1, n):
            for j in range(len(self.transition_weights)):
                max_score = -float('inf')
                max_index = -1
                for k in range(len(self.transition_weights)):
                    features = extract_features(sentence, i)
                    score = dp[i-1][k] + self.transition_weights.get((k, j), 0) + self._get_feature_score(features)
                    if score > max_score:
                        max_score = score
                        max_index = k
                dp[i][j] = max_score
                backpointer[i][j] = max_index
        # 回溯：找到最优标签序列
        best_path = []
        best_state = np.argmax(dp[n-1])
        best_path.append(best_state)
        for i in range(n-2, -1, -1):
            best_state = backpointer[i+1][best_state]
            best_path.insert(0, best_state)

        return best_path

    def predict(self, sentence):
        predictions = []
        for i in range(len(sentence)):
            features = extract_features(sentence, i)
            score = self._get_feature_score(features)
            predictions.append(score)
        return predictions


# 执行代码
if __name__ == "__main__":
    crf_model = CRF()
    crf_model.train(train_data, epochs=10)

    test_sentence = ['I', 'love', 'Paris']
    predictions = crf_model.predict(test_sentence)
    print(f'Predictions: {predictions}')

    # 使用 Viterbi 解码获取标签序列
    best_path = crf_model.viterbi_decode(test_sentence)
    print(f'Predicted path (labels): {best_path}')