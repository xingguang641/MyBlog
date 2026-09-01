---
title: 【ACM 算法随笔】单调数据结构的应用
published: 2025-11-27
description: 记录一些 ACM 常用技巧
tags: [Algorithm, Trick, Note]
category: ACM Note
draft: false
---

# 滑动窗口相关问题

我们经常会遇到需要处理 **所有子数组** 的一类经典问题，解决这类问题最直接的思路是枚举所有可能的子数组，然后针对每个子数组单独处理。然而枚举所有子数组的时间复杂度较高，在数据规模较大时无法满足要求。

滑动窗口是针对这类问题的经典优化方法，其核心是在数组中维护一个连续区间，通过不断调整区间的左右端点以保证区间在移动过程中不会发生回退，从而避免对所有子数组进行枚举，将 $O(n^2)$ 的子数组问题优化至 $O(n)$ 。

但滑动窗口并不是解决所有子数组问题的通用优化技巧，只有当子数组本身 **存在限制条件** 时，窗口的移动才会呈现单向变化的趋势。通过判断当前子数组是否满足限制条件，可以排除大量无需枚举的情况。

以最常见的「子数组累加和不超过 $K$ 」为例，假设数组中的所有数字均为正数，当固定左指针 $left$ 并不断移动右指针 $right$ 时，窗口内的累加和会随着 $right$ 的增加而不断增大。当累加和超过限制后，继续向右扩展必然无法满足要求，因此在当前 $left$ 固定的情况下，无需继续枚举后续的 $right$ 。

随后移动 $left$ 缩小窗口并继续寻找满足条件的区间。由于数组中的元素均为正数，移除左端点只会使窗口累加和减小，因此在新的 $left$ 下，原窗口中 $left + 1$ 到 $right$ 的部分仍然满足限制，$right$ 无需重新从 $left$ 开始移动，而是可以直接从当前位置继续向右扩展。由于左右指针在移动过程中均不会发生回退，每个元素最多进入或离开窗口一次，因此原本的双重循环枚举过程可以优化为线性复杂度的窗口滑动过程。

根据窗口限制条件的不同，滑动窗口可以分为不定长滑动窗口和定长滑动窗口两类。上述问题属于 **不定长滑动窗口** 的一种形式，这类问题的限制条件来自窗口内部状态，窗口大小会随着状态变化不断调整。其中限制条件通常可以分为「至多/至少」两类，而「恰好」条件一般也可以转化为这两种条件。

当限制条件与窗口大小有关时，通常采用 **定长滑动窗口** 解决。此类问题需要根据要求维护长度固定的窗口，并在窗口移动过程中更新对应的信息。需要注意的是，对于「窗口长度不超过 $K$ 」这类限制条件，同样可以通过维护长度为 $K$ 的窗口进行处理，因此也可以将其归入定长滑动窗口类型题。

### 种类滑窗相关问题

前面介绍的滑动窗口之所以能够成立，是因为窗口需要满足的限制条件 **在整个滑动过程中保持不变** 。虽然窗口内部的状态会随着端点的移动而发生变化，但判断窗口是否合法的标准始终保持不变。对于「窗口内每种元素的出现次数都不少于 $K$ 」这类限制条件，由于窗口中包含的元素种类并不确定，因此需要满足的条件也无法确定。 

为了深入理解这类限制条件为什么无法使用普通的滑动窗口进行维护，可以将窗口中每种元素需要满足的出现次数视为一个独立的任务，并将当前 **未完成的任务数量** 作为窗口实际需要维护的变量。

当窗口向右扩展时，如果新加入的元素存在窗口中，那么其出现次数增加可能完成对应的任务，从而减少未完成任务数；如果新加入的元素不在窗口中，那么窗口新增一种元素并产生一个新的任务，从而增加未完成任务数。随着窗口不断向右扩展，未完成任务数既可能增加也可能减少，因此窗口状态的变化 **不再具有单调性** 。

