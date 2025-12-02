---
title: 【机器学习基础算法】第四节：概率图算法
published: 2025-11-17
description: 介绍机器学习常见的算法
tags: [Machine Learning, Course]
category: ML Algorithm
draft: false
---

# 概率图算法背景介绍

概率图模型是一类将 **概率分布** 与 **图结构** 结合起来的建模方法。它的核心思想是：

> **高维联合分布之所以难以处理，是因为变量之间的依赖关系过于复杂；而图结构能够清晰表达这些依赖，使得分布分解成为可能，从而让推断和学习变得可行。**

换句话说，概率图模型是一种把 “概率” 变成 “图” 的技术，用图来表达随机变量如何相互影响，再在这个图结构下执行推断与学习。

## 因子分解（Factorization）

概率图模型的基础是利用图（Graph）来描述变量间的条件独立关系。典型有两种形式：

- **有向图（Bayesian Network）**

    有向图的边表示因果或条件生成关系，联合分布分解为：

    $$
    P(x_1, \ldots, x_n) = \prod_i P(x_i | pa(x_i))
    $$

- **无向图（Markov Random Field）**

    无向图的边表示相互作用，联合分布分解为：

    $$
    P(x) = \frac{1}{Z} \prod_{c \in \mathcal{C}} \psi_c(x_c)
    $$

    这里的 ​$\psi_c$ 是 “团（clique）” 上的势函数。

更常用的统一表示是 **因子图（Factor Graph）**，把联合分布直接写成因子的乘积，便于做消息传递（message passing）：

$$
P(x) = \frac{1}{Z} \prod_i f_i(x_i)
$$

这种因子分解的力量在于：高维分布变成许多局部分布的乘积，推断不再需要直接面对全局复杂度。

## 消息传递（Message Passing）

概率图算法最核心的思想是：

> **全局推断 = 图结构下的局部消息传递**

经典例子是 **Belief Propagation（BP）**：

- 每个节点维护对自己变量的 “belief”
- 通过边向其他节点传递 message（局部边缘化）
- 多轮迭代后逐渐收敛到近似边缘分布

树结构图上 BP 等价于精确推断。一般图上则是近似推断（Loopy BP），但往往效果很好。

BP 及其变体的统一公式本质上就是：

$$
m_{i \rightarrow j}(x_j) = \sum_{x_i} f_i(x_i) \prod_{k \in N(i) \setminus j} m_{k \rightarrow i}(x_i)
$$

这就是概率图算法的 “局部性原则”：每个节点只需要处理和自己直接相连的因子/变量，不必了解整个图。

## 核心价值（Core Value）

概率图算法之所以成为现代统计推断和机器学习的基石，是因为它解决了一个根本问题：

> **如何在高维空间中处理复杂依赖的概率分布？**

PGM 给出的答案是：

- 用图表示依赖结构（结构化）
- 用局部因子分解联合分布（可处理）
- 用消息传递、优化或采样做推断（可计算）

因此它几乎适用于所有需要 “推断隐变量” 的系统，从经典 HMM 到 CRF，再到深度学习中的能源模型、变分自动编码器（VAE）后验推断，全部可以放进 PGM 框架理解。

---

# 贝叶斯网络

在高维随机系统中，我们真正难以掌握的往往不是概率分布本身，而是分布背后隐含的 **结构关系** 。多个变量之间既不是完全独立，也不是彼此全都强关联，而是形成了一张稀疏、有向且层次分明的依赖网络。传统的联合分布写法会将这种结构完全掩盖，而 **贝叶斯网络**（Bayesian Network，简称 BN）正是为了解决这一问题。它通过一个有向无环图（DAG）将高维联合分布展开为一系列局部因子的组合，从而将原本不可处理的全局模型转化为一个结构化、可解释且可推断的系统。

这种结构化的建模方式带来了显著的优势。依赖关系被明确地写入图结构中，不再埋藏在高维联合分布的符号背后；模型在高维空间中的复杂度得以控制，每个变量只依赖其父节点，从而避免了指数级的参数膨胀；同时，推断也由全局困难的问题转变为可局部分解的操作，使得计算效率显著提高。这些特点共同解释了贝叶斯网络在系统建模、信号处理、因果推断以及图模型研究中长期占据核心地位的原因。

