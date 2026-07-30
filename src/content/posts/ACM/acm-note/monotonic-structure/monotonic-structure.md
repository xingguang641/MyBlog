---
title: 【ACM 算法随笔】单调数据结构的应用
published: 2025-11-27
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: true
---

# 单调数据结构介绍

在设计算法时，识别并利用题目隐含的 **单调性** 是优化性能的关键。这种性质通常意味着数据内部存在特定的偏序关系，或者最优决策点具有不可逆的移动趋势。为了高效地捕捉并利用这种结构化信息，我们通常需要借助单调数据结构。它们能够动态地维护一组具有单调特性的候选集合，通过实时剔除无效的冗余数据，帮助我们在大规模数据中精准锁定目标信息。

这类数据结构的核心在于 **决策剪枝** 。无论是寻找元素两侧最近极值的 **单调栈** ，还是维护区间最值的 **单调队列** ，亦或是动态调整边界的**滑动窗口** ，其精髓都在于通过利用元素间的单调关系，将原本需要多次遍历的暴力检索优化为均摊常数级的快速响应。通过这种结构化的约束，复杂的区间操作被大幅压缩，使得算法在处理海量信息流时依然能够保持极高的运行效率。

## 单调滑动窗口

在各种数组与序列相关的题目中，滑动窗口几乎是最常见、也最实用的技巧之一。它的核心做法很简单：通过两个指针在序列上同步向前移动，始终维护一个当前的区间，并在移动的过程中不断检查区间是否满足题目的要求。不过，滑动窗口并不是可以随意使用的。它之所以高效，是因为许多问题本身具备一种关于窗口长度的单调性。典型的情形是：**窗口越长越不满足条件，或者窗口越长越容易满足条件** 。只要存在这种单调性，我们在扩张右端点的时候，就能确保左端点不会回退，从而保证整个过程不会出现重复扫描的情况。

