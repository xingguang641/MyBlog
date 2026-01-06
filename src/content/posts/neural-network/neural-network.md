---
title: 【深度学习基本模型】第一节：神经网络
published: 2025-11-23
description: 介绍深度学习常见的模型
tags: [Deep Learning, Course]
category: DL Model
draft: false
---

# 神经网络基本结构

在机器学习的发展历程中，人们始终试图构建一种能够 **自动从数据中提取并表达复杂规律** 的模型。传统方法往往依赖人工设计的特征或受限的函数族，而在高维数据、复杂结构或大规模应用场景下，这些方法通常难以胜任。**神经网络（Neural Networks）** 的出现，为这一难题提供了一套统一而灵活的解决方案。它以高度参数化的结构为基础，能够在同一框架下处理图像、语音、文本等多种类型的数据，成为现代机器学习的重要支柱。

神经网络的思想最早来源于对生物神经系统的抽象。1940–1950 年代，McCulloch–Pitts 提出了最初的神经元逻辑模型，为这一研究方向奠定了数学基础。随后 Rosenblatt 提出的 **感知机（Perceptron）** 展示了利用简单神经元构建可学习分类器的可能性。进入 1980 年代，多层神经网络结构的提出以及反向传播算法（Backpropagation）的成功应用，使研究者得以训练更深层的网络；再加上数据规模与计算硬件的快速提升，神经网络逐渐发展为现代人工智能的核心方法之一。

![神经网络图像](src\content\posts\neural-network\神经网络1.png)

随着理论体系的完善，人们逐渐认识到神经网络不仅是受生物结构启发的计算模型，更可以从 **函数逼近（function approximation）** 与 **统计学习理论（statistical learning theory）** 的角度进行系统研究。经典的万能逼近定理说明，只要网络的结构足够宽或足够深，前馈神经网络便可以逼近几乎任意连续函数；而现代泛化理论也表明，即使参数维度极高，适当的结构选择、训练方式与正则化策略仍能够使模型具备良好的泛化能力。

在应用层面，神经网络已经形成覆盖广泛任务的一整套技术体系。卷积神经网络成为图像处理和视觉任务中的标准模型；循环网络与后来的注意力机制推动了自然语言处理的范式转变；而多层感知机则因其结构简单、适用性强，持续被用于各类预测与决策模块中。无论是在监督学习、生成模型还是强化学习中，神经网络都展现出强大的表达能力与适配性。

整体而言，神经网络从最初的生物启发式模型逐步演化为现代深度学习的核心基础设施。凭借其高表达力、可扩展性与普适建模能力，它已经成为理解当代人工智能体系不可或缺的一部分。

## 激活函数

**激活函数** 是神经网络中施加于神经元输出的非线性映射，用以调节输入信号在各层之间的传递方式。它决定了网络的局部响应结构，使每一层能够在不同输入区域呈现出截然不同的变换行为。通过这种可控的非线性，激活函数为模型提供了构建复杂映射所需的基础操作单元。

不同激活函数在光滑性、是否存在饱和区间、梯度幅度、数值稳定性以及计算代价等方面具有显著差异。这些性质会直接影响模型的梯度传播效率、参数更新动态以及最终的收敛表现。因此，激活函数不仅是神经网络结构的基本组成模块，更是训练效果与泛化能力的重要调控手段，需要根据具体任务与网络结构进行合理选择。

### 非线性层的必要性

在神经网络中引入非线性变换是提升模型表达能力的关键步骤。若网络仅由线性运算组成，即使堆叠任意多层，其整体仍可等价地被合并为一次线性映射，从而无法刻画真实任务中普遍存在的复杂 “输入–输出” 关系。非线性层的加入使网络能够构造更丰富的函数族，使模型具备对高维结构、局部变化及复杂决策边界进行拟合的能力，是现代深度学习模型得以成功的基础。

我们首先考虑最基本的前馈结构。设输入向量 $x \in \mathbb{R}^d$ ，第 1 层与第 2 层均为仿射变换：

$$
h = W_1 x + b_1 \qquad y = W_2 h + b_2
$$

将两层合并可得：

$$
y = W_2 (W_1 x + b_1) + b_2
= (W_2 W_1) x + (W_2 b_1 + b_2)
$$

即使网络包含更多层，只要每层均为线性（或仿射）变换：

$$
h^{(k)} = W_k h^{(k-1)} + b_k
$$

其整体仍可折叠为单一映射：

$$
h^{(L)} = W_{\mathrm{eff}} x + b_{\mathrm{eff}}
$$

因此，一个完全由线性层堆叠而成的前馈网络，其函数族始终为：

$$
\mathcal{F}_\text{linear}
= \{ x \mapsto Wx + b \mid W, b \text{ 任意} \}
$$

无法逼近绝大多数非线性函数族（如 XOR、分段复杂决策边界、图像—语言映射等）。这一限制直接导致模型无法处理现代机器学习中常见的高复杂度任务。

在网络中引入非线性函数 $\sigma(\cdot)$ 后，每层结构变为：

$$
h^{(k)} = \sigma(W_k h^{(k-1)} + b_k)
$$

最终得到的函数族形式为：

$$
\mathcal{F}_{\mathrm{NN}}
= \Big\{
x \mapsto
W_L\, \sigma\!\Big( W_{L-1}\, \sigma(\cdots \sigma(W_1 x + b_1)\cdots) + b_{L-1} \Big) + b_L
\Big\}
$$

该空间包含大量可组合的非线性结构，其表达能力远超线性模型。根据通用逼近定理（Universal Approximation Theorem），只要激活函数满足适当条件（如连续、非线性、非多项式），一个具有有限宽度的前馈网络即可逼近任意连续函数：

$$
\forall f \in C([0,1]^d), \forall \varepsilon > 0 \qquad \exists \text{ 神经网络 } g \text{ 使得 } |f - g|_\infty < \varepsilon.
$$

这意味着非线性层使得网络能够构建分段非线性、多尺度嵌套结构，从而获得足够丰富的函数表达能力来处理实际应用。

从优化角度看，若网络仅由线性层构成，其雅可比与 Hessian 的结构过于简单，梯度地形贫乏，不利于模型训练。引入非线性后，第 $k$ 层的梯度传播形式变为：

$$
\frac{\partial h^{(k)}}{\partial h^{(k-1)}}
= \sigma'(z^{(k)}) W_k
\qquad
z^{(k)} = W_k h^{(k-1)} + b_k
$$