![BN 图像](src\content\posts\probabilistic-graphical-model\BN结构1.jpg)

## 因子化公式（Factorization Formula）

贝叶斯网络由两部分组成：一个表示依赖关系的图结构，以及与图对齐的局部条件分布。设变量集合为 $x_1,\ldots,x_n$ ，其联合分布满足著名的因子化公式：

$$
P(x_1,\ldots,x_n) = \prod_{i=1}^n p(x_i| pa(i))
$$

其中 $pa(i)$ 表示节点 $i$ 的父集。这个因子化并非任意，而是图结构所 **强制** 施加的限制。每个节点只需描述自身在给定父节点下的局部行为，而不需关心整个系统的复杂度。

因此，联合分布原本需要的参数量 ———— 指数级随节点数增长 ———— 在图结构的约束下被压缩到线性或稀疏图下的可控规模。这些局部因子共同拼装出整个系统，而它们之间的拼装方式又是由图精确定义的。

在这个过程中，一些条件独立性自动产生。例如若节点 $x_k$ 的父节点仅为 $x_i$ 与 $x_j$ ，则结构立即给出：

$$
x_k \perp {x_\ell:\ell\neq i,j,k} \mid (x_i,x_j)
$$

可以看作每个节点自带一个 “独立性语句” ，而整个网络的独立性结构就是这些局部语句的组合。

## 独立性结构（Independence Structure）

贝叶斯网络的核心价值实际上在于 **将独立性写进图的拓扑结构** 。图中的路径对应潜在依赖，而 d-separation 则提供了判断路径是否被阻断的标准。

若集合 $Z$ 阻断了 $X$ 到 $Y$ 之间的所有有效路径，则有：

$$
X \perp Y \mid Z
$$

路径的阻断由三种基本结构决定：

* **链式结构**（ $X\to Z\to Y$ ）：条件化 $Z$ 会切断路径
* **分叉结构**（ $X\leftarrow Z\to Y$ ）：同样因为条件化 $Z$ 而路径中断
* **汇聚结构**（ $X\to Z\leftarrow Y$ ）：此时反过来，观察 $Z$ 或其后代会激活路径

这三种结构虽然简单，但它们的组合可以描述极其复杂的依赖与独立性关系，使得 d-separation 成为整个概率图论的逻辑核心。

也正因为图的拓扑直接决定独立性结构，许多推断算法可以只依赖图而不依赖具体参数。

## 局部推断机制（Local Inference Mechanism）

一旦联合分布按照图结构因子化，推断便不再是一个全局积分问题。

无论使用的是变量消元（variable elimination）、belief propagation 、junction tree 方法，还是更通用的 EP、VI、图上的 MCMC，它们的思想都极其统一：

> **将全局推断拆解为局部消息传递。**

例如在变量消元中，如果我们要对某个变量 $x_k$ 做边缘化，只需将所有包含 $x_k$ 的局部因子相乘并对其积分，最终产生一个新的因子。整个运算过程只会在局部子图中进行，不会 “污染” 整个系统。

而在 belief propagation 中，这一思想更加明显。

每个节点通过向邻接节点发送一个 “消息” ，该消息仅基于本地因子与来自其他邻居的消息计算。最终每个节点得到自己的腹地（belief）：

* **不需要全局信息**
* **不需要全局分布**
* **只需要图的局部结构与相邻节点的消息**

因此，推断复杂度完全依赖图的稀疏性与图的 “树宽” 。稀疏图带来快速推断，而稠密图则可能导致指数级复杂度。

## 高斯网络（Gaussian Network）

当随机变量由离散过渡到连续时，最自然的局部模型便是 **线性–高斯条件分布** 。若节点 $x_i$ 的父集合为 $pa(i)$ ，其局部生成式写成：

$$
x_i = \sum_{j\in pa(i)} w_{ij} x_j + \epsilon_i \qquad \epsilon_i \sim \mathcal{N}(0, \sigma_i^2)
$$

将所有节点按拓扑序拼成向量 $x$ ，便得到整体的矩阵形式：

$$
x = W x + \epsilon \qquad \epsilon \sim \mathcal{N}(0, D)
$$

其中 $W$ 的稀疏结构对应图结构本身，$D$ 为噪声方差的对角矩阵。

### 联合分布的闭式表达

由线性结构可以直接推出联合分布为一个多元高斯：