既然窗口中包含的元素种类不确定，那么可以尝试将元素种类数固定下来。设窗口中包含 $d$ 种不同的元素，则限制条件可以转化为窗口内恰好包含 $d$ 种元素且每种元素的出现次数都不少于 $K$ 。对于每个固定的 $d$ ，只需要维护窗口中的元素种类数和已完成的任务数，并根据这两个状态判断窗口是否满足限制条件。

当窗口元素种类少于 $d$ 时，说明当前窗口包含的元素种类不足，需要扩展窗口；当窗口元素种类超过 $d$ 时，说明当前窗口包含的元素种类过多，需要收缩窗口。当元素种类恰好为 $d$ 时，如果已完成的任务数也恰好为 $d$ ，则说明窗口中的每种元素出现次数都不少于 $K$ ，当前窗口满足限制条件；如果已完成的任务数小于 $d$ ，则说明仍有元素的出现次数不足 $K$ ，当前窗口不满足限制条件，需要继续扩展窗口。

这种通过枚举窗口中元素种类数，并对每个固定的 $d$ 使用滑动窗口的方法，可以称为 **种类滑动窗口** 。由于需要枚举不同元素的数量 $d$ ，因此更适用于字符集大小有限的 **字符串问题** 。

### 分组滑窗相关问题

对于某些问题，限制条件要求区间内只能包含一种元素，同时还存在其他需要维护的条件。由于区间最终只需要保留一种元素，因此可以 **按照元素种类进行分组** ，将每种元素单独提取出来进行滑动窗口。

具体做法是将原数组按照元素种类进行分组，将每种元素单独提取出来。由于每个分组中都只包含一种元素，原问题中区间内只能包含一种元素的要求也自然得到满足，此时只需要在这个基础上继续处理其他要求。由于不同分组之间相互独立，因此可以分别对每个分组使用滑动窗口，维护窗口状态并计算对应结果。

在完成所有分组的处理后，只需要将各个分组得到的结果按照题目要求进行汇总就能得到原问题的答案。这样可以将原问题拆分为多个 **只包含一种元素** 的独立滑动窗口问题，从而简化窗口的维护方式。

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
- 会议按 $startTime$ 升序排列且不重叠

### Input

输入包含三行：

- 第一行包含三个整数 $n$ 、 $k$ 和 $eventTime$ 。
- 第二行包含 $n$ 个整数，表示每个会议的开始时间 $startTime$ 。
- 第三行包含 $n$ 个整数，表示每个会议的结束时间 $endTime$ 。

> $n \quad k \quad eventTime$
> 
> $startTime_0 \quad startTime_1 \quad \ldots \quad startTime_{n - 1}$
> 
> $endTime_0 \quad endTime_1 \quad \ldots \quad endTime_{n - 1}$

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
直接考虑会议的移动方式较为复杂，因此我们可以换一个角度，从会议之间的空闲间隔入手。当我们移动 $k$ 个会议时，连续 $k+1$ 个间隔之间恰好存在 $k$ 个会议，重新安排这 $k$ 个会议的位置后，这 $k+1$ 个间隔就可以合并成一段连续的空余时间。因此我们只需要寻找连续 $k+1$ 个间隔的最大总长度。

在具体实现上，我们可以将所有 $n+1$ 个间隔的长度存入数组，然后使用大小为 $k+1$ 的固定长度滑动窗口，维护窗口内的间隔总和。这样就将原本的会议移动问题，转化为定长区间最大和问题。

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
- 第三行包含 $m$ 个字符串，表示 $words$ 数组中的每个单词。

> $s$
> 
> $m$
> 
> $words_0 \quad words_1 \quad \ldots \quad words_{m - 1}$

### Output

输出一行整数，表示所有符合条件的起始索引，如果不存在答案请输出 `-1` 。

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

本题的关键在于将原字符串 `s` 视为由若干个长度为 $len$ 的单词块构成的序列，可以将复杂的子串匹配问题转化为经典的滑动窗口问题。由于 `words` 中的单词可以任意排列，因此只需要判断各单词的出现次数是否匹配。