其中 $\sigma'$ 的调制使梯度在传播过程中呈现更丰富的变化结构，从而形成更有利于优化的几何特性，使深度网络的训练成为可能并保持稳定。

### 常见的激活函数

在构建神经网络时，激活函数的选择会对模型的表达能力、梯度传播特性以及训练稳定性产生重要影响。不同激活函数在光滑性、梯度饱和、输出范围以及数值稳定性等方面各具特点。下文将介绍几种在实际应用中被广泛采用的激活函数及其核心性质。

1. **Sigmoid 函数**

    Sigmoid 函数是最早应用于神经网络的激活函数之一，其形式为：

    $$
    \sigma(x) = \frac{1}{1 + e^{-x}}
    $$

    Sigmoid 函数将输入映射到 $(0,1)$ ，具备平滑可微的特性，因此在概率建模或二分类输出层中仍然常见。然而Sigmoid 函数的梯度在 $|x|$ 增大时迅速趋近于零，导致反向传播过程中容易出现梯度消失现象，从而限制网络的可训练深度。

2. **Tanh 函数**

    Tanh 函数是 Sigmoid 函数的平移缩放版本：

    $$
    \tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}
    $$

    其输出范围为 $(-1,1)$ ，在零点附近呈更陡峭的响应，相比 Sigmoid 函数更适合用于隐藏层。然而 Tanh 函数同样存在饱和区域，仍可能在深层网络中引发梯度衰减。

3. **ReLU 函数**

    ReLU（Rectified Linear Unit）函数是现代深度学习中使用最广泛的激活函数，其形式为：

    $$
    \operatorname{ReLU}(x) = \max(0, x)
    $$

    ReLU 函数在正半轴保持线性，不会饱和，使其在深度网络中能维持较好的梯度传播效率。同时，其稀疏性特征（大量输出为零）在一定程度上有助于提升表示能力和训练稳定性。然而，负半轴梯度为零可能导致 “神经元死亡（dead ReLU）” 现象，参数可能无法再更新。

4. **Leaky ReLU 函数**

    为缓解 ReLU 函数在负半轴完全 “关闭” 的问题，Leaky ReLU 函数引入一个小的负向斜率：

    $$
    \operatorname{LeakyReLU}(x) =
    \begin{cases}
    x, & x \ge 0 \\
    \alpha x, & x < 0
    \end{cases}
    \quad \alpha \in (0,1)
    $$

    这种设计减少了死神经元的概率，使梯度在全域保持非零，有助于更稳定的深层训练。

5. **Parametric ReLU 函数**

    PReLU 函数将 Leaky ReLU 函数的斜率参数设为可学习变量：

    $$
    \operatorname{LeakyReLU}(x) =
    \begin{cases}
    x, & x \ge 0 \\
    a x, & x < 0
    \end{cases}
    \quad a \text{ 可学习}
    $$

    能够根据数据自动调节负半轴的响应程度，使网络在不同任务中获得更灵活的非线性结构，但也会引入额外参数，需要一定正则化以避免过拟合。

6. **GELU 函数**

    GELU（Gaussian Error Linear Unit）函数是近年来在大规模预训练模型中广泛使用的激活函数（如 BERT、Vision Transformer）。其近似形式为：

    $$
    \operatorname{GELU}(x) = x \Phi(x)
    $$

    其中 $\Phi(x)$ 是标准正态分布的累积分布函数。GELU 函数具有平滑、概率式门控的特性，使得在输入较大时接近线性，在输入较小时平滑地抑制信号。相比 ReLU 函数，其曲线更自然地反映 “按概率保留” 信息的机制，适用于庞大模型的稳定训练。

7. **Softplus 函数**

    Softplus 函数是 ReLU 函数的光滑近似：

    $$
    \operatorname{Softplus}(x) = \log(1 + e^x)
    $$

    与 ReLU 函数不同，Softplus 函数在全域可微，梯度连续，对于某些需要光滑优化几何结构的任务具有优势。但其计算成本略高，且在大规模神经网络中不如 ReLU 常见。

## 损失函数

**损失函数** 用于衡量模型预测结果与真实观测之间的差异，是神经网络训练过程中优化的核心目标。设模型输出为 $\hat{y} = f_\theta(x)$ ，真实标签为 $y$ ，则单个样本的损失可写为：

$$
\ell(\hat{y}, y)
$$

在整个数据集上，总损失函数为：

$$
\mathcal{L}(\theta) = \sum_{i=1}^{n} \ell(\hat{y}_i, y_i)
$$

训练的目标是通过优化参数 $\theta$ 来最小化总损失：

$$
\hat{\theta} = \arg\min_{\theta} \mathcal{L}(\theta)
$$

### 极大似然估计

许多常见的损失函数都可以从 **极大似然估计**（Maximum Likelihood Estimation，简称 MLE）中得到自然解释。其关键观点是：神经网络不仅是一个函数拟合器，更可以理解为一个参数化的概率模型。假设数据集 $\mathcal{D} = {(x_i, y_i)}_{i=1}^n$ 独立同分布，并且每个标签的条件分布由参数 $\theta$ 控制，即：

$$
P(y_i | x_i, \theta)
$$

那么整个数据集的联合概率为：

$$
P(\mathcal{D} | \theta) = \prod_{i=1}^{n} P(y_i | x_i, \theta)
$$

MLE 的目标是选择能使数据最 “可能” 出现的参数：

$$
\hat\theta = \arg\max_\theta P(\mathcal{D}|\theta)
$$

为了便于数值计算，一般对似然取对数，将连乘转化为求和，得到对数似然：

$$
\ell(\theta) = \sum_{i=1}^{n} \log P(y_i | x_i, \theta)
$$

将损失定义为负对数似然，即：

$$
\mathcal{L}(\theta) = - \sum_{i=1}^{n} \log P(y_i | x_i, \theta)
$$

此时 **最小化损失函数** 就等价于 **最大化对数似然** ，从而实现 MLE。

这一视角解释了许多经典损失函数的统计来源：

* **回归任务**：若假设观测噪声服从高斯分布，则 MLE 等价于最小化均方误差。
* **分类任务**：若类别服从多项分布，则 MLE 自然导出交叉熵损失。
* **生成模型**：KL 散度等价于对数似然的推广，可理解为最大化真实分布在模型分布下的概率。

因此，损失函数不仅仅是 “需要优化的量” ，它从统计学角度反映了模型对数据生成机制的假设。通过最小化损失，我们实际上在执行最大似然估计，使模型的预测分布尽可能贴近训练数据的真实分布。借助梯度下降类优化方法，这一过程得以高效实现，并为模型带来良好的拟合能力与泛化性能。