$$
x \sim \mathcal{N}\Big( 0, (I-W)^{-1} D (I-W)^{-{\rm T}} \Big)
$$

进一步，精度矩阵（precision matrix）可写为：

$$
\Lambda = (I-W)^{\rm T} D^{-1} (I-W)
$$

这里最关键的现象是，图中 **不存在的边** 会在精度矩阵中体现为对应位置的零，而图的局部结构决定了精度矩阵的稀疏性。换言之，图结构与代数结构实现了严格的一一对应关系。

### 边缘化与条件化

高斯模型计算优势的核心在于可积性。将变量划分为两部分：

$$
x = (x_a, x_b)
$$

并写成分块高斯：

$$
x \sim \mathcal{N}\left(
\begin{bmatrix}\mu_a \ \mu_b\end{bmatrix},
\begin{bmatrix}
\Sigma_{aa} & \Sigma_{ab} \
\Sigma_{ba} & \Sigma_{bb}
\end{bmatrix}
\right)
$$

则条件分布可以直接写出闭式形式：

$$
p(x_a | x_b) = \mathcal{N}\Big(\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b - \mu_b), \Sigma_{aa} - \Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba} \Big)
$$

这里没有任何近似，所有边缘化和条件化都退化为矩阵代数操作。

### 推断的线性代数化

GBN 的优势在于，它将贝叶斯网络的结构化推断与高斯模型的解析可处理性结合成了非常干净的计算形式。在实践中，推断过程主要体现在：

* **边缘化**：积分操作退化为 Schur 补和分块矩阵运算
* **条件化**：更新操作可通过矩阵分解（如 Cholesky 分解）完成
* **消息传递（BP）**：局部高斯消息的传递仅涉及精度和方差的线性组合

整个推断过程几乎完全由线性代数支配，使得 GBN 在连续变量系统中成为计算效率与结构表达能力兼具的模型。

---

# 马尔可夫随机场

在许多真实的高维系统中，变量之间的依赖往往并不表现为明显的 “从原因到结果” 的方向性结构。例如图像中的像素之间并没有严格的先后顺序，它们的相互关系通常更像一种对称的空间耦合；物理系统中的粒子之间也常通过邻近作用能量彼此牵引，而不是通过某个单向的因果链条传播影响；在统计力学、社交网络、序列标注等问题中，节点之间的约束也往往是双向的。面对这种 “无明确方向、但具有强局部相互作用” 的概率结构，贝叶斯网络的有向图就不再是最自然的描述方式。

马尔可夫随机场（Markov Random Field，简称 MRF）正是从这种背景下诞生的一类模型。它使用无向图来描述系统中对称的局部依赖关系，将全局联合分布写成若干个势函数（potential functions）的组合。通过这种图结构，MRF 不仅能够直观描述复杂系统中的约束模式，还可以将高维概率分布分解为局部能量片段，从而让推断、计算与建模都变得更为可控。

MRF 的核心思想可以用一句话概括：

> **全局行为由局部相互作用决定，邻居决定一切。**

无向图提供了自然的对称结构，而基于团的因子化表达则把系统从 “全局不可处理” 的状态压缩成了 “局部可计算” 的形式。

![MRF 图像](src\content\posts\probabilistic-graphical-model\MRF结构1.jpg)

## 团因子化（Clique Factorization）

对于一个无向图 $G=(V,E)$ ，其中节点集合 $V$ 对应随机变量 $\{x_1,\dots,x_n\}$ ，MRF 假设联合分布可以因子化为若干团（clique）上的势函数。设 $\mathcal{C}$ 为所有团的集合，则联合分布写作：

$$
P(x_1,\dots,x_n) = \frac{1}{Z} \prod_{C\in \mathcal{C}} \psi_C(x_C)
$$

其中：

* (\psi_C(x_C)) 是 **团势函数** ，反映了团内变量之间的局部相互作用；
* (Z) 是归一化常数，称为 **分区函数（partition function）**：

$$
Z = \sum_x \prod_{C\in \mathcal{C}} \psi_C(x_C)
$$

势函数不需要满足特定形式，甚至不必归一化，它们仅需要满足非负性。
这给予了 MRF 极大的表达能力，例如：

* 图像平滑模型中，邻近像素倾向于取相似值；
* Ising/Potts 模型中，节点倾向于与邻居同态；
* 物理中的玻尔兹曼分布中，势函数与局部能量直接对应。