由于单词的起始位置并不固定，如果只从索引 $0$ 开始以 $len$ 为步长进行扫描，就会遗漏从其他位置开始的合法划分。因此我们需要依次以 $0, 1, 2, \dots, len - 1$ 作为起点进行偏移扫描，从而覆盖所有可能的切分方式。

在每一组偏移扫描中都可以维护一个独立的滑动窗口，我们利用哈希表记录窗口内各单词的出现次数，右指针每次向右移动 $len$ 个字符，并将新的单词加入窗口。当窗口内某个单词的出现次数超过目标频次时，左指针开始向右收缩并不断删除左侧单词，从而保证窗口内各单词的出现次数都不超过 `words` 中对应的数量。

当窗口内的单词数量 `curm` 等于 $m$ 时，说明当前窗口中的单词与 `words` 完全匹配，记录窗口此时的左端点。

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
- $s[i]$ 为 `'0'` 或 `'1'`

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

操作 $1$ 的 **本质就是轮换** ，而处理轮换的常见方式是 **将原数组倍增后滑窗** 。当我们维持一个长度固定为 $n$ 的窗口在倍增数组上向右滑动时，窗口每滑动一次就等价于原数组进行一次轮换操作。

对于交替字符串，其最终的目标形态本质上只有两种：一种是形如 `101010` 的字符串，另一种是形如 `010101` 的字符串。为了避免在滑动窗口的过程中对这两种目标形态进行复杂的分类讨论，我们可以巧妙地引入一个 **全局参考基准线** ，并采用 “错位映射” 的数学思想将两种目标统一起来。

我们不妨以第二种形式作为全局参考基准线，这意味着在目标基准线上，所有偶数下标对应的字符应当为 `'0'` ，所有奇数下标对应的字符应当为 `'1'` 。此时我们将倍增字符串中的每一个字符与该基准线进行比对，如果当前字符不满足这个奇偶交替的规律，我们就将其视为一个错位点，也就是需要进行类型 $2$ 反转操作的位置。

随着窗口在倍增字符串上向右滑动，具体的错位映射逻辑会出现以下两种情况：

- 第一种情况，当子串左端点下标是偶数时。因为左端点在全局基准线上本来就是偶数位置，所以此时窗口内部的奇偶性与全局基准线 **完全对齐** 。这意味着如果我们想把这个子串变成 `010101` 形态，那些 **不符合全局基准线** 的字符就需要反转；如果我们想把它变成 `101010` 形态，那些 **符合全局基准线** 的字符就需要反转。

- 第二种情况，当子串左端点下标是奇数时。因为左端点在全局基准线上变成奇数位置，这导致整个窗口的奇偶性相对于全局基准线 **整体向右偏移 1 位** 。这意味着如果我们想把子串变成 `010101` 形态，那些 **符合全局基准线** 的字符就需要反转；如果我们想把它变成 `101010` 形态，那些 **不符合全局基准线** 的字符就需要反转。

在这两种情况中，由于窗口内的总字符数固定为 $n$ ，如果我们引入一个计数器 $cnt$ ，专门用来动态统计当前窗口内 **不符合全局基准线** 的错位点个数，那么当前窗口内 **符合全局基准线** 的字符个数自然就为 $n - cnt$ 。此时我们可以清晰地看到，无论子串的左端点下标是奇数还是偶数，其最小反转次数均可以通过以下公式统一表达：

$$
Ans = \min(cnt, n - cnt)
$$

在接下来的滑动窗口过程中，我们只需要动态维护这个计数器 $cnt$ ，并不断更新全局最优解。

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

给你一个二维数组 `coins` ，其中 `coins[i] = [li, ri, ci]` 表示从坐标 `li` 到 `ri` 的每个袋子中都有 `ci` 枚硬币，这些区间互不重叠。另给一个整数 `k` ，返回通过收集连续 `k` 个袋子可以获得的 **最多** 硬币数量。

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



## 数组的连续难题

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