### 常见的损失函数

在神经网络训练中，损失函数用于量化模型预测结果与真实观测之间的差异。损失函数不仅定义了优化目标，也反映了模型对数据生成过程的概率假设。不同损失函数适用于不同任务和数据分布，下文将介绍几种经典且常用的损失函数，并分析它们的来源、推导及设计动机。

1. **均方误差（Mean Squared Error）**

    均方误差是回归问题中最常用的损失函数，用于衡量预测值与真实值的平方差。设模型预测输出为 $\hat{y} = f_\theta(x)$ ，真实值为 $y$ ，单样本损失为：

    $$
    \ell_{\text{MSE}}(\hat{y}, y) = (\hat{y} - y)^2
    $$

    均方误差的设计来源于极大似然估计。假设观测值服从高斯分布：

    $$
    y \sim \mathcal{N}(\hat{y}, \sigma^2)
    $$

    则条件概率为：

    $$
    P(y | x, \theta) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\Big(-\frac{(y - \hat{y})^2}{2\sigma^2}\Big)
    $$

    对数似然函数为：

    $$
    \ell(\theta) = \sum_{i=1}^n \log P(y_i | x_i, \theta) \propto - \sum_{i=1}^n (y_i - \hat{y}_i)^2
    $$

    因此，最小化均方误差等价于最大化高斯似然函数。MSE 适合连续值预测，梯度平滑，优化稳定，但对异常值敏感。


2. **交叉熵损失（Cross-Entropy Loss）**

    交叉熵损失常用于分类问题，用于衡量预测概率分布 $\hat{y}$ 与真实类别分布 $y$ 的差异。单样本损失为：

    $$
    \ell_{\text{CE}}(\hat{y}, y) = - \sum_c y_c \log \hat{y}_c
    $$

    假设类别服从多项分布，则每个样本的条件概率为：

    $$
    P(y | x, \theta) = \prod_c \hat{y}_c^{y_c}
    $$

    对数似然函数为：

    $$
    \ell(\theta) = \sum_i \sum_c y_{i,c} \log \hat{y}_{i,c}
    $$

    最大化对数似然即最小化交叉熵损失，因此交叉熵损失是多项分布下的 MLE。它能够对概率预测直接建模，并提供平滑可导的梯度，适合梯度优化。

3. **焦点损失（Focal Loss）**

    焦点损失是交叉熵损失的一种改进，主要用于处理类别不平衡问题。单样本损失为：

    $$
    \ell_{\text{Focal}}(\hat{y}, y) = - (1 - \hat{y}_t)^\gamma \log \hat{y}_t
    $$

    其中 $\hat{y}_t$ 是真实类别的预测概率，$\gamma > 0$ 为调节因子。

    焦点损失在极大似然的基础上引入难样本加权机制，降低易分类样本的贡献，使模型更关注难分类样本。本质上仍是对数似然优化的变体，但适用于长尾类别或严重不平衡的数据集。

4. **KL 散度损失（KL Divergence Loss）**

    KL 散度损失用于衡量两个概率分布 $P$（真实分布）和 $Q$（预测分布）之间的差异：

    $$
    \ell_{\text{KL}}(P \parallel Q) = \sum_i P(i) \log \frac{P(i)}{Q(i)}
    $$

    其设计来源于信息论，量化预测分布与真实分布的偏离。在概率建模中，最小化 KL 散度等价于最大化对数似然的推广，即在分布匹配任务中寻找最优参数，使预测分布尽量接近目标分布。常用于生成模型、知识蒸馏等场景。

## 梯度下降

在训练神经网络时，我们的目标是找到一组参数，使得模型的损失函数尽可能小。形式上，这可以表示为一个优化问题：

$$
\theta^* = \arg\min_\theta L(\theta)
$$

然而现实中的损失函数往往非常复杂：它是由无数层线性变换、激活函数、归一化等嵌套组合而成的高维非凸函数，既没有封闭形式，也无法像传统统计模型那样通过推导直接解出最优点。再加上参数量动辄成千上万甚至上亿，任何依赖 Hessian 或二阶信息的方式在计算上都会变得不现实。

尽管如此，我们仍然可以利用一个可靠的局部信息 ———— 梯度。梯度告诉我们在当前参数位置附近，损失函数的增长趋势；我们只需要朝着与梯度相反的方向前进，就能让损失下降。也就是说，梯度下降并不是在全局范围内 “找到最优解” ，而是在复杂地形中做一种 **连续的、可迭代的局部下降** 过程：每一步都基于当前梯度进行微调，把参数推向 “更低的方向” 。

于是就有了最基础的更新规则：

$$
\theta \leftarrow \theta - \eta \nabla_\theta L(\theta)
$$

这里的学习率 $\eta$ 决定了每一步的步幅：步子太大可能直接越过谷底，使训练发散；步子太小则下降缓慢。由于梯度可以通过链式法则高效计算，我们可以在每个 mini-batch 上反复执行上述更新，从而逐步逼近损失函数的低谷。这种方式不仅计算成本可控，也非常适合参数量庞大的深度学习模型。

### 反向传播

为了让梯度下降在神经网络中真正可行，我们必须解决一个核心问题：**梯度从哪里来** 。虽然损失函数是所有层共同作用的结果，但每一层的参数对最终损失的贡献并不是直接可见的。尤其在深度模型中，几十层甚至上百层的网络结构，使得手动推导每个参数的偏导数几乎不可能。因此，我们需要一种系统化的方法，让梯度从网络输出一路传回输入端，沿途计算每个中间变量的贡献。

这正是 **反向传播（Backpropagation）** 的目的。其核心思想非常直观：如果前向传播是 “从输入一路计算到输出” ，那么反向传播就是 “从损失函数开始，把梯度沿着计算图回传” 。

也就是说：

> **所有参数指导此次损失函数的更新，而损失函数的变化反过来指导所有参数的更新。**

由于神经网络可以看作多层函数的复合，链式法则告诉我们：对任意一层求导时，只需将上游梯度与自身局部导数相乘即可。反向传播在网络中不断重复这一过程：先计算损失对输出的梯度，然后沿计算路径逐层回流，每经过一层，就根据该层的局部结构（如线性变换、激活函数、卷积等）计算新的梯度，并传递给前一层。最终，每个参数都会得到属于自己的梯度，而这些梯度正是梯度下降更新所需要的。

![反向传播图像](src\content\posts\neural-network\反向传播1.png)