在建模上，团因子的形式是灵活的，你可以指定一对节点之间的势函数，也可以定义三元、四元团来捕捉更复杂的局部结构。

## 邻域结构（Neighborhood Structure）

MRF 的核心价值来自于它的条件独立性结构。对任意一个节点 $x_i$ ，其邻居集合记为 $\mathcal{N}(i)$ ，则 MRF 满足：

$$
x_i \perp x_{V \setminus ({i} \cup \mathcal{N}(i))} | x_{\mathcal{N}(i)}
$$

也就是说：

> **在给定邻居的条件下，节点与图中所有其他非邻居节点独立。**

这一点与贝叶斯网络不同：

BN 的独立性来自路径阻断（d-separation），而 MRF 的独立性完全来自 “邻居之外没有直接约束” 。

这种结构在很多系统中特别自然：

* 图像像素只和周围像素关联，而不受远处像素直接影响
* 物理粒子的作用通常由邻近粒子决定
* 标注序列中，如果条件随机场（CRF）采用链式结构，每个标签只与前后标签连接

这类基于邻域的局部性让 MRF 的推断高度可分解，也让势函数可解释性强。

## 玻尔兹曼分布（Boltzmann Distribution）

在经典物理、统计力学以及图像建模中，MRF 常常以能量形式表达，即将势函数改写为：

$$
\psi_C(x_C) = \exp(-E_C(x_C))
$$

联合分布变为：

$$
P(x) = \frac{1}{Z}\exp\Big(-\sum_{C\in\mathcal{C}}E_C(x_C)\Big)
$$

这种形式在两个方面极为重要：

1. **符合物理系统直觉**：能量越低越可能出现
2. **很多优化与采样方法都基于能量差构造**：如 Metropolis-Hastings、Gibbs Sampling

特别是 Gibbs 采样，只需按照：

$$
P(x_i \mid x_{\mathcal{N}(i)}) \propto \psi_i(x_i)\psi_{\text{对偶团}}(x_i, x_{\mathcal{N}(i)})
$$

即可完成局部更新，整个采样过程只在邻域中操作。

## 高斯随机场（Gaussian Random Field）

当随机变量是连续的，并且联合分布为高斯分布时，MRF 会出现一个极为美妙的性质：**条件独立性与精度矩阵的稀疏性完全对应** 。

设 $x \sim \mathcal{N}(0, \Sigma) \quad \Lambda = \Sigma^{-1}$ ，则有：

$$
\Lambda_{ij} = 0 \iff x_i \perp x_j \mid x_{{1,\dots,n}\setminus{i,j}}
$$

换句话说：

> **图中没有边 ⇒ 精度矩阵对应位置为零。**

这意味着图结构直接给出了联合分布在代数结构上的稀疏模式。因此 GMRF 在图像恢复、空间统计（如 Gaussian Process 的稀疏近似）、信号处理等领域极为常用。

对于任意分块高斯：

$$
x=
\begin{bmatrix}
x_a \ x_b
\end{bmatrix}
\sim \mathcal{N}\Big(
\begin{bmatrix}
\mu_a \ \mu_b
\end{bmatrix},
\begin{bmatrix}
\Sigma_{aa} & \Sigma_{ab}\\
\Sigma_{ba} & \Sigma_{bb}
\end{bmatrix}
\Big)
$$

其条件分布为：

$$
P(x_a|x_b) = \mathcal{N}\big(
\mu_a + \Sigma_{ab}\Sigma_{bb}^{-1}(x_b-\mu_b),
\Sigma_{aa}-\Sigma_{ab}\Sigma_{bb}^{-1}\Sigma_{ba}
\big)
$$

所有运算都退化为线性代数，非常便于推断。

## 推断机制（Inference Mechanism）

MRF 的推断方式与贝叶斯网络有共通的本质：都通过 **局部因子之间的消息传递** 来完成全局推断。不过由于图是无向的，因此消息传递更自然地基于团或因子图展开。

常用推断方法包括：

### 精确推断

对树或低树宽图，可使用：

* **Belief Propagation（BP）**
* **Junction Tree（连接树）方法**

这些方法在树结构上可以得到精确的边缘分布，而 MRF 在图像网格等图上通常需要先将图三角化再构造连接树。