## 统计完全字符串

[题目链接](https://leetcode.cn/problems/count-complete-substrings/description/)

### Problem Statement

给你一个字符串 `word` 和一个整数 `k` 。

如果一个字符串满足以下条件，则称它是一个 **完全子字符串**：

1. 字符串中的每个字符都恰好出现 `k` 次。
2. 相邻字符在字母表中的顺序至多相差 $1$ 。

返回 `word` 中完全子字符串的数目。

### Constraints

- $1 \leq word.length \leq 10^5$
- $1 \leq k \leq word.length$
- $word$ 仅由小写英文字母组成

### Input

输入包含两行：

- 第一行包含一个字符串 $word$ 。
- 第二行包含一个整数 $k$ 。

> $word$
>
> $k$

### Output

输出一个整数，表示 $word$ 中完全子字符串的数目。

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



---

# 单调堆栈相关问题

在处理需要寻找元素之间关系的问题时，我们通常可以枚举当前元素，将已经出现的元素作为候选值，再根据题目的具体限制选择合适的数据结构进行维护，这就是[两数之和思想](https://xingguang641.com/posts/acm/acm-note/two-sum-idea/two-sum-idea/)。对于单调堆栈相关问题，候选值之间往往存在明显的 **相互排除关系** ，因此可以进一步利用这种关系筛选候选值，从而减少需要维护的元素数量。

当问题同时受到两种约束限制时，候选值之间往往会因为这两种约束产生明显的支配关系。假设有一批物品，每件物品都有容量和价值两个属性，现在要求选择两个物品，使它们的总容量不超过 $m$ 且总价值尽可能大。那么对于两个物品，如果其中一个物品的容量更大的同时价值还更低，那么它在任何情况下都不可能成为更优的候选值，因此可以直接排除。将物品按照容量排序后，这种候选值之间的相互排除关系就可以通过单调结构进行维护。

这种候选值之间的相互排除关系，正是单调堆栈能够发挥作用的基础。当候选值之间存在明确的大小关系时，我们就可以利用这种关系不断排除已经失去竞争力的候选值，并将剩余候选值维护成单调结构。**最近上/下邻问题** 和 **最远上/下邻问题** 都可以从这一思路展开，下面将分别从这两类问题展开进行分析。

### 最近上下邻问题

**最近上/下邻问题** 是单调栈最经典的应用场景之一。它通过维护一个具有单调性的候选序列，并在遍历过程中不断排除已经失去竞争力的元素，从而快速确定每个元素两侧的最近上邻或下邻。由于每个元素最多入栈一次并出栈一次，整个过程的时间复杂度可以降至 $O(N)$ ，这也构成了单调栈处理此类问题的基本思路。

以「寻找两侧最近上邻」为例，问题的核心在于判断哪些元素仍然具备成为候选答案的可能。当我们从左向右扫描时，如果当前元素比前面某些元素更大，那么它就形成了对这些元素的 **绝对支配** 。对于后续元素而言，当前元素不仅数值更大且位置也更加靠近，因此那些数值更小且位置更远的元素便不再具有成为最近上邻的可能。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻1.png)

按照上述支配逻辑，当前元素前面所有比它小的元素都会被它支配，因此 **可以直接剔除** 。对于那些比当前元素更大的元素，当前元素虽然位置更靠后，但数值不足以取代它们，所以 **仍然需要保留** 。这样一来，候选集合便会随着新元素的加入不断筛选，始终保留具有竞争力的元素。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻2.png)

由此可以得到一个核心规则：**每当新元素加入时，都将其与栈顶元素进行比较，并不断弹出所有被当前元素支配的候选值** 。完成筛选后，栈中剩余元素的数值始终保持 **单调递减** ，因此可以通过栈的结构高效维护这组候选值。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻3.png)

基于这一结构，当新元素准备入栈时，完成剔除操作后的 **当前栈顶元素** 就是它左侧第一个比它大的元素，也就是左侧最近上邻。如果采用相同的逻辑从右向左遍历序列，则可以得到每个元素右侧的最近上邻。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻4.png)