在计算机中，**计算图（Computation Graph）** 模块化了整个反向传播过程。每个计算节点负责一个简单操作，梯度沿图结构逐层回传，使网络的梯度计算既系统化又高效。前向传播时，计算图记录每一次加法、乘法、矩阵运算、激活函数等操作的输出，形成数据流图：输入从图底部进入，经过各层线性或非线性变换，最终得到输出。每个节点只执行简单操作，但所有节点组合起来构成完整前向计算路径，同时保存中间变量以备反向传播使用。

![计算图图像](src\content\posts\neural-network\计算图1.png)

反向传播时，梯度从损失函数顶端沿图结构回流。每个节点利用前向传播保存的中间值和局部变换规则，计算局部导数并传递梯度给输入节点。链式法则在此体现得非常自然：节点只需知道自身局部导数和上游梯度，即可计算并传递下游梯度。

![计算图图像](src\content\posts\neural-network\计算图2.png)

计算图的模块化让高维复杂函数拆解成可处理的小块，使反向传播在计算机中得以高效执行。无论网络结构多复杂，包括注意力机制、归一化层甚至自定义运算，只要每个算子实现自己的前向与反向规则，整个网络的梯度都能被自动、稳定地计算。现代深度学习框架（如 PyTorch、TensorFlow）正是基于这种 **自动求导（autograd）** 系统构建的：它们维护一张动态计算图，并在需要梯度时沿图回溯。

通过计算图，梯度下降成为训练深度神经网络的可行途径。它将看似无法直接求导的复杂函数拆解成可处理的小计算单元，从而实现高效、稳定的训练。

### 梯度下降优化

基础的梯度下降（包括随机梯度下降或 mini-batch 形式）虽然结构简单、易于实现，但在实际的深度学习训练中常表现出明显的局限性。最突出的问题是 **收敛效率不足**：深度神经网络的损失函数通常高度非凸，具有明显的 **各向异性曲率（Anisotropic Curvature）**。在高曲率方向，梯度下降因步长受限而推进缓慢；在低曲率方向，又容易出现剧烈振荡，使整体收敛速度受制于最 “难走” 的方向。

此外，传统梯度下降为所有参数统一设置一个全局学习率，这在高维空间中显然不够灵活。不同参数的梯度特性往往差异巨大：某些参数长期保持大梯度，而另一些参数则极为稀疏或变化缓慢。在这种情况下，单一学习率会导致某些维度更新过度，而另一些维度更新不足，直接影响训练效果。

深度模型的损失景观还广泛存在 **鞍点（saddle point）** 、**平坦区域（plateau）** 、甚至 **梯度消失区域（vanishing gradient region）**。在这些区域内，梯度的方向信息几乎不提供有效下降方向，使得纯梯度下降极易停滞在不足以代表局部极小点甚至欠优化的区域附近。

基于上述挑战，各类优化方法从不同维度对梯度下降进行了加强和扩展：

* **二阶方法（如 Newton 法）** 尝试利用 Hessian 的局部曲率信息给出更接近最优步长的更新
* **动量型方法（Momentum, Nesterov）** 通过引入累积梯度，使优化过程具备 “惯性” ，在低曲率方向加速、在高曲率方向抑制振荡
* **自适应学习率方法（AdaGrad, RMSProp, Adam）** 通过历史梯度的统计量为每个参数维度动态调整步长，使优化能够自动适应数据稀疏性与梯度尺度差异

这些方法共同构成了现代深度学习训练中最常见、最核心的优化策略，使得在高维非凸环境下的优化不再完全依赖简单梯度，而是能更有效地探索损失函数的几何结构，从而获得更快、更稳定的收敛。

1. **牛顿法**

    牛顿法是一种二阶优化方法，其核心思想是利用梯度和 Hessian 矩阵（目标函数的二阶导数信息）来加速收敛。更新公式为：

    $$
    \theta_{t} = \theta_{t-1} - H^{-1}*{t-1} \nabla f(\theta*{t-1})
    $$

    其中 $\nabla f(\theta_{t-1})$ 是梯度，$H_{t-1}$ 是 Hessian 矩阵，即目标函数在 $\theta_{t-1}$ 处的二阶导数矩阵。

    通过引入 Hessian，牛顿法不仅考虑梯度方向，还利用曲率信息调整步长，使优化沿曲率适宜的方向快速收敛。直观比喻：想象在山谷中行走，不仅看坡度（梯度），还考虑坡面弯曲程度（曲率），每一步都更精准地接近最低点。

    **牛顿法的局限性**：计算和存储 Hessian 在高维空间中非常昂贵，而且 Hessian 可能不可逆或条件数差，容易导致数值不稳定。因此在深度学习中，牛顿法通常不直接使用，而是衍生出拟牛顿法（如 BFGS）或结合一阶方法的混合策略。

2. **动量法**

    动量法通过引入 “惯性” ，让参数更新不仅依赖当前梯度，还参考过去的更新方向，从而加速收敛并抑制震荡。更新公式为：

    $$
    v_t = \beta v_{t-1} + \eta \nabla f(\theta_{t-1}) \quad \theta_t = \theta_{t-1} - v_t
    $$

    其中 $v_t$ 是累积的动量，$\beta \in [0,1)$ 是动量系数，$\eta$ 是基础学习率。

    动量的作用类似物理惯性，如果梯度连续指向某个方向，动量会让更新 “加速前进” ，如果梯度方向频繁变化，动量会抑制震荡。直观比喻：想象一个小球滚动下山，小球会沿山谷逐渐加速，而不会因为局部凸起轻易停下来。

    **动量法的局限性**：需要调节 $\beta$ 和 $\eta$ 的组合，过大会导致过冲，过小则动量作用不明显。Nesterov 方法在此基础上做了改进。

3. **Nesterov 加速梯度**

    Nesterov 的创新在于 “预见未来” 。我们可以在计算梯度之前，先沿动量方向进行一步预测，然后在预测位置计算梯度。更新公式为：

    $$
    v_t = \beta v_{t-1} + \eta \nabla f(\theta_{t-1} - \beta v_{t-1}) \quad \theta_t = \theta_{t-1} - v_t
    $$

    与普通动量法不同，梯度不是在当前参数位置计算，而是在 “预测的未来位置” 计算，从而在动量方向上进行修正。直观比喻：就像开车时，不仅根据当前速度和方向踩油门，还提前观察前方路况来调整，避免过冲或过慢。Nesterov 往往比普通动量法收敛更快且更稳定。