### 近似推断

如果图较稠密，则精确方法不可行，需要采用近似推断：

* **MCMC（如 Gibbs Sampling、Metropolis-Hastings）**
* **变分推断（Variational Inference, VI）**
* **EP（Expectation Propagation）**

尤其在能量模型中，Gibbs 采样非常自然，因为每次更新仅依赖邻域结构：

$$
P(x_i | x_{\mathcal{N}(i)}) \propto \psi_i(x_i)\prod_{j\in \mathcal{N}(i)} \psi_{ij}(x_i, x_j)
$$

这一点与物理系统的逐点更新非常契合，使得 GMRF 和离散 MRF 都有广泛应用。

---

# 深层问题思考

1. 贝叶斯网络和马尔科夫随机场做出的概率假设分别是什么？

    ### 贝叶斯网络的概率假设

    **核心假设：联合分布可按节点的父节点进行链式因子化（有向因子化）。**

    $$
    P(x_1,\dots,x_n) = \prod_{i=1}^n P(x_i | pa(i))
    $$

    也就是说：

    > **BN 假设每个变量的概率分布只依赖它的父节点（Pa(i)），而与其他所有非后代无关。**

    因此 BN 隐含的概率结构是：

    - **每个节点的条件分布是局部的**
    只与其父节点有关，父节点之外的变量不会直接出现在该因子里。

    - **联合分布可以以一个“生成顺序”展开**
    即便顺序不唯一，BN 默认存在一种从父到子的生成因果结构。

    - **条件独立性来自有向图与 d-separation**
    例如一个节点在给定其父节点条件下，与非后代独立：

    $$
    x_i \perp \text{NonDescendants}(i) \mid pa(i)
    $$

    这些都是 BN 由 “有向因果结构” 赋予的概率假设。

    ### 马尔可夫随机场的概率假设

    **核心假设：联合分布可分解为无向图中各团（clique）上的势函数乘积（无向因子化）。**

    $$
    P(x_1,\dots,x_n) = \frac{1}{Z} \prod_{C\in \mathcal{C}} \psi_C(x_C)
    $$

    其中 $\psi_C$ 是团势函数。

    > **MRF 假设：节点的统计依赖关系由无向的“邻域”决定，独立性来自 Markov 性（局部性）。**

    因此 MRF 的概率结构包含：

    - **势函数只作用在团内变量上**
    团外的变量不出现在该势函数中，这构建了局部相互作用。

    - **联合分布由局部能量片段组合而成**
    其归一化常数 (Z) 可能非常难算，但这是模型固有的假设。

    - **条件独立性来自邻域结构（Markov Blanket）**
    具体地：

    $$
    x_i \perp x_{V\setminus({i}\cup \mathcal{N}(i))} \mid x_{\mathcal{N}(i)}
    $$

    即给定邻居后，与所有非邻居节点独立。

---

# 参考文献

## 贝叶斯网络

1. [Introduction to Bayesian Networks](https://medium.com/%40segunemmanuel46/introduction-to-bayesian-networks-2b62b4d35a52)

2. [概率图模型简明教程](https://jmaasch.github.io/pgm/)

3. [【Mathigon】贝叶斯推断和图模型](https://mathigon.org/course/bayesian-inference-and-graphical-models/introduction)

## 高斯网络

1. [高斯网络详细讲解](https://liangliangzhuang.github.io/MachineLearningNote/高斯网络.html)

2. [ML白板推导18：高斯网络](https://zhuanlan.zhihu.com/p/463764463)

## 马尔科夫随机场

1. [AI算法工程师手册：马尔可夫随机场](https://www.bookstack.cn/read/huaxiaozhuan-ai/spilt.3.a1c8cb11a2e246b2.md)

2. [【高中生讲机器学习】29. 马尔可夫随机场](https://blog.csdn.net/weixin_46836893/article/details/144287338)

3. [从贝叶斯理论到马尔可夫随机场（MRF）](https://blog.csdn.net/qq_40507857/article/details/110164691)

4. [【Alex_McAvoy】马尔可夫随机场](https://alex-mcavoy.github.io/mathematics/mathematical-statistics/a8049182.html)

5. [马尔可夫随机场和条件随机场](https://leimao.github.io/blog/Markov-Random-Field-VS-Conditional-Random-Field/)