然而更精妙的是，我们不需要额外进行反向遍历。对于栈中的任意元素，当后续首次出现一个比它更大的元素时，它就会在当前元素入栈的过程中被弹出。由于在此之前没有更大的元素出现，因此 **元素被弹出的时刻，恰好就是它第一次遇到右侧更大元素的时刻** ，而这个元素正是它右侧的最近上邻。

![最近上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最近上邻5.png)

这种策略不仅避免了重复扫描，也充分利用了元素之间的大小与位置关系。通过将复杂的查找过程转化为简单的入栈与出栈操作，单调栈能够不断排除已经失去竞争力的候选值，并将原本需要大量比较的过程优化为线性遍历。

### 最远上下邻问题

**最远上/下邻问题** 与最近邻问题的处理方式有所不同，最近邻只需要找到距离当前元素最近的候选值，而最远邻则需要在满足条件的候选值中寻找位置最远的元素，因此需要保留具有潜在价值的候选值，并利用单调性结合二分查找快速确定最远位置，将暴力枚举的 $O(N^2)$ 复杂度优化到 $O(N \log N)$ 。

以「寻找两侧最远上邻」为例，问题的核心在于确定哪些历史元素仍然具有成为最远上邻的可能。由于我们追求的是更远的位置，因此位置越靠前的元素越有价值。如果一个较晚出现的元素，其数值还不如左侧已经出现的某个元素，那么它在位置和数值上都处于劣势，后续也不可能成为更优的候选值。因此能够进入候选集合的元素，必须不断刷新此前的历史最大值，并在数值上形成严格的 **单调递增** 序列。

![最远上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最远上邻1.png)

当新元素与候选集合进行匹配时，我们不再进行元素剔除，而是直接在已有的候选集合中进行 **内部检索** 。如果当前值小于栈顶元素，说明左侧存在满足条件的上邻，此时只需要在候选集合中继续向前寻找，直到找到 **位置最靠前且满足条件的元素** 。由于候选集合在数值上保持单调递增，因此可以通过 **二分查找** 快速确定对应位置。

![最远上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最远上邻2.png)

值得注意的是，**最远邻问题无法像最近邻问题那样，仅通过单次遍历便同时结算两侧的答案** 。这是由最远邻判定对 **全局位置极值** 的高度依赖性决定的。在单向扫描过程中，算法无法即时判定当前匹配的合法元素是否为物理意义上的最远边界，因为序列未遍历的远端仍可能存在更优解。这种 **信息的滞后性** 决定了该问题必须通过 **正向遍历求左侧最远邻** 与 **反向遍历求右侧最远邻** 两个独立的流程来完成。

![最远上邻图像](src\content\posts\ACM\acm-note\monotonic-structure\最远上邻3.png)

从更宏观的角度来看，由于最远上下邻问题中的候选元素一旦加入后便不会被剔除，因此这个单调栈本质上是在不断记录历史上的最大值。为了进一步简化代码实现，我们可以预处理一个前缀最大值数组：

$$
mx[i] = \max(a[1], a[2], \ldots, a[i])
$$

对于当前位置 $i$ ，如果 $mx[i - 1] \leq a[i]$ ，说明其左侧不存在更大的元素；如果 $mx[i - 1] > a[i]$ ，说明在区间 $[1, i - 1]$ 内一定存在满足条件的解。由于前缀最大值数组具有单调性，我们可以在前缀最大值数组上通过二分查找，找到 **最早使得前缀最大值大于当前值的位置** ，从而确定最远上邻。

## 寻找累加和至少为K的最短数组