4. **AdaGrad**

    AdaGrad 的核心思想是为每个参数维度自适应地调整学习率，使得稀疏梯度参数可以走得更快，而频繁更新的参数步长自动减小。更新公式为：

    $$
    \theta_{t,i} = \theta_{t-1,i} - \frac{\eta}{\sqrt{\sum_{k=1}^{t} g_{k,i}^2} + \epsilon} g_{t,i}
    $$

    其中 $g_{t,i}$ 是第 $i$ 个参数在第 $t$ 步的梯度，$\eta$ 是基础学习率，$\epsilon$ 是防止除零的小常数。
    
    累积梯度 $\displaystyle \sum_{k=1}^{t} g_{k,i}^2$ 会让频繁更新的参数步长自动减小，而稀疏梯度参数保持较大步长。直观比喻：对于常走的路自动缩短步子，对于没走过的路保持大步，使稀疏参数也能有效训练。
    
    **AdaGrad 的局限性**：累积梯度不断增大导致后期步长变得过小，因此 RMSProp 对此做了改进。

5. **RMSProp**

    RMSProp 是 AdaGrad 的改进版，它通过指数加权平均只关注近期梯度，避免步长过早减小。更新公式为：

    $$
    s_t = \gamma s_{t-1} + (1-\gamma) g_t^2 \quad \theta_t = \theta_{t-1} - \frac{\eta}{\sqrt{s_t + \epsilon}} g_t
    $$

    其中 $s_t$ 是梯度平方的指数加权平均，$\gamma$ 通常取 0.9 左右。
    
    相比 AdaGrad，RMSProp 可以保持步长在训练后期仍然合理，尤其适合非平稳目标函数，如循环神经网络。直观比喻：像只参考最近的路况来调整步幅，而不是累积所有历史变化，使步伐保持灵活且稳健。

6. **Adam**

    Adam 将动量法与 RMSProp 结合，既考虑梯度的一阶矩（动量），又考虑二阶矩（梯度平方的指数平均），从而自适应调整每个参数步长。更新公式为：

    $$
    m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t \quad v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2
    $$

    $$
    \hat{m}_t = \frac{m_t}{1-\beta_1^t} \quad \hat{v}*t = \frac{v_t}{1-\beta_2^t} \quad \theta_t = \theta*{t-1} - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}
    $$

    其中 $m_t$ 和 $v_t$ 分别是一阶和二阶矩的指数加权平均，$\hat{m}_t, \hat{v}_t$ 是偏置修正。
    
    Adam 的优势是收敛快、对超参数不敏感，并且对稀疏梯度也友好。直观比喻：既沿惯性方向前进（动量），又根据最近路况自动调节步幅（RMS），像是智能化的行走策略，既快速又稳健。
    
    **Adam 的局限性**：在某些凸优化问题上可能不如 SGD 收敛到全局最优，常结合学习率衰减使用。

### 梯度消失

梯度消失是指在网络反向传播过程中，梯度逐层变得非常小，几乎接近零，导致靠近输入层的参数更新极其缓慢，网络训练困难甚至停滞。

数学上，如果一个深度网络有 $L$ 层，梯度计算可表示为链式法则：

$$
\frac{\partial L}{\partial \theta_1} = \frac{\partial L}{\partial h_L} \cdot \frac{\partial h_L}{\partial h_{L-1}} \cdot \cdots \cdot \frac{\partial h_2}{\partial h_1} \cdot \frac{\partial h_1}{\partial \theta_1}
$$

如果每一层的导数 $\frac{\partial h_i}{\partial h_{i-1}}$ 小于 1，则连乘 $L$ 层后，梯度会迅速衰减：

$$
\prod_{i=1}^L \frac{\partial h_i}{\partial h_{i-1}} \approx 0
$$

**解决方法**：

1. **使用合适的激活函数**

   * Sigmoid 和 tanh 在输入过大或过小时导数接近零，会加剧梯度消失。
   * ReLU 及其变体（Leaky ReLU、ELU）能保持较大梯度，有助于缓解问题。

2. **权重初始化策略**

   * Xavier/Glorot 初始化：适合 tanh 激活，使前向输出和反向梯度方差稳定。
   * Kaiming He 初始化：适合 ReLU 激活，保证梯度在深层传播时不衰减。

3. **归一化层**

   BatchNorm 或 LayerNorm 可以稳定各层输入分布，使梯度更容易传播。

4. **残差连接（Residual Connection）**

   在 ResNet 中，通过跳跃连接 $h_{l+1} = h_l + F(h_l)$ 让梯度能够直接流向前面层，从而显著缓解梯度消失。

> 关于参数初始化方法可以观看下面两个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=343521101&bvid=BV1r94y1Q7eG&cid=778240021&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=301032447&bvid=BV1PF411K7nb&cid=778242757&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

### 梯度爆炸

梯度爆炸是指在反向传播过程中，梯度快速增大，导致参数更新过大，使训练不稳定甚至发散。

同样用链式法则，如果每层导数大于 1，则连乘会导致梯度呈指数增长：

$$
\prod_{i=1}^L \frac{\partial h_i}{\partial h_{i-1}} \gg 1
$$

这种现象在循环神经网络（RNN）、LSTM 以及深层前馈网络中尤为常见。

**解决方法**：

1. **梯度裁剪（Gradient Clipping）**

   将梯度限制在预设阈值范围内：

   $$
    g \leftarrow g \cdot \frac{\text{clip\_norm}}{\max\bigl(\text{clip\_norm},\,\lVert g\rVert_2\bigr)}
    $$

   常用于 RNN、LSTM、Transformer 等网络。

2. **合理的权重初始化**

   避免初始权重过大，使前向输出和梯度不会指数放大。

3. **使用稳定的激活函数**

   ReLU 系列通常比 Sigmoid/Tanh 更稳健，能减缓梯度指数增长。

4. **归一化层**

   BatchNorm、LayerNorm 可以限制每层激活值范围，从而间接控制梯度规模。

> 关于归一化层可以观看下面两个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=115194411878768&bvid=BV1hqpjzrEmT&cid=32345950291&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=401088977&bvid=BV12d4y1f74C&cid=1126872119&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

---

# 神经网络层级结构

神经网络由多种类型的层组合而成，每种层在模型中承担不同功能，相互协作以实现复杂的特征学习和表示能力。有的层负责线性变换和特征映射，将输入信号转换为更适合后续处理的形式；有的层专注于局部特征提取和空间结构分析，能够捕捉数据中的模式与结构信息；还有一些层用于稳定训练过程，通过调整激活分布或梯度传递，使网络收敛更快、更平稳；另外一些层则专注于防止模型过拟合，提高泛化能力，确保网络在未见数据上也能保持良好表现。