其中一个典型的例子是「区间和不超过 $k$ 」。如果数组中的元素均为非负整数，那么随着窗口长度增加，窗口累加和只会上升而不会下降。这样一来，窗口越短就越满足条件，我们就可以放心地在累加和超过上限时收缩左端点，从而在线性时间内完成整个搜索。但如果数组中存在负整数，窗口累加和便不再单调，此时窗口累加和随着窗口的扩张反而会因负数的加入而下降。由于单调性被破坏，滑动窗口便失去原本的高效性，需要换用[其他算法](#寻找累加和至多为k的最长数组)。

![滑动窗口图像](src\content\posts\ACM\acm-note\monotonic-structure\滑动窗口1.png)

对于更复杂的滑动窗口极值问题，简单的双指针配合变量记录的方式已无法胜任。因为当旧的极值随左端点滑出窗口时，我们需要在 $O(1)$ 时间内找到新的极值，这时就需要配合 **单调队列** 进行维护。单调队列通过在队尾剔除冗余数据，强制保证队列内部元素的单调性，从而保证队头始终指向当前窗口的局部极值。这种结构将原本需要 $O(k)$ 的区间检索优化到了均摊 $O(1)$ ，完美契合了滑动窗口对实时性的要求。

对于滑动窗口中位数问题，情况则更具挑战性：由于中位数对数值的排序位置高度敏感，简单的单调性维护已不足以实现 $O(1)$ 的查询。这类问题通常需要借鉴[数据流中位数](https://xingguang641.com/posts/acm/acm-note/priority-queue/#数据流中位数问题)中经典的对顶堆架构。在窗口滑动过程中，我们不仅要动态维护两个堆的平衡以锁定窗口的中间值，还需额外引入延迟删除的机制来处理滑出窗口的过期元素。这种将双堆平衡与窗口移动相结合的策略，能将复杂度稳定在 $O(n \log k)$ ，是处理滑动窗口中位数问题的利器。

## 单调栈与队列

在处理序列相关问题时，我们不仅要关注数据的输入顺序，更需要 **在扫描过程中持续维护** 某种局部最优或特定的约束关系。为了高效地记录并更新这些结构化信息，单调栈与单调队列成为了核心工具。它们的核心思路是 **在容器内部强制维持单调性** ，通过预见性的筛选，只保留在后续状态中仍具备竞争力的有效元素，而果断剔除那些在当前逻辑下已失去价值的候选者。这种对冗余信息的实时清理机制，将复杂的区间关系巧妙地压缩进了线性处理流程中，从而实现了均摊 $O(1)$ 的极高处理效率。

从结构上看，栈与队列同属线性容器，但操作维度的不同决定了它们的应用边界。栈严格遵循后进先出的逻辑，仅允许在单端进行存取；而双端队列则拥有更灵活的进出机制。这种接口能力的差异，使得它们在处理单调性问题时各司其职：**单调栈** 更侧重于捕捉元素间的相互指向关系，如寻找左右两侧的最近极值；而 **单调队列** 则与滑动窗口紧密结合，专注于维护动态区间内的实时最值。

**单调栈** 常用于解决 “下一个更大元素” 、“下一个更小元素” 等结构性问题。借助其单端更新的特性，我们可以在扫描序列时强制保持栈内的元素递增或递减。每当新元素尝试入栈却违反单调性时，栈顶那些比它更差的元素就会被永久弹出，因为对于后续的所有元素而言，当前的这个新元素不仅数值更优，而且位置更近，完全替代了旧元素的贡献。通过这种方式，我们可以在一次遍历中确定每个元素左右两侧最近的极值边界。

![单调栈图像](src\content\posts\ACM\acm-note\monotonic-structure\单调栈1.png)

**单调队列** 与滑动窗口的结合非常紧密，主要用于在窗口滑动的过程中实时维护区间的极值。不同于单调栈的单端操作，单调队列需要随着窗口的推进执行双重筛选：首先需要在队头弹出已经滑出窗口范围的过期元素；随后在队尾剔除那些数值不如新元素、且生存周期也更短的冗余元素。这种机制确保队列内部始终维持着一段严格单调的最优候选集合，使我们能够随时以 $O(1)$ 的代价，直接通过队头获取当前窗口内的全局最值。

![单调队列图像](src\content\posts\ACM\acm-note\monotonic-structure\单调队列1.png)

归根到底，无论使用单调栈还是单调队列，其目的都是一致的：**利用数据之间的偏序关系与时序关系，主动压缩掉无效的候选集合，从而在一次遍历中完成本应需要多重循环才能实现的关系维护** 。它们不仅是简单的容器，更是一种动态过滤冗余信息的策略。通过将复杂的结构化扫描转化为简单的入队入栈操作，它们为涉及局部最值、区间判定以及动态规划状态转移优化等问题提供了极为高效且简洁的解决途径。

---

# 普通滑动窗口模型

在处理数组或字符串的 **子区间** 相关问题时，**滑动窗口** 是一种兼具简洁与高效的经典算法技巧。其核心逻辑在于通过维护两个同向移动的指针，即左边界 $l$ 与右边界 $r$ ，在序列上动态地维护一个连续的窗口范围。通过这种双指针的协作，算法能够实时追踪区间内的属性变化，在不需要回退的前提下，精准定位符合约束条件的子区间，为后续的处理提供一个清晰且不断演进的观测窗口。

该模型的应用精髓在于对问题 **单调性** 的深度挖掘。在执行过程中，右指针 $r$ 主动向右推进以引入新元素，驱动窗口内的状态产生单向趋势变化。一旦窗口状态触及或突破预设的边界条件，如总和超过目标值 $k$ ，算法便由扩张转入收缩。通过左指针 $l$ 的右移来剔除陈旧元素，这种由左端的被动收缩来抵消右端扩张带来的状态偏移，本质上是在线性空间内寻找一种持续演进的 **动态平衡** 。

这种机制巧妙利用了区间处理的连续性，通过 **增量更新** 彻底告别了对重叠区域的重复计算。它将原本需要 $O(n^2)$ 暴力枚举的搜索空间大幅压缩至线性时间，在整个算法周期内，每个元素经历一进一出的完整过程，左右指针均遵循只进不退的原则，确保了每个数据点最多仅被访问两次。这种极致的执行效率使其成为处理大规模数据下区间约束问题的 **首选方案** ，并在各种高性能数据过滤场景中展现出卓越的逻辑美感。

## 最长的休息间隔

[题目链接](https://leetcode.cn/problems/reschedule-meetings-for-maximum-free-time-i/description/)

### Problem Statement

一个公司有 $n$ 个会议，第 $i$ 个会议的开始时间为 `startTime[i]` ，结束时间为 `endTime[i]` 。所有的会议都在一天内进行，该天的总时长为 `eventTime` 。

你可以通过移动会议来重新安排日程，但必须遵守以下规则：
1. 会议的 **持续时间** 保持不变。
2. 会议之间的 **相对顺序** 必须保持不变，且会议之间不能重叠。
3. 你最多可以移动 **k** 个会议。
4. 移动后所有会议必须在 $[0, \text{eventTime}]$ 范围内。

你的目标是寻找一种移动方案，使得日程中出现一段 **最长** 的连续空余时间。返回这段空余时间的最大长度。

### Constraints

- $1 \leq eventTime \leq 10^9$
- $n == startTime.length == endTime.length$
- $2 \leq n \leq 10^5$
- $1 \leq k \leq n$
- $0 \leq startTime[i] < endTime[i] \leq eventTime$
- 会议按 `startTime` 升序排列且不重叠

### Input

输入包含三行：

- 第一行包含三个整数 $n$ 、 $k$ 和 $eventTime$ 。
- 第二行包含 $n$ 个整数，表示每个会议的开始时间 $startTime$ 。
- 第三行包含 $n$ 个整数，表示每个会议的结束时间 $endTime$ 。

> $n \quad k \quad eventTime$
> 
> $startTime_0 \quad startTime_1 \quad \ldots \quad startTime_{n-1}$
> 
> $endTime_0 \quad endTime_1 \quad \ldots \quad endTime_{n-1}$

### Output

输出一个整数，表示重新安排后能获得的最大连续空余时间长度。

### Sample Input 1

```txt showLineNumbers=false
2 1 5
1 3
2 5
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
3 1 10
0 2 9
1 4 10
```

### Sample Output 2

```txt showLineNumbers=false
6
```

## 题目要点解析

这道题的核心在于 **视角转换**：与其纠结于会议具体的起始与结束时间，不如将注意力转向会议之间的空隙。在 $n$ 个会议的序列中，天然存在着 $n+1$ 个间隔（包括首尾与边界的距离）。当我们拥有 $k$ 次移动会议的机会时，等同于我们可以撤走夹在某些间隔中间的 $k$ 个会议，从而将连续的 **k + 1 个间隔** 强行汇聚成一段完整的空余时间。

在具体实现上，我们可以将该问题转化为一个标准的 **固定长度滑动窗口** 问题。我们预先提取出所有 $n+1$ 个间隔的长度并存入数组，随后利用大小为 $k+1$ 的窗口在数组上滑动。这种反向维护间隙而非正向维护会议的思路，极大地简化了题目中 “不改变相对顺序” 和 “不改变持续时间” 的复杂约束。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int n, k, eventTime;

int main() {
    cin >> n >> k;
    cin >> eventTime;

    vector<int> startTime(n), endTime(n);
    for (int i = 0; i < n; i++) cin >> startTime[i];
    for (int i = 0; i < n; i++) cin >> endTime[i];

    vector<int> nums;
    for (int i = 0; i < (int) startTime.size(); i++){
        if (i == 0) nums.push_back(startTime[0] - 0);
        else nums.push_back(startTime[i] - endTime[i - 1]);
    }
    nums.push_back(eventTime - endTime[(int) endTime.size() - 1]);

    ll ans = 0, curSum = 0;
    if (k > (int) nums.size()) {
        for (int i = 0; i < (int) nums.size(); i++){
            ans += nums[i];
        }
        cout << ans << endl;
    } else {
        for (int i = 0; i < k; i++){
            curSum += nums[i];
        }
        for (int i = k; i < (int) nums.size(); i++){
            curSum += nums[i];
            ans = max(ans, curSum);
            curSum -= nums[i - k];
        }
        cout << ans << endl;
    }
}
```

## 串联所有的单词

[题目链接](https://leetcode.cn/problems/substring-with-concatenation-of-all-words/)

### Problem Statement

给定一个字符串 `s` 和一个字符串数组 `words` 。`words` 中所有字符串的 **长度相同** 。

`s` 中的 **串联子串** 是指包含 `words` 中所有字符串以任意顺序排列连接而成的子串。

返回所有串联子串在 `s` 中的开始索引。你可以按 **任意顺序** 返回答案。

### Constraints

- $1 \leq s.length \leq 10^4$
- $1 \leq words.length \leq 5000$
- $1 \leq words[i].length \leq 30$
- $words[i]$ 和 $s$ 由小写英文字母组成

### Input

输入包含三行：

- 第一行包含一个字符串 $s$ 。
- 第二行包含一个整数 $m$ ，表示 $words$ 数组的长度。
- 第三行包含 $m$ 个字符串，由空格隔开，表示 $words$ 数组中的每个单词。

> $s$
> 
> $m$
> 
> $words_0 \quad words_1 \quad \ldots \quad words_{m-1}$

### Output

输出一行整数，表示所有符合条件的起始索引，以空格隔开；如果不存在答案，请输出 `-1` 。

### Sample Input 1

```txt showLineNumbers=false
barfoothefoobarman
2
foo bar
```

### Sample Output 1

```txt showLineNumbers=false
0 9
```

### Sample Input 2

```txt showLineNumbers=false
wordgoodgoodgoodbestword
4
word good best word
```

### Sample Output 2

```txt showLineNumbers=false
-1
```

### Sample Input 3

```txt showLineNumbers=false
barfoofoobarthefoobarman
3
foo bar the
```

### Sample Output 3

```txt showLineNumbers=false
6 9 12
```

## 题目要点解析

本题最核心的转化在于将原字符串 `s` 视为由若干个长度为 `len` 的单词块构成的序列。在这种视角下，问题便由复杂的子串匹配降维成了经典的 **计数滑动窗口** 问题。然而，由于单词的起始位置在原字符串中是连续的，单纯以 `len` 为步长进行一次扫描会忽略掉那些不从索引 $0$ 开始的划分情况。为了确保扫描的完备性，我们需要依次以 $0, 1, 2, \dots, len-1$ 作为起点分别进行 **偏移检测** 。这种多起点偏移的策略能够覆盖字符串中所有可能的单词切分方式，而 $len$ 之后的起点（如从 $len$ 开始）在逻辑上与其前面的起点完全对等，因此无需额外计算。

在具体的执行流程中，每一组偏移扫描都可以看作是一个 **独立的双指针滑动窗口** 过程。我们利用哈希表实时维护当前窗口内各单词的出现频次，右指针负责向右跳跃 `len` 个字符加入新单词。当窗口内某个单词的频率超过了目标需求时，左指针便开始向右收缩，不断删除左侧单词直至窗口重新合法。由于我们严格保证了窗口内没有任何单词超标，只要当前窗口内的单词总数 `curm` 恰好等于目标总数 `m` ，就说明此时的窗口必然是由 `words` 数组中所有单词的一种排列组合构成的，此时记录左边界对应的索引即可。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
int m; string s;

int main() {
    cin >> s; cin >> m;
    
    vector<string> words(m);
    unordered_map<string, int> cnts;
    for (int i = 0; i < m; i++) {
        cin >> words[i];
        cnts[words[i]]++;
    }

    int n = s.size();
    int len = words[0].size();
    vector<int> ans_indices;
    for (int i = 0; i < len; i++) {
        unordered_map<string, int> curCnt;
        int curm = 0; int left = i - len;
        for (int right = i; right + len <= n; right += len) {
            string str = s.substr(right, len);
            
            curCnt[str]++; curm++;
            while (curCnt[str] > cnts[str]) {
                left += len;
                string cur = s.substr(left, len);
                curCnt[cur]--;
                curm--;
            }

            if (curm == m) {
                ans_indices.push_back(left + len);
            }
        }
    }

    for (int i = 0; i < (int)ans_indices.size(); i++) {
        cout << ans_indices[i] << (i == (int)ans_indices.size() - 1 ? "" : " ");
    }
    cout << endl;
}
```

## 使二进制字符串交替的最少反转

[题目链接](https://leetcode.cn/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/)

### Problem Statement

给你一个二进制字符串 `s` 。你可以对字符串执行以下两种操作：

1. **删除**：删除字符串的第一个字符，并将其追加到字符串的末尾。
2. **反转**：选择字符串中的任一字符，将其从 `0` 反转为 `1` ，或者从 `1` 反转为 `0` 。

目标是使字符串 `s` 变为 **交替字符串** ，求所需的 **最少** 反转次数。

交替字符串定义为：字符序列中没有相邻的字符相等。

例如，`"01010"` 和 `"10101"` 是交替字符串，而 `"0110"` 不是。

### Constraints

- $1 \leq s.length \leq 10^5$
- `s[i]` 为 `'0'` 或 `'1'`

### Input

输入仅包含一行：

> $s$

### Output

输出一个整数，表示使 `s` 变为交替字符串所需的最少反转次数。

### Sample Input 1

```txt showLineNumbers=false
111000
```

### Sample Output 1

```txt showLineNumbers=false
2
```

### Sample Input 2

```txt showLineNumbers=false
010
```

### Sample Output 2

```txt showLineNumbers=false
0
```

### Sample Input 3

```txt showLineNumbers=false
1110
```

### Sample Output 3

```txt showLineNumbers=false
1
```

## 题目要点解析

操作 $1$ 的 **本质就是轮换** ，而处理轮换的常见方式是 **将原数组倍增后滑窗** 。当我们维持一个长度固定为 $n$ 的窗口在倍增数组上向右滑动时，窗口每滑动一次就等价于原数组进行一次轮换操作。通过这种方式，我们可以消除模拟轮换带来的高额时间复杂度。

对于交替字符串，其最终的目标形态本质上只有两种。一种是形如 `101010` 的字符串，另一种是形如 `010101` 的字符串。为了避免在滑动窗口的过程中对这两种目标形态分别进行复杂的分类讨论，我们可以巧妙地引入一个 **全局参考基准线** ，并采用 “错位映射” 的数学思想将它们统一起来。

我们不妨以第二种形式作为全局参考基准线，这意味着在目标基准线上，所有偶数下标对应的字符应当为 `'0'` ，所有奇数下标对应的字符应当为 `'1'` 。此时，我们将倍增字符串中的每一个字符与该基准线进行比对。如果当前字符不满足这个奇偶交替的规律，我们就将其视为一个错位点，也就是需要进行类型 $2$ 反转操作的位置。

随着窗口在倍增字符串上向右滑动，具体的错位映射逻辑会出现以下两种情况：

- 第一种情况，当子串左端点下标是偶数时。因为左端点在全局基准线上本来就是偶数位置，所以此时窗口内部的奇偶性与全局基准线 **完全对齐** 。这意味着如果我们想把这个子串变成 `010101` 形态，那些 **不符合** 全局基准线的字符就需要反转；如果我们想把它变成 `101010` 形态，那些 **符合** 全局基准线的字符就需要反转。

- 第二种情况，当子串左端点下标是奇数时。因为左端点在全局基准线上变成奇数位置，这导致整个窗口的奇偶性相对于全局基准线 **整体向右偏移 1 位** 。这意味着如果我们想把子串变成 `010101` 形态，那些 **符合** 全局基准线的字符就需要反转；如果我们想把它变成 `101010` 形态，那些 **不符合** 全局基准线的字符就需要反转。

在这两种情况中，由于窗口内的总字符数固定为 $n$ ，如果我们引入一个计数器 $cnt$ ，专门用来动态统计当前窗口内 **不符合** 全局基准线的错位点个数，那么当前窗口内 **符合** 全局基准线的字符个数自然就为 $n - cnt$ 。此时我们可以清晰地看到，无论子串的左端点下标是奇数还是偶数，其最小反转次数均可以通过以下公式统一表达：

$$
Ans = \min(cnt, n - cnt)
$$

利用这个核心公式，复杂的奇偶状态与目标分类被彻底消解。在接下来的滑动窗口过程中，我们只需要动态维护这个计数器 $cnt$ ，并不断用该公式的计算结果去更新全局最优解即可。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 获得最多的硬币

[题目链接](https://leetcode.cn/problems/maximum-coins-from-k-consecutive-bags/description/)

### Problem Statement

在一条数轴上有无限多个袋子，每个坐标对应一个袋子。其中一些袋子里装有硬币。

给你一个二维数组 `coins` ，其中 `coins[i] = [li, ri, ci]` 表示从坐标 `li` 到 `ri` 的每个袋子中都有 `ci` 枚硬币。这些区间是互不重叠的。

另给你一个整数 `k` 。返回通过收集连续 `k` 个袋子可以获得的 **最多** 硬币数量。

### Constraints

- $1 \leq coins.length \leq 10^5$
- $1 \leq k \leq 10^9$
- $1 \leq li \leq ri \leq 10^9$
- $1 \leq ci \leq 1000$
- 给定的区间互不重叠

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ 。
- 第二行包含 $n$ 行，每行包含三个整数，表示第 $i$ 个区间的信息。

> $n \quad k$
>
> $li_1 \quad ri_1 \quad ci_1$
>
> $\ldots$
>
> $li_n \quad ri_n \quad ci_n$

### Output

输出一个整数，表示收集连续 $k$ 个袋子可获得的最大硬币数量。

### Sample Input 1

```txt showLineNumbers=false
3 4
8 10 1
1 3 2
5 6 4
```

### Sample Output 1

```txt showLineNumbers=false
10
```

### Sample Input 2

```txt showLineNumbers=false
1 2
1 10 3
```

### Sample Output 2

```txt showLineNumbers=false
6
```

## 题目要点解析



## 使数组连续难题

[题目链接](https://leetcode.cn/problems/minimum-number-of-operations-to-make-array-continuous/description/)

### Problem Statement

给你一个整数数组 `nums` 。每一次操作中，你可以将数组中任一元素替换为 **任意整数** 。

如果数组满足以下条件，则称其为 **连续** 的：

1. 数组中所有元素都是 **唯一** 的（没有重复元素）。
2. 数组中最大元素与最小元素之间的差值等于 `nums.length - 1` 。

例如，`nums = [4, 2, 5, 3]` 是连续的，因为重新排序后得到 `[2, 3, 4, 5]` ，最大值与最小值差为 $5 - 2 = 3$ ，且长度为 $4$ 。而 `nums = [1, 2, 3, 5, 6]` 不是连续的。

请返回使 `nums` 成为连续数组所需的 **最少** 操作次数。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $1 \leq nums[i] \leq 10^9$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ ，表示数组长度。
- 第二行包含 $n$ 个整数，表示数组元素。

> $n$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出一个整数，表示使数组连续所需的最少操作次数。

### Sample Input 1

```txt showLineNumbers=false
4
4 2 5 3
```

### Sample Output 1

```txt showLineNumbers=false
0
```

### Sample Input 2

```txt showLineNumbers=false
5
1 2 3 5 6
```

### Sample Output 2

```txt showLineNumbers=false
1
```

### Sample Input 3

```txt showLineNumbers=false
4
1 10 100 1000
```

### Sample Output 3

```txt showLineNumbers=false
3
```

## 题目要点解析

正难则反，维护不需要改变的部分

---

# 种类滑动窗口问题

在处理字符串序列问题时，**种类滑动窗口** 是一种通过人为施加约束来构造单调性的精妙技巧。标准的滑动窗口通常要求窗口内的总长度具备某种天然的单调性，但在处理诸如计算包含相同频率字符的最长子串等问题时，窗口往往并不满足越长越好的简单单调逻辑，这使得常规的双指针方案难以直接奏效。为了破解这一困局，我们通常采取 **枚举字符种类数** 的核心策略，将复杂的全局问题拆解为在窗口内恰好包含 $k$ 种字符时的局部最优解，从而为滑动窗口创造了先决条件。

这种方法的核心在于利用了字符集规模通常较小的客观事实。以仅包含小写字母的字符串为例，其字符集规模 $\Sigma$ 的最大值仅为 $26$ 。我们通过一个外层循环固定当前的种类数限制 $target$ ，随后在内层执行标准的滑动窗口逻辑。右指针不断向右扩展并维护一个频率数组，一旦当前窗口内的不同字符总数超过了 $target$ ，左指针便开始收缩。这种强行制造单调性的做法，将原本复杂的组合搜索转化为了 $\Sigma$ 次标准的线性窗口扫描。虽然从形式上看复杂度增加了 $\Sigma$ 倍，但在 $O(\Sigma \cdot N)$ 的量级下，它在处理长字符串题目时展现出了极高的运行效率。

通过引入字符种类数这一额外的逻辑维度，我们将一个看似不具备单调性的全局搜索问题，转化为了若干个局部单调的子问题。在每一次子问题的求解过程中，由于种类数被严格限制，窗口的收缩逻辑变得清晰且唯一，从而确保了双指针移动的有效性与正确性。

## 统计完全字符串

[题目链接](https://leetcode.cn/problems/count-complete-substrings/description/)

### Problem Statement

给你一个字符串 `word` 和一个整数 `k` 。

如果一个字符串满足以下条件，则称它是一个 **完全子字符串**：

1. 字符串中的每个字符都恰好出现 `k` 次。
2. 相邻字符在字母表中的顺序至多相差 $1$（即 `abs(word[i] - word[i+1]) <= 1` ）。

返回 `word` 中完全子字符串的数目。

### Constraints

- $1 \leq word.length \leq 10^5$
- $1 \leq k \leq word.length$
- `word` 仅由小写英文字母组成

### Input

输入包含两行：

- 第一行包含一个字符串 $word$ 。
- 第二行包含一个整数 $k$ 。

> $word$
>
> $k$

### Output

输出一个整数，表示 `word` 中完全子字符串的数目。

### Sample Input 1

```txt showLineNumbers=false
igigee
2
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
aaabbbccc
3
```

### Sample Output 2

```txt showLineNumbers=false
6
```

## 题目要点解析



## K重复最长子串

[题目链接](https://leetcode.cn/problems/longest-substring-with-at-least-k-repeating-characters/description/)

### Problem Statement

给你一个字符串 `s` 和一个整数 `k` ，请你找出 `s` 中的最长子串，要求该子串中的每一字符出现次数都不少于 `k` 。如果有多个这样的子串，返回其中最长的长度。

如果不存在这样的子字符串，则返回 $0$ 。

### Constraints

- $1 \leq s.length \leq 10^4$
- $s$ 仅由小写英文字母组成
- $1 \leq k \leq 10^5$

### Input

输入包含两行：

- 第一行包含一个字符串 $s$ 。
- 第二行包含一个整数 $k$ 。

> $s$
>
> $k$

### Output

输出一个整数，表示符合要求的最长子串的长度。

### Sample Input 1

```txt showLineNumbers=false
aaabb
3
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
ababbc
2
```

### Sample Output 2

```txt showLineNumbers=false
5
```

## 题目要点解析



---

# 分组滑动窗口问题

在处理复杂的序列约束时，**分组滑动窗口** 是一种通过 **数据解耦** 来简化逻辑的高阶策略。在许多数组或字符串题目中，我们需要处理某种特定元素（如数字 $x$ 或字符 $c$ ）的连续段性质，而原数组中往往存在大量无关元素的交替干扰，导致直接维护全局窗口时逻辑极其冗余。该方法的核心思想在于 **按值归类与化繁为简** ，即预先利用动态数组将每种元素出现的所有下标分别提取出来，从而将杂乱无章的原始数组拆解为若干个独立的下标序列。

在这种独立序列上进行滑动窗口，本质上是在研究该元素第 $i$ 次出现与第 $j$ 次出现之间遮蔽了多少其他元素，或者其物理距离是否满足某种特定的约束。这种模型将混乱的全局状态转化为了 **局部有序的窗口移动** ，使得我们能够极速计算出特定元素在满足间隙限制下的最长连续段。由于窗口操作仅在同类元素的下标集合内进行，原本复杂的区间判定被抽象成对下标差值的线性扫描，极大地提升了算法的直观性与执行效率。

该模型在处理涉及 **修改操作** 的题目时表现尤为出色，其精髓在于每种元素的下标序列在逻辑上是相对独立的。这种局部的思维方式有效避免了对无关数据的无效扫描，通过将原本复杂的全局计数转化为局部下标间的运算，使得原本难以处理的修改问题变得非常直观。这种从原始序列中剥离核心数据的做法，不仅精简了算法的流程，更让整体逻辑变得清晰且易于维护。

## 最长等值子数组

[题目链接](https://leetcode.cn/problems/find-the-longest-equal-subarray/description/)

### Problem Statement

给你一个下标从 $0$ 开始的整数数组 `nums` 和一个整数 `k` 。

如果子数组中所有元素都相等，则认为子数组是 **等值** 的。注意，空子数组是等值的。

在从数组中删除最多 `k` 个元素后，返回其中最长的等值子数组的长度。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $1 \leq nums[i] \leq nums.length$
- $0 \leq k \leq nums.length$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ ，分别表示数组长度和最多可删除的元素个数。
- 第二行包含 $n$ 个整数，表示数组元素。

> $n \quad k$
>
> $nums_1 \quad nums_2 \quad \dots \quad nums_n$

### Output

输出一个整数，表示删除最多 $k$ 个元素后能得到的最长等值子数组的长度。

### Sample Input 1

```txt showLineNumbers=false
6 3
1 3 2 3 1 3
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
6 2
1 1 2 2 1 1
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析



## 单字符重复子串

[题目链接](https://leetcode.cn/problems/swap-for-longest-repeated-character-substring/description/)

### Problem Statement

如果字符串中的所有字符都相同，那么这个字符串是单字符重复的字符串。

给你一个字符串 `text` ，你只能交换其中两个字符一次或者什么都不做，然后得到一些单字符重复的子串。返回其中最长的子串的长度。

### Constraints

- $1 \leq text.length \leq 2 \cdot 10^4$
- `text` 仅由小写英文字母组成

### Input

输入仅包含一行：

> $text$

### Output

输出一个整数，表示在执行最多一次交换后，单字符重复子串的最大长度。

### Sample Input 1

```txt showLineNumbers=false
ababa
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
aaabaaa
```

### Sample Output 2

```txt showLineNumbers=false
6
```

### Sample Input 3

```txt showLineNumbers=false
aaabbaaa
```

### Sample Output 3

```txt showLineNumbers=false
4
```

## 题目要点解析



## 带修最长字符串

[题目链接](https://leetcode.cn/problems/longest-repeating-character-replacement/description/)

### Problem Statement

给你一个字符串 `s` 和一个整数 `k` 。你可以选择字符串中的任一字符，并将其更改为任何其他大写英文字符。该操作最多可执行 `k` 次。

在执行上述操作后，返回包含相同字母的最长子串的长度。

### Constraints

- $1 \leq s.length \leq 10^5$
- `s` 仅由大写英文字母组成
- $0 \leq k \leq s.length$

### Input

输入包含两行：

- 第一行包含一个整数 $k$ 。
- 第二行包含一个字符串 $s$ 。

> $k$
>
> $s$

### Output

输出一个整数，表示在最多替换 $k$ 次字符后，包含相同字母的最长子串的长度。

### Sample Input 1

```txt showLineNumbers=false
2
ABAB
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
1
AABABBA
```

### Sample Output 2

```txt showLineNumbers=false
4
```

## 题目要点解析



---

# 最近上与下邻问题

**最近上/下邻问题** 是单调栈最经典的应用场景。它通过维护一个特定的单调序列，将原本需要 $O(N^2)$ 的暴力检索优化为线性时间的实时响应。在遍历过程中，算法利用栈后进先出的特性，动态剔除那些在后续比较中 **已经失去竞争力的冗余元素** ，从而为每个元素准确定位其两侧的最近邻。这种剪枝机制确保了每个元素在整个生命周期中仅进出栈一次，实现了整体 $O(N)$ 的高效处理，为解决复杂的区间边界问题提供了清晰的逻辑起点。

以寻找 **两侧最近上邻**（即左侧和右侧第一个比当前元素大的数）为例，问题的本质在于识别哪些元素能成为候选答案。当我们从左向右扫描时，如果当前元素比前面出现的某些元素都要大，那么它在逻辑上就形成了对这些旧元素的 **绝对支配** 。其原因非常直观：对于后续待处理的元素而言，当前这个新元素不仅数值更优，而且在位置上也更靠近自身。在这种双重优势下，那些既小又远的旧元素便彻底失去了作为最近上邻的竞争力。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻1.png)

如果当前元素并不是目前的最大值，情况则演变为一种 **梯队式的筛选** 。根据上述支配逻辑，当前元素前面所有比它小的元素都已经失效，应当被果断剔除。然而，那些原本就比当前元素更大的旧元素依然具有保留价值，因为虽然当前元素位置更靠后，但它的数值大小不足以完全替代前面那些数值更大的元素。这种筛选机制确保了我们的候选集合始终处于一种 **优胜劣汰** 的动态平衡中。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻2.png)

由此我们可以提炼出一个核心规则：**每当新元素入场，就应当将其与栈顶元素进行比较，将候选集合中所有被其支配（即数值更小）的元素强制弹出**。在不断剔除这些冗余项后，剩余的候选元素在数值上必然是 **单调递减** 的序列，这在逻辑结构上正好契合了单调栈的维护逻辑。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻3.png)

基于这一结构，问题求解过程就会变得极其高效：每当新元素准备入栈时，在完成剔除操作后的 **当前栈顶元素** ，恰好就是它左侧扫描路径上的首个高位，即该元素左侧的最近上邻。同理，如果我们采用相同的逻辑反向遍历序列，便可以镜像地求出每个元素在右侧的最近上邻。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻4.png)

然而更精妙的是，我们并不需要显式地进行反向遍历，只需沿着单调栈的思路进一步分析：当栈中存在比当前元素更小的值时，它们必然会在当前元素入栈时被弹出；而栈中的任意一个元素，只要在后续过程中首次遇到一个比自己更大的元素，就一定会在那一刻出栈。因此 **元素被弹出的瞬间，恰好意味着它第一次遇到了右侧比它大的元素** ，这正是最近上邻的定义。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻5.png)

这种 **以空间换时间** 的策略不仅规避了低效的重复扫描，更直观地反映了序列元素间的大小与位置约束。通过将复杂的结构化查找转化为简单的入栈与出栈操作，单调栈为解决直方图最大矩形、接雨水问题以及各类复杂的区间贡献统计提供了最为简洁、高效的底层逻辑，实现了从暴力搜索到优雅剪枝的质变。

## 寻找累加和至少为K的最短数组

[题目链接](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/)

### Problem Statement

给你一个整数数组 `nums` 和一个整数 $k$ ，找出 `nums` 中和至少为 $k$ 的 **最短非空子数组** ，并返回该子数组的长度。如果不存在这样的 **子数组** ，返回 $-1$ 。

子数组是数组中 **连续** 的一部分。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $-10^5 \leq nums[i] \leq 10^5$
- $1 \leq k \leq 10^9$

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组中的各个元素。

> $N \quad k$
> 
> $nums_1 \quad nums_2 \quad \ldots \quad nums_N$

### Output

输出一个整数表示答案。

### Sample Input 1

```txt showLineNumbers=false
1 1
1
```

### Sample Output 1

```txt showLineNumbers=false
1
```

### Sample Input 2

```txt showLineNumbers=false
2 4
1 2
```

### Sample Output 2

```txt showLineNumbers=false
-1
```

## 题目要点解析

这道题目的核心目标是在含有负数的数组中，寻找和至少为 $k$ 的最短连续子数组。处理连续子数组和的问题，最自然的切入点是引入前缀和数组。令 $pre[i]$ 表示原数组前 $i$ 个元素的和，那么任意一个连续子数组 `nums[l...r-1]` 的和就可以转化为两个前缀和的差值，即 $pre[r] - pre[l]$ 。于是，题目要求的核心数学不等式可以写为 $pre[r] - pre[l] \geq k$ 。

为了方便通过遍历寻找最优解，我们可以将该不等式进行移项变形，得到以下形式：

$$
pre[l] \leq pre[r] - k
$$

该公式表明，当固定右端点 $r$ 时，我们需要在它的左边寻找一个满足条件的左端点 $l$ ，使得 $l$ 对应的前缀和数值小于等于 $pre[r] - k$ 。在所有满足该条件的左端点中，为了让子数组的长度 $r - l$ 尽量小，我们应该让 $l$ 尽量靠右，这本质上是一个最近下邻问题的变形。

由于原数组中存在负数，前缀和数组 $pre$ 会呈现出上下波动的非单调特性，这导致传统的双指针滑动窗口算法在此处失效。为了在非单调的前缀和序列中高效筛选出最优的左端点，我们需要借助单调双端队列来动态维护前缀和的下标，并保持队列中对应的前缀和数值严格单调递增。

随着右端点 $r$ 的向右移动，队列的维护逻辑主要分为两步。第一步是自队头向后查找可行解，若队头元素满足 $pre[r] - pre[dq.front()] \geq k$ ，则该队头已完成其作为左端点的最短历史使命，我们在更新全局最小长度后将其弹出。第二步是自队尾向前维护单调性，若当前 $pre[r]$ 小于等于队尾元素对应的前缀和，由于 $r$ 位置更靠右且数值更小，旧的队尾已被完全替代，我们将其从队尾弹出。

在这套双向剔除的机制下，每个元素的下标在整个遍历过程中最多只会入队一次和出队一次。这使得我们可以彻底告别暴力枚举的高额复杂度，将整个寻找最短区间的时间复杂度完美控制在线性级别。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 数组最大幸运值

[题目链接](https://www.luogu.com.cn/problem/CF280B)

### Problem Statement

给定一个长度为 $n$ 的整数数组 $a$ 。你需要找出数组中任意两个元素 $a[i]$ 和 $a[j]$（ $i \le j$ ），使得它们的异或和 $a[i] \oplus a[j]$ 最大。该异或和必须满足：对于所有满足 $i < k < j$ 的 $k$ ，都有 $a[k] < \min(a[i], a[j])$ 。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq a[i] \leq 10^9$

### Input

输入包含两行：

- 第一行包含一个整数 $n$ 。
- 第二行包含 $n$ 个整数，表示数组元素。

> $n$
>
> $a_1 \quad a_2 \quad \ldots \quad a_n$

### Output

输出一个整数，表示满足条件的最大异或和。

### Sample Input

```txt showLineNumbers=false
5
5 2 1 4 3
```

### Sample Output

```txt showLineNumbers=false
7
```

## 题目要点解析

枚举次大值，用单调栈求解可能的最大值

## 变化阈值子数组

[题目链接](https://leetcode.cn/problems/subarray-with-elements-greater-than-varying-threshold/description/)

### Problem Statement

给你一个整数数组 `nums` 和一个整数 `threshold` 。

找出数组 `nums` 中的一个子数组，且满足以下条件：

1. 子数组的长度为 `k` 。
2. 子数组中的每个元素都大于 `threshold / k` 。

返回满足条件的任意子数组的 **长度** `k`。如果没有这样的子数组，返回 `-1` 。

### Constraints

- $1 \leq nums.length \leq 10^5$
- $1 \leq nums[i], threshold \leq 10^9$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $threshold$ 。
- 第二行包含 $n$ 个整数，表示数组的元素。

> $n \quad threshold$
>
> $nums_1 \quad nums_2 \quad \ldots \quad nums_n$

### Output

输出一个整数，表示满足条件的子数组长度 $k$ ；若不存在，输出 `-1` 。

### Sample Input 1

```txt showLineNumbers=false
5 6
1 3 4 3 1
```

### Sample Output 1

```txt showLineNumbers=false
3
```

### Sample Input 2

```txt showLineNumbers=false
5 7
6 5 6 5 8
```

### Sample Output 2

```txt showLineNumbers=false
1
```

## 题目要点解析



---

# 最远上与下邻问题

**最远上/下邻问题** 与最近邻问题的核心差异在于对单调性的利用逻辑。最近邻关注的是生存竞争下的局部排除，而最远邻则侧重于历史存留中的全局跨度。该问题的挑战在于如何在长序列中快速定位最远的目标，通常需要通过 **预处理单调序列** 配合 **二分查找** ，将暴力检索的 $O(N^2)$ 复杂度优化至 $O(N \log N)$ 。这种策略利用了单调性提供的有序检索空间，在确保不漏掉任何潜在解的同时，极大地提升了在大规模数据下锁定最远边界的能力。

以寻找 **两侧最远上邻**（即位于最左侧和最右侧且比当前元素大的数）为例，问题的核心在于识别哪些历史元素具备成为最远目标的潜力。由于我们追求的是相对最远的位置，那么位置越靠前的元素，其价值自然就越高。基于这一观察，如果一个较晚出现的元素，其数值甚至还不如它左侧已有的某个元素大，那么它在位置和数值上都处于劣势，便永远不可能成为后续任何元素的最远上邻。因此，真正有资格进入候选集合的，必然是那些 **刷新了历史最值的元素** ，这些元素必然会在数值上呈现出严格的 **单调递增** 形式。

![最远上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最远上邻1.png)

当新元素尝试与这个候选集合匹配时，处理逻辑从原本的 **末端剔除** 转向了 **内部检索** 。如果当前值小于栈顶元素，说明其左侧确实存在合法的上邻。但为了追求最远的跨度，仅仅找到一个大于当前值的数是不够的，我们必须在所有比它大的候选中，精准锁定那个 **位置最靠前的元素** 。本质上，这相当于在有序的单调序列中执行一次 **二分查找**，可以在 $O(\log N)$ 的时间内精准锁定符合要求的元素。

![最远上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最远上邻2.png)

值得注意的是，**最远邻问题无法像最近邻问题那样，仅通过单次遍历便同时结算两侧的答案** 。这是由最远邻判定对 **全局位置极值** 的高度依赖性决定的。在单向扫描过程中，算法无法即时判定当前匹配的合法元素是否为物理意义上的最远边界，因为序列未遍历的远端仍可能存在更优解。这种 **信息的滞后性** 决定了该问题必须通过 **正向遍历求左侧最远邻** 与 **反向遍历求右侧最远邻** 两个独立的流程来完成。

![最远上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最远上邻3.png)

从更宏观的视角来看，单调栈在处理此类问题时表现出一种只进不出的单向累加状态，这其实揭示了它与前缀最大值结构的等价性。为了进一步简化代码实现，我们可以预处理一个前缀最大值数组：

$$
mx[i] = \max(a[1], a[2], \ldots, a[i])
$$

由于该数组本身具有天然的单调不降属性，对于当前位置 $i$ ，如果 $mx[i-1] \leq a[i]$ ，那么显然左侧不存在更大的元素；否则，说明在区间 $[1, i-1]$ 内一定存在满足条件的解。此时，由于前缀最大值具有单调性，我们可以在前缀最大值数组上通过二分查找，找到 **最早使得前缀最大值大于当前值的位置** ，从而确定最远上邻。

## 寻找累加和至多为K的最长数组

[题目链接](https://www.nowcoder.com/practice/3473e545d6924077a4f7cbc850408ade)

### Problem Statement

给定一个无序整数数组 `arr` ，其中元素可以为正、负或 $0$ ；同时给定一个整数 `k` 。
请你在数组中找到 **所有累加和 ≤ k 的子数组** 中，长度 **最长** 的子数组的长度并输出该长度。

子数组必须是连续的一段，不可以跳跃选取。

### Constraints

- $1 \leq N \leq 10^5$
- $-10^9 \leq k \leq 10^9$
- $-100 \leq arr_i \leq 100$
- 所有输入均为整数

### Input

输入包含两行：

- 第一行包含两个整数 $N$ 和 $k$ 。
- 第二行包含 $N$ 个整数，表示数组中的各个元素。

> $N \quad k$
> 
> $arr_0 \quad arr_1 \quad \ldots \quad arr_{N-1}$

### Output

输出一个整数，表示累加和小于或等于 $k$ 的最长子数组的长度。

### Sample Input

```txt showLineNumbers=false
5 -2
3 -2 -4 0 6
```

### Sample Output

```txt showLineNumbers=false
4
```

## 题目要点解析

这道题可以转化为最远上邻问题。首先我们构造前缀和数组 `pre[i]` ，使得任意子数组 $[l, r]$ 的和可以表示为：

$$
sum(l, r) = pre[r+1] - pre[l]
$$

题目要求子数组和不超过 $k$ ，即：

$$
pre[r+1] - pre[l] \leq k \quad \Rightarrow \quad pre[r+1] \leq k + pre[l]
$$

通过这个变换我们可以将原问题转化为最远上邻问题：对每个右端点 $r$ ，我们希望找到最左的 $l$ ，满足 `pre[l]` 足够大，使得右端点对应的子数组和不超过 $k$ 。也就是说，右端点对应的最长子数组长度就等于 $r - l + 1$ ，而最左上邻的位置正是 $l$ 。

为了快速查找最左上邻，我们可以维护前缀最小值数组 `min_pre` ，记录 `pre` 数组的历史最小值。对于每个右端点，通过二分查找 `min_pre` 中第一个满足 `pre[l] >= pre[r+1] - k` 的位置，就能得到最左上邻。这种做法完全对应最远上邻模板：历史候选元素构成单调集合，右端点查询最远满足条件的左端点，然后更新答案。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

这道题可以进一步优化为更快的滑动窗口解法，但由于 **数组中可能存在负数** ，我们不能直接使用普通的滑动窗口。为了能正常处理这种情况，我们可以先用 DP 预处理每个位置往右延伸的 **最小累加和子数组** 。具体来说，这个解法需要定义两个 DP 数组：

- `minSum[i]`：表示从位置 $i$ 开始往右延伸的子数组中，累加和最小的那个子数组的和。
- `minSumEnd[i]`：表示对应 `minSum[i]` 的子数组终点位置，即最小累加和子数组的右端位置。

有了这两个数组之后，我们可以在滑动窗口中快速寻找最长子数组。右端点 $r$ 利用 DP 信息直接跳跃：当窗口扩展到某个右端点时，查 `minSum[r]` 得到从 $r$ 开始的最小累加和子数组，如果整个子数组加上当前窗口和不超过 $k$ ，则右端点可以直接跳到 `minSumEnd[r] + 1` ，一次性覆盖整个最小累加和子数组。如果窗口无法容纳该最小累加和，则说明从当前左端点开始延伸的子数组已经无法满足条件，此时左端点向右移动一格进行缩窗。

通过这种方式，左端点每次只移动一格，而右端点通过最小累加和子数组进行跳跃扫描，每个元素最多被访问一次，因此整个算法的时间复杂度为 $O(N)$ 。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 滑动窗口极值问题

在算法竞赛中，**滑动窗口极值问题** 是一类极其经典且高频的题型。其核心任务是给定一个长度不固定的窗口，要求在窗口沿数组从左向右滑动的过程中，实时获取每个窗口内元素的最值。如果采用暴力手段对每个窗口重新进行区间扫描，整体时间复杂度将达到 $O(nk)$ ，这在面对大规模数据时往往会超出时间限制。

解决这类问题的核心突破点在于识别窗口移动过程中的 **连续性与重叠性** 。由于每次滑动仅涉及一个旧元素的移出与一个新元素的引入，相邻窗口之间绝大多数元素是相同的。基于这一特征，我们并不需要关注窗口内的所有成员，而应聚焦于那些 **仍具竞争力的候选元素** ，即那些在当前或未来的滑动周期内，依然有可能成为极值的元素。

以维护区间最大值为例，当一个新元素进入窗口时，如果它大于窗口内已有的某些元素，那么这些数值较小且位置靠左的旧元素便失去了意义。即便它们仍在窗口的物理范围内，但因为新元素不仅数值更大，而且在时间维度上存活得更久，旧元素已经不可能再成为后续任何窗口的最大值。这种现象被称为 **支配关系** 。通过在处理时主动剔除这些失去竞争力的冗余数据，并让剩下的元素在队列中按数值维持严格的单调递减，我们便构造出了 **单调队列** 。

在单调队列的结构下，队头元素始终对应当前窗口的全局极值，从而实现了 **均摊 $O(1)$ 复杂度的获取效率** 。随着窗口左端点的向右移动，算法采用 **延迟弹出机制** 确保数据的时效性：即在查询最值前，持续校验队头元素的索引，一旦判定其已越过当前窗口左边界，便将其从队头移除。尽管在某些步骤中可能伴随多次弹出操作，但由于每个元素在整个流程中 **至多入队一次、出队一次** ，整体时间复杂度被稳定在 $O(n)$ 的线性级别。

## 接雨水最小花盆

[题目链接](https://www.luogu.com.cn/problem/P2698)

### Problem Statement

给定 $n$ 个雨滴的坐标 $(x_i, y_i)$ ，你需要选择一个宽度为 $w$ 的花盆（即花盆覆盖的水平区间为 $[x, x+w]$ ），使得花盆内所有雨滴的纵坐标极差（最大纵坐标与最小纵坐标之差）至少为 $d$ 。

求满足条件的最小花盆宽度 $w$ 。如果不存在这样的宽度，返回 $-1$ 。

### Constraints

- $1 \leq n \leq 10^5$
- $1 \leq d \leq 10^6$
- $0 \leq x_i, y_i \leq 10^6$

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $d$ 。
- 接下来的 $n$ 行，每行包含两个整数 $x_i$ 和 $y_i$ 。

> $n \quad d$
>
> $x_1 \quad y_1$
>
> $x_2 \quad y_2$
>
> $\ldots$
>
> $x_n \quad y_n$

### Output

输出一个整数，表示满足条件的最小花盆宽度 $w$ 。若不存在，输出 `-1` 。

### Sample Input

```txt showLineNumbers=false
4 5
6 3
2 4
4 10
12 15
```

### Sample Output

```txt showLineNumbers=false
2
```

## 题目要点解析



## 不等条件最大值

[题目链接](https://leetcode.cn/problems/max-value-of-equation/description/)

### Problem Statement

给你一个数组 `points` 和一个整数 `k` 。数组中每个元素都表示二维平面上的点的坐标，其中 `points[i] = [xi, yi]` ，并且按照 `xi` 从小到大排序。

请你返回 `yi + yj + |xi - xj|` 的最大值，其中 `|xi - xj| <= k` 且 `1 <= i < j <= points.length` 。

### Constraints

- $2 \leq points.length \leq 10^5$
- $points[i].length == 2$
- $-10^8 \leq points[i][0], points[i][1] \leq 10^8$
- $0 \leq k \leq 2 \cdot 10^8$
- `points` 中的所有点坐标 $xi$ 互不相同，且按 $xi$ 升序排列

### Input

输入包含两行：

- 第一行包含两个整数 $n$ 和 $k$ ，分别表示数组长度和最大水平距离限制。
- 接下来的 $n$ 行，每行包含两个整数 $xi$ 和 $yi$ 。

> $n \quad k$
>
> $x_1 \quad y_1$
>
> $x_2 \quad y_2$
>
> $\dots$
>
> $x_n \quad y_n$

### Output

输出一个整数，表示满足条件的最大值。

### Sample Input 1

```txt showLineNumbers=false
4 1
1 3
2 0
5 10
6 -10
```

### Sample Output 1

```txt showLineNumbers=false
4
```

### Sample Input 2

```txt showLineNumbers=false
3 3
0 0
3 0
9 2
```

### Sample Output 2

```txt showLineNumbers=false
3
```

## 题目要点解析

需要用到两数之和思想

---

# 参考文献列表

## 单调滑动窗口

1. [【CSDN 博客】滑动窗口法总结](https://blog.csdn.net/Dby_freedom/article/details/89066140)

2. [【labuladong】滑动窗口核心代码模板](https://labuladong.online/algo/essential-technique/sliding-window-framework/)

3. [【CSDN 博客】滑动窗口算法详解](https://blog.csdn.net/2401_87820834/article/details/145998759)

## 单调栈与队列

1. [【OI WiKi】单调栈相关知识](https://oi-wiki.org/ds/monotonous-stack/)

2. [【算法通关手册】单调栈详解](https://algo.itcharge.cn/03_stack_queue_hash_table/03_02_monotone_stack/)

3. [【CSDN 博客】数据结构之单调栈](https://blog.csdn.net/2301_79248256/article/details/155377188)

4. [【OI WiKi】单调队列相关知识](https://oi-wiki.org/ds/monotonous-queue/)

5. [【Jerrycyx】实用而好写的数据结构](https://www.cnblogs.com/jerrycyx/p/18683014)

6. [【P2441M】单调栈/单调队列](https://www.cnblogs.com/P2441M/p/18637702)