[题目链接](https://leetcode.cn/problems/shortest-subarray-with-sum-at-least-k/)

### Problem Statement

给你一个整数数组 `nums` 和一个整数 $k$ ，找出 `nums` 中累加和至少为 $k$ 的 **最短非空子数组** ，并返回该子数组的长度。如果不存在这样的 **子数组** ，请返回 $-1$ 。

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

输出一个整数，表示满足条件的最短非空子数组的长度，若无法完成则输出 `-1` 。

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

这道题需要在包含负数的数组中寻找和至少为 $k$ 的最短子数组。由于负数会破坏区间和的单调性，传统的滑动窗口无法直接使用。因此对于此类数组子段和问题，我们可以引入前缀和数组辅助求解。

令 $pre[i]$ 表示原数组前 $i$ 个元素的和，那么连续子数组 `nums[l...r-1]` 的和可以表示为：

$$
pre[r] - pre[l]
$$

因此题目要求可以转化为：

$$
pre[r] - pre[l] \geq k
$$

将不等式移项可以得到：

$$
pre[l] \leq pre[r] - k
$$

在固定右端点 $r$ 后，我们需要在左侧寻找满足 $pre[l] \leq pre[r] - k$ 的下标 $l$ 。由于目标是使子数组长度 $r - l$ 尽可能地小，因此需要在所有满足条件的下标中选择位置最靠右的 $l$ 。这本质上是在前缀和序列中 **寻找当前值对应的最近下邻** ，因此可以使用单调双端队列维护前缀和下标，并保证队列中对应的前缀和保持单调递增。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## 数组最大幸运值

[题目链接](https://www.luogu.com.cn/problem/CF280B)

### Problem Statement

给定一个长度为 $n$ 的数组 $a$ ，你需要找出数组中任意两个元素 $a[i]$ 和 $a[j]$（ $i \leq j$ ），使得它们的异或和最大。

该异或和必须满足：对于所有满足 $i < k < j$ 的 $k$ ，都有 $a[k] < \min(a[i], a[j])$ 。

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

返回满足条件的任意子数组的 **长度** `k` 。如果没有这样的子数组，返回 `-1` 。

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

输出一个整数，表示满足条件的子数组长度 $k$ ，若不存在则输出 `-1` 。

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

单调栈贪心问题

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
> $arr_0 \quad arr_1 \quad \ldots \quad arr_{N - 1}$

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

这道题可以转化为最远上邻问题。首先构建前缀和数组 `pre[i]` ，使得任意子数组 $[l, r]$ 的和可以表示为：

$$
sum(l, r) = pre[r + 1] - pre[l]
$$

将题目的条件带入并移项变形可以得到：

$$
pre[r + 1] - pre[l] \leq k \quad \Rightarrow \quad pre[r + 1] \leq k + pre[l]
$$

固定右端点 $r$ 后，我们需要在其左侧寻找满足 $pre[l] \geq pre[r + 1] - k$ 的最左下标 $l$ 。由于目标是使子数组长度 $r - l + 1$ 尽可能大，因此需要让 $l$ 尽可能靠前，这可以看作一个最远上邻问题。

为了快速查找最左上邻，我们可以维护前缀最小值数组 `min_pre` ，记录 `pre` 数组的历史最小值。对于每个右端点，通过二分查找 `min_pre` 中第一个满足 `pre[l] >= pre[r+1] - k` 的位置，就能得到最左上邻。

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

除了前面的前缀和二分方法外，这道题还存在另一种时间复杂度为 $O(N)$ 的滑动窗口解法。由于 **数组中可能存在负数** ，普通的滑动窗口无法直接使用，因此需要先通过 DP 预处理每个位置向右延伸时的 **最小累加和子数组** 。

具体而言，我们需要定义两个 DP 数组：

- `minSum[i]`：表示从位置 $i$ 开始往右延伸的子数组中，累加和最小的那个子数组的和。
- `minSumEnd[i]`：表示对应 `minSum[i]` 的子数组终点位置，即最小累加和子数组的右端位置。

有了这两个数组之后，我们可以在滑动窗口中快速寻找最长子数组。右端点 $r$ 每次利用 DP 信息进行跳跃，如果当前窗口加上 `minSum[r]` 后仍然不超过 $k$ ，说明从 $r$ 开始的整个最小累加和子数组都可以加入窗口，此时可以直接将右端点跳到 `minSumEnd[r] + 1` 。如果无法加入，则移动左端点缩小窗口，并继续进行判断。

通过这种方式，左端点每次只向右移动一格，右端点则根据最小累加和子数组的终点位置进行跳跃。由于左右端点都只向右移动，每个位置最多参与两次操作，因此整个算法的时间复杂度为 $O(N)$ 。  

```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

---

# 单调队列相关问题

单调队列可以看作是 **单调栈的进阶结构** ，它主要用于处理候选元素存在有效范围限制的问题。单调栈在维护候选值时，只需要根据元素之间的支配关系进行筛选。而在某些问题中，候选元素还会随着位置的变化逐渐失效，因此需要在维护单调结构的同时及时删除已经过期的元素。

单调队列的维护方式与单调栈基本一致：新元素加入时，从队尾不断排除已经被当前元素支配的候选值，使剩余元素继续保持单调性；同时根据元素的有效范围，从队首删除已经过期的元素。这样既可以利用元素之间的支配关系筛选候选值，又可以保证队列中的元素始终处于有效范围内。

在此基础上，单调队列还可以用于解决 **滑动窗口最值问题** 。如果每次窗口移动后都重新遍历窗口寻找最值，就需要重复检查窗口中的元素。此时可以利用单调队列维护候选最值，新元素加入时从队尾排除失去竞争力的元素，同时从队首删除已经离开窗口的元素，使队首始终对应当前窗口的最值。

以「滑动窗口最大值」为例，窗口中的候选元素同时受到 **位置和数值** 两方面的影响。对于后续窗口而言，元素位置越靠后且数值越大的候选值越有优势，因此如果一个元素位置更靠前且数值还更小，那么它就会被后出现的更大元素支配。按照这种支配关系，可以将候选值维护为 **单调递减** 的结构。

由于窗口左侧的元素会逐渐离开当前窗口，因此候选元素还会受到窗口范围的限制。当队首元素的位置已经超出当前窗口的左边界时，该元素便不再具备成为窗口最大值的资格，需要将其从队首删除。结合队尾的支配关系和队首的位置限制，就可以维护一个 **单调递减队列** ，使队首始终对应当前窗口中的最大值。

## 接雨水最小花盆

[题目链接](https://www.luogu.com.cn/problem/P2698)

### Problem Statement

给定 $n$ 个雨滴的坐标 $(x_i, y_i)$ ，你需要选择一个宽度为 $w$ 的花盆（即花盆覆盖的水平区间为 $[x, x + w]$ ），使得花盆内所有雨滴的纵坐标极差（最大纵坐标与最小纵坐标之差）至少为 $d$ 。

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

输出一个整数，表示满足条件的最小花盆宽度 $w$ ，若不存在则输出 `-1` 。

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

给你一个数组 `points` 和一个整数 `k` ，数组中每个元素都表示二维平面上的点的坐标。

其中 `points[i] = [xi, yi]` ，并且按照 `xi` 从小到大排序。

请你返回 `yi + yj + |xi - xj|` 的最大值，其中 `|xi - xj| <= k` 且 `1 <= i < j <= points.length` 。

### Constraints

- $2 \leq points.length \leq 10^5$
- $points[i].length == 2$
- $-10^8 \leq points[i][0], points[i][1] \leq 10^8$
- $0 \leq k \leq 2 \times 10^8$
- $points$ 中的所有点坐标 $xi$ 互不相同，且按 $xi$ 升序排列

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

# 参考文献引用列表

1. [【OI WiKi】单调栈相关知识](https://oi-wiki.org/ds/monotonous-stack/)

2. [【OI WiKi】单调队列相关知识](https://oi-wiki.org/ds/monotonous-queue/)

3. [【Jerrycyx】实用好写的数据结构](https://www.cnblogs.com/jerrycyx/p/18683014)

4. [【P2441M】单调栈/单调队列](https://www.cnblogs.com/P2441M/p/18637702)