这种层的组合不仅使神经网络具有强大的表达能力，也让模型能够在高维、非线性的复杂任务中学习到有效特征。不同类型的层通常相互配合：例如卷积层提取局部特征，池化层进行下采样，归一化层保持数值稳定，正则化层防止过拟合，最终线性层将抽象特征映射到具体任务输出。这种模块化的设计思路，使得神经网络既灵活又高效，能够适应图像、语音、文本等各种不同类型的数据。

接下来，我们将按照功能类别，逐步介绍神经网络中常用的各类层及其作用、计算原理和直观理解。

## 全连接层

全连接层通常指线性变换层（Linear Transformation Layer），是神经网络中最基础的模块。它的核心功能是对输入向量进行线性映射，将输入特征组合成新的特征表示：

$$
y = W x + b
$$

其中 $x$ 是输入向量，$W$ 是权重矩阵，$b$ 是偏置向量，$y$ 是输出向量。通过训练，网络学习到最合适的 $W$ 和 $b$，使输出能够反映输入特征之间的关系。

直观上，可以把线性层看作 “信号混合器” ，它把输入中的各类信号按不同权重组合成新的信号，再交给下一层处理。单独的线性层无法表达复杂非线性关系，但与激活函数组合后，就能构建深层网络，实现强大的特征表示能力。全连接层广泛用于分类和回归任务，尤其是网络的最后输出层。需要注意的是，参数量会随输入和输出维度增加而快速增长，因此通常与卷积层或降维层结合使用以平衡效率和表达能力。

**PyTorch 示例**：

```py frame="code" title="main.py"
import torch
import torch.nn as nn

# 定义一个线性层
# 输入维度 128，输出维度 64
fc_layer = nn.Linear(in_features=128, out_features=64)

# 输入数据，batch_size=32, 特征维度=128
x = torch.randn(32, 128)

# 前向计算
y = fc_layer(x)
print(y.shape)  # 输出: torch.Size([32, 64])
```

## 卷积类层

卷积层不仅仅是单一的卷积操作。在深度学习中，根据计算效率、参数量、感受野和任务需求，卷积层有多种变体，每种都有特定的优势和适用场景。例如，普通卷积适用于基础特征提取，组卷积可以显著降低计算量，深度可分离卷积则在轻量化网络中表现优异，而空洞卷积可以在不增加参数的情况下扩大感受野。通过这些不同的卷积层，神经网络能够灵活地提取多尺度、多通道的特征，从而在图像识别、语义分割、生成模型等任务中发挥核心作用。常见卷积类层包括：

1. **普通卷积（Conv2d）**

   普通二维卷积是最基本的卷积操作，用于从输入特征图中提取局部特征。其计算公式为：

    $$
    y_{i,j,k} = \sum_{c=1}^{C_\text{in}} \sum_{m=1}^{K_h} \sum_{n=1}^{K_w} x_{c,i+m,j+n} \cdot W_{k,c,m,n} + b_k
    $$

   其中 $x$ 是输入特征图，$W$ 是卷积核权重，$b$ 是偏置，$C_\text{in}$ 是输入通道数，$K_h, K_w$ 是卷积核高宽，输出特征图的通道数为卷积核个数 $k$。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    import torch
    import torch.nn as nn

    conv = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=1, padding=1)
    x = torch.randn(1, 3, 32, 32)  # batch=1, C=3, H=32, W=32
    y = conv(x)
    print(y.shape)  # torch.Size([1, 16, 32, 32])
    ```

2. **组卷积（Group Convolution）**

    组卷积将输入通道分为若干组，每组独立进行卷积，从而减少参数量和计算量。其计算公式为：

    $$
    y^{(g)} = \text{Conv}(x^{(g)}, W^{(g)}) + b^{(g)}
    $$

    其中 $x^{(g)}$ 和 $W^{(g)}$ 分别是第 $g$ 组的输入通道和卷积核权重，输出 $y^{(g)}$ 为该组卷积结果。组卷积广泛用于 ResNeXt 等网络结构中。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    conv_group = nn.Conv2d(32, 64, kernel_size=3, groups=4, padding=1)
    x = torch.randn(1, 32, 32, 32)
    y = conv_group(x)
    print(y.shape)  # torch.Size([1, 64, 32, 32])
    ```

3. **深度可分离卷积（Depthwise Separable Conv）**

    深度可分离卷积将卷积操作拆分为两步：先进行深度卷积（每个输入通道独立卷积），再进行逐点卷积（1×1 卷积用于融合通道），以降低计算量和参数量。计算公式为：

    $$
    y = \text{PointwiseConv}(\text{DepthwiseConv}(x))
    $$

    其中 $\text{DepthwiseConv}$ 对每个通道独立处理，$\text{PointwiseConv}$ 用于通道间线性组合。该操作广泛用于轻量化网络如 MobileNet。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    # 深度卷积
    depthwise = nn.Conv2d(32, 32, kernel_size=3, groups=32, padding=1)
    # 逐点卷积
    pointwise = nn.Conv2d(32, 64, kernel_size=1)
    x = torch.randn(1, 32, 32, 32)
    y = depthwise(x)
    y = pointwise(y)
    print(y.shape)  # torch.Size([1, 64, 32, 32])
    ```

4. **转置卷积（Transposed Conv）**

    转置卷积用于上采样操作，将小尺寸特征图映射到更大尺寸，常用于生成模型（如 GAN、Autoencoder）或语义分割中。计算公式为：

    $$
    y = \text{TransposedConv}(x, W) + b
    $$

    其中 $x$ 为输入特征图，$W$ 为卷积核权重，$b$ 为偏置。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    conv_trans = nn.ConvTranspose2d(16, 8, kernel_size=3, stride=2, padding=1, output_padding=1)
    x = torch.randn(1, 16, 16, 16)
    y = conv_trans(x)
    print(y.shape)  # torch.Size([1, 8, 32, 32])
    ```

5. **空洞卷积（Atrous Conv）**

    空洞卷积在卷积核内部插入间隔（空洞），以扩大感受野而不增加参数量。计算公式为：

    $$
    y_{i,j} = \sum_{m,n} x_{i+d \cdot m, j+d \cdot n} \cdot W_{m,n}
    $$

    其中 $d$ 是空洞率，$x$ 为输入特征图，$W$ 为卷积核权重。空洞卷积常用于语义分割和时序建模（如 WaveNet）。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    dilated_conv = nn.Conv2d(3, 16, kernel_size=3, dilation=2, padding=2)
    x = torch.randn(1, 3, 32, 32)
    y = dilated_conv(x)
    print(y.shape)  # torch.Size([1, 16, 32, 32])
    ```

## 池化类层

池化层的主要作用是对特征图进行下采样，从而减小空间尺寸，降低计算量和参数量，同时增强网络对平移或微小变形的鲁棒性。通过池化，网络能够保留最重要的特征信息，而忽略局部微小变化，从而提升泛化能力。常见的池化层有多种形式，例如最大池化（Max Pooling）提取局部最显著特征，平均池化（Average Pooling）则关注局部整体信息，而全局池化（Global Pooling）可以将整个特征图压缩为单个数值，用于分类任务的特征汇总。这些不同类型的池化层使网络在保持关键特征的同时，有效降低了计算复杂度。常见池化层包括：

1. **最大池化（Max Pooling）**

    最大池化在池化窗口内取最大值，以保留最显著的特征。计算公式为：

    $$
    y_{i,j} = \max_{(p,q)\in \text{window}} x_{i+p,j+q}
    $$

    其中 $x$ 为输入特征图，$\text{window}$ 为池化区域，$y$ 为下采样后的输出特征图。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    max_pool = nn.MaxPool2d(kernel_size=2, stride=2)
    x = torch.randn(1, 16, 32, 32)
    y = max_pool(x)
    print(y.shape)  # torch.Size([1, 16, 16, 16])
    ```

2. **平均池化（Average Pooling）**

    平均池化在池化窗口内计算平均值，以保留局部特征的整体分布。计算公式为：

    $$
    y_{i,j} = \frac{1}{N} \sum_{(p,q)\in \text{window}} x_{i+p,j+q}
    $$

    其中 $x$ 为输入特征图，$\text{window}$ 为池化区域，$N$ 为窗口内元素数量，$y$ 为下采样后的输出特征图。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)
    x = torch.randn(1, 16, 32, 32)
    y = avg_pool(x)
    print(y.shape)  # torch.Size([1, 16, 16, 16])
    ```

3. **全局平均池化（Global Average Pooling）**

    全局平均池化对整个特征图进行平均操作，通常用于分类网络的最后一层，以替代全连接层。计算公式为：

    $$
    y_c = \frac{1}{H \cdot W} \sum_{i=1}^{H} \sum_{j=1}^{W} x_{c,i,j}
    $$

    其中 $x$ 为输入特征图，$H$ 和 $W$ 分别为高度和宽度，$c$ 表示通道索引，$y_c$ 为输出的每个通道特征值。该操作能够将空间信息压缩为通道级别的全局表示，常用于 ResNet、Inception 等网络的分类层。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    gap = nn.AdaptiveAvgPool2d((1,1))
    x = torch.randn(1, 64, 8, 8)
    y = gap(x)
    print(y.shape)  # torch.Size([1, 64, 1, 1])
    ```

4. **全局最大池化（Global Max Pooling）**

    全局最大池化对整个特征图取最大值，用于强调最显著的特征。计算公式为：

    $$
    y_c = \max_{i,j} x_{c,i,j}
    $$

    其中 $x$ 为输入特征图，$c$ 表示通道索引，$i,j$ 遍历整个空间维度，$y_c$ 为输出的每个通道最大值。该操作可将空间信息压缩为通道级别的代表特征，有助于强化关键模式。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    gmp = nn.AdaptiveMaxPool2d((1,1))
    x = torch.randn(1, 64, 8, 8)
    y = gmp(x)
    print(y.shape)  # torch.Size([1, 64, 1, 1])
    ```

## 归一化层

在深度网络中，随着信号在层与层之间传递，每一层的输入分布会不断发生变化，这会使训练变得不稳定、梯度传播困难。归一化层的设计初衷是让中间表示保持数值分布的稳定，从而加速训练、改善梯度流动，并提升网络整体的可优化性。根据归一化作用的维度不同，它有多种形式，其中最常见的是 Batch Normalization 和 Layer Normalization。

1. **Batch Normalization**

    Batch Normalization 是在 CNN 和许多前馈网络中使用最广泛的归一化方式。它对每个通道，在整个 mini-batch 维度上计算均值和方差，使同一通道的数值在不同样本之间保持分布一致。其核心操作是对每个 channel 执行标准化：

    $$
    \hat{x} = \frac{x - \mu_{\text{batch}}}{\sqrt{\sigma_{\text{batch}}^2 + \epsilon}}
    $$

    随后通过可训练参数恢复表达能力：

    $$
    y = \gamma \hat{x} + \beta
    $$

    BN 在大 batch 下表现良好，能有效稳定梯度、加速收敛，并在 CNN 中成为事实标准组件。然而当 batch 较小或输入是序列数据（如 NLP）时，BN 的效果会明显下降，因为小 batch 使统计量不稳定，而序列模型中不同位置之间并不适合共享 batch 统计量。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    import torch
    import torch.nn as nn

    # 用于 CNN 的 2D BatchNorm
    bn = nn.BatchNorm2d(num_features=64)

    x = torch.randn(32, 64, 32, 32)  # batch=32, channels=64, feature map 32x32
    y = bn(x)

    print(y.shape)
    ```

2. **Layer Normalization**

    Layer Normalization 则完全避免依赖 batch，它在每个样本内部进行归一化，对该样本的所有通道（或特征维度）求均值与方差。这意味着每条样本的归一化计算彼此独立，不受 batch 大小影响。因此 LN 非常适合 Transformer、RNN 以及各种序列模型。

    其标准化方式为：

    $$
    \hat{x} = \frac{x - \mu_{\text{layer}}}{\sqrt{\sigma_{\text{layer}}^2 + \epsilon}}
    $$

    同样有可训练的缩放与偏移：

    $$
    y = \gamma \hat{x} + \beta
    $$

    由于 LN 在单个样本内部进行统计，它在 NLP 和注意力模型中具有极高的稳定性，能够让网络在长序列和复杂结构中保持可训练性，也被视为 Transformer 成功的重要因素之一。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    import torch
    import torch.nn as nn

    # 用于 Transformer/MLP 的 LayerNorm
    ln = nn.LayerNorm(normalized_shape=128)

    x = torch.randn(32, 10, 128)  # batch=32, seq_len=10, feature_dim=128
    y = ln(x)

    print(y.shape)
    ```

## 正则化层

正则化层的核心目标是提升模型的泛化能力，避免网络在训练数据上过拟合。随着网络深度和参数规模不断增长，模型往往会记住训练集中的噪声和偶然模式，使测试性能下降。正则化层通过在训练过程中引入随机性、稀疏性或归约机制，让网络学到更加稳健的特征表示。

深度学习中使用最广泛的正则化方式是 **Dropout** ，此外还包括 DropConnect、Stochastic Depth 等更深度化的结构性随机化手段。

1. **Dropout**

    Dropout 的核心思想是在训练时随机 “丢弃” 一部分神经元，使网络不能依赖某些特定特征，从而降低 Co-Adaptation（特征共适应）。在前向传播中，Dropout 会对每个神经元以一定概率 $p$ 将其置零：

    $$
    \tilde{h}_i = h_i \cdot z_i,\qquad z_i \sim \text{Bernoulli}(1-p)
    $$

    为了保持期望一致，训练时会进行缩放（Inverted Dropout）：

    $$
    \tilde{h}_i = \frac{h_i \cdot z_i}{1-p}
    $$

    在推理阶段，则不执行任何随机丢弃操作，使网络表现确定且稳定。

    Dropout 能有效缓解过拟合，因此经常用于全连接网络、MLP block 或 Transformer 的前馈层。对于卷积网络，Dropout 的效果相对弱于 BatchNorm + 数据增强，但在较深的 CNN 中仍然有一定应用价值。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    import torch
    import torch.nn as nn

    # Dropout 概率 p=0.5
    dropout = nn.Dropout(p=0.5)

    x = torch.randn(4, 10)   # 一个 batch 的全连接输入
    y = dropout(x)

    print(y)
    ```

2. **DropConnect**

    与 Dropout 丢弃激活值不同，DropConnect 随机丢弃的是权重。其计算形式为：

    $$
    \tilde{W} = W \cdot M \qquad M_{ij} \sim \text{Bernoulli}(1-p)
    $$

    然后用被随机裁剪后的权重进行前向传播。这是一种更激进的正则化方式，但在实践中使用较少，只在部分模型如一些 RNN 变体中出现。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    import torch
    import torch.nn as nn

    class DropConnectLinear(nn.Linear):
        def __init__(self, in_features, out_features, p=0.5):
            super().__init__(in_features, out_features)
            self.p = p

        def forward(self, x):
            if self.training:
                mask = torch.bernoulli(torch.full_like(self.weight, 1-self.p))
                w = self.weight * mask
            else:
                w = self.weight
            return x @ w.t() + self.bias

    layer = DropConnectLinear(128, 64, p=0.3)
    ```

3. **Stochastic Depth**

    在深层网络中，某些残差块可以在训练时随机跳过，从而形成 “动态深度” 。对于一个残差块：

    $$
    y = x + F(x)
    $$

    Stochastic Depth 会以概率 $p$ 直接跳过该残差分支：

    $$
    y =
    \begin{cases}
    x + F(x), & \text{with prob } 1-p\\
    x, & \text{with prob } p
    \end{cases}
    $$

    这种方法特别适用于深层 ResNet、Vision Transformer，使模型在训练时表现为较浅网络，更易优化，而在推理时保持完整深度。

    **PyTorch 示例**：

    ```py frame="code" title="main.py"
    import torch
    import torch.nn as nn

    class StochasticDepth(nn.Module):
        def __init__(self, p):
            super().__init__()
            self.p = p

        def forward(self, x, residual):
            if self.training and torch.rand(1) < self.p:
                return x
            return x + residual

    # 使用（伪示例）
    sd = StochasticDepth(p=0.2)
    ```

---

# 深层问题探究

1. Softmax 函数是如何设计的？（如何用最大熵原理推出 Softmax 函数？）

    在多分类任务中，我们希望模型输出一组 **概率**：这些概率不仅要非负、总和为 1，还要能够响应输入的 “证据” 差异。最大熵原理提供了一条自然路径：在满足必要约束的前提下，选择 **熵最大的分布** ，从而避免引入额外偏见。

    ### 最大熵建模

    假设模型的前向计算得到一组实数（logits）：
    
    $$
    z = (z_1, \dots, z_K)
    $$
    
    我们希望基于这些分数构造一个概率分布：
    
    $$
    p = (p_1,\dots, p_K) \quad p_k\ge 0,\ \sum_k p_k = 1
    $$

    最大熵原理告诉我们：

    > 在所有满足约束的概率分布中，应选择 **熵最大** 的那个。

    熵的定义为：

    $$
    H(p)= -\sum_{k=1}^K p_k \log p_k
    $$

    为了让概率分布能够体现 logits 提供的信息，需要加入一个 **期望约束**（常称 “能量约束” ）：

    $$
    \sum_{k=1}^K p_k z_k = \mu
    $$

    其中 $\mu$ 不必显式求出，它由拉格朗日乘子自然吸收。

    因此最大化问题写作：

    $$
    \max_{p_k\ge 0} -\sum_{k} p_k \log p_k
    $$

    $$
    \text{s.t. } \sum_k p_k = 1 \quad \sum_k p_k z_k = \mu
    $$

    ### 拉格朗日乘子求解

    构造拉格朗日函数：

    $$
    \mathcal{L}(p, \alpha, \beta)
    = -\sum_k p_k \log p_k + \alpha\left(\sum_k p_k -1\right) + \beta\left(\sum_k p_k z_k -\mu\right)
    $$

    对 $p_k$ 求偏导并令其为零：

    $$
    \frac{\partial \mathcal{L}}{\partial p_k}
    = -(\log p_k + 1) + \alpha + \beta z_k = 0
    $$

    $$
    \log p_k = \alpha - 1 + \beta z_k
    $$

    指数化后可以得到：

    $$
    p_k = e^{\alpha - 1} e^{\beta z_k} = C e^{\beta z_k}
    $$

    利用归一化条件：

    $$
    \sum_{k=1}^K p_k = 1
    \quad\Rightarrow\quad
    C = \frac{1}{\sum_j e^{\beta z_j}}
    $$

    最终得到 Softmax 的一般形式：

    $$
    \boxed{
    p_k = \frac{e^{\beta z_k}}{\sum_j e^{\beta z_j}}
    }
    $$

    其中 $\beta = 1/T$ 是温度系数，用于控制分布的尖锐程度。最常用的设定是 $\beta=1$ ，得到标准 Softmax：

    $$
    \boxed{
    p_k = \frac{e^{z_k}}{\sum_j e^{z_j}}
    }
    $$

    > 关于更详细的讲解可以参考以下视频

    <iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=889408481&bvid=BV1cP4y1t7cP&cid=379457443&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>