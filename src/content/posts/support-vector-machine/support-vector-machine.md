---
title: 【机器学习基本模型】第五节：支持向量机
published: 2025-10-25
description: 介绍机器学习常见的算法模型
tags: [Machine Learning, Course]
category: ML Model
draft: false
---

> 写在前面：我们的教程终于来到了机器学习的第一个大难点 ———— 支持向量机。在深度学习盛行的今天，支持向量机是为数不多还能继续使用的传统机器学习算法之一，就让我们来看看大名鼎鼎的支持向量机到底是什么吧！（注意本篇的配图都在文字的下方）

# 支持向量机基本原理

> 以下推导部分参考自该视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=936042727&bvid=BV16T4y1y7qj&cid=494397114&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

我们首先来思考这么一个问题，如上图所示，如果要求你画一条直线，使其能够将图中的两类点分开，并且在加入新的点后也尽可能实现这个目的（具有预测能力），你会如何画这个条直线呢？直觉上来讲，这条直线靠近任何一类点都不太可行。因此我们认为，这条直线到任何一个点都足够远时，直线的分类效果最好。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机2.jpg)

为了实现我们上述的初步猜想，我们要先引入一个概念： **间隔** （Margin）。间隔的作用是将两类数据所处的空间分隔开来，并且间隔越大，两类数据的差异也就越大。因此，要想区分两类数据，我们就得找到两类数据的最大间隔，然后我们再以间隔的正中间作为决策边界，就可以实现我们的猜想。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机3.jpg)

我们将已经找到的超平面上下移动 C 个单位，使其恰好经过某些数据点，我们称这两条直线为间隔上下边界。由于间隔上下边界必然会经过几个数据点，而这几个数据点也是起到了限制间隔上下边界的作用，因此我们称这几个点为 **支持向量** （Support Vector）。这便是 **支持向量机** （Support Vector Machine，简称 SVM）名称的由来。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机4.jpg)

## 归一化

对于直线方程来说，如果我们对其两边同时除以一个数，我们就可以得到一个新的方程。因此空间上的 **一条直线** 拥有 **无数** 个直线方程，这对我们的计算会产生影响。因此我们规定：决策上下边界的右值必须为 $\pm 1$ 。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机5.jpg)

这样我们就得到了三个平面：正超平面（Positive Hyperplane）、负超平面（Negative Hyperplane）和决策超平面（Decision Hyperplane）。

## 软间隔

我们再进一步思考这样一个问题：如果两类数据的间隔中出现了一个异常点，那么我们计算所得的的间隔就会缩小，但我们是否要为了这个异常点而牺牲我们的间隔呢？

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机6.jpg)

答案是否定的。但我们要如何判断什么样的点是异常点呢？或者说，我们可以让算法自己判断是否要忽略某个数据点吗？对此，我们引入了 **损失因子** （Penalty Factor）这个概念。你可以将原本的间隔视为经营的 **收入** ，而将损失看作经营的 **成本** ，那么我们最初的问题则可以转化为最大化 **利润** 。此时的间隔我们称之为 **软间隔** （Soft Margin）。

## 数学建模

基本思想已经讲解清楚了，接下来我们就将我们的猜想转换为数学模型，也就是建模（由于篇幅的限制，我们将重点介绍硬间隔支持向量机，软间隔向量机将放到代码实现中的[内容拓展](#内容拓展)）。

> 以下推导部分参考自该视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=766832077&bvid=BV13r4y1z7AG&cid=516465204&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

首先我们分别在正负超平面上任意选取一个支持向量点 $x_m$ 和 $x_n$ 。由于它们分别在正负超平面上，所以它们一定满足下列等式：

$$
w_1 x_{1m} + w_2 x_{2m} + b = 1
$$

$$
w_1 x_{1n} + w_2 x_{2n} + b = -1
$$

我们将上述的两个等式相减后又可以得到下面这个式子：

$$
w_1 (x_{1m} - x_{1n}) + w_2 (x_{2m} - x_{2n}) = 2
$$

上面这个式子又相当于下面这个式子：

$$
\vec{w} \cdot (\vec{x}_{m} - \vec{x}_{n}) = 2
$$

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机7.jpg)

我们再从决策超平面上随机选取两个点 $x_o$ 和 $x_p$ ，同理我们可以得到下面这个式子：

$$
\vec{w} \cdot (\vec{x}_{o} - \vec{x}_{p}) = 0
$$

由此我们可以得知： $\vec{w}$ 与决策超平面垂直。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机8.jpg)

回到上面的推导过程，我们将上面的点积式子用模长表示：

$$
\| \vec {x}_m - \vec {x}_n \| * \cos \theta * \| \vec {w} \| = 2
$$

由于 $\vec{w}$ 与决策超平面垂直，从几何含义可以得到：

$$
\| \vec {x}_m - \vec {x}_n \| * \cos \theta = L
$$

其中 $L$ 为间隔宽度。

结合上面的两个式子，我们便可以得到间隔宽度 $L$ 的表达式：

$$
L = \frac{2}{\| \vec{w} \|}
$$

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机9.jpg)

我们再来看看约束条件。所有的绿点都属于正类，对应的分类值 $y_i = 1$ ，又因为它们处于正超平面的 上方，因此满足 $\vec{w} \cdot \vec{x}_{i} + b \geq 1$ ；同理，对于所有的黄点来说，它们对应的分类值 $y_i = -1$ ，满足 $\vec{w} \cdot \vec{x}_{i} + b \leq -1$ 。

综上可知，这些数据点均满足下面这个不等式：

$$
y_i * (\vec{w} \cdot \vec{x}_{i} + b) \geq 1
$$

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机10.jpg)

从上面的式子我们可以知道，最大化间隔其实就是最小化 $\vec{w}$ 的模长，形式地来讲：

$$
\min \left\| \vec{w} \right\|_2
$$

$$
\text{s.t.} \quad y_i * (\vec{w} \cdot \vec{x}_{i} + b) \geq 1 \quad \forall i = 1,2,\dots,N
$$

到此，我们成功地将我们的猜想转换成一个带约束的最优化问题。

## 深层理解

看到上面的最优化问题后，许多人的第一反应应该是使用 **拉格朗日乘数法** 来解决，这在一般情况下的确如此。但对于支持向量机来说，为了后续求解的效率，我们往往会将上述最优化问题转化为它的 **拉格朗日对偶问题** 来求解。但我们暂且按下不表，让我们顺着拉格朗日乘数法的思路往下推导，顺便深度了解一下支持向量的含义。

为了后续推导的方便，我们可以将上述的最优化问题做个小变形：

$$
\min f(w) = \frac{\|\vec{w}\|_2^2}{2}
$$

$$
\text{s.t.} \quad g_i(w, b) = y_i * (\vec{w} \cdot \vec{x}_{i} + b) - 1 \geq 0 \quad \forall i = 1,2,\dots,N
$$

显然转换之后不影响最小值的求解。

对于约束条件是不等式的情况，我们需要引入一个非负变量来将不等式转化为等式（我们这里之所以要将不等式转化为等式进行处理是为了从零开始推导不等式约束的拉格朗日系数必须非负这个条件，后续使用拉格朗日乘数法时不再使用，可以直接将不等式写入拉格朗日函数）：

$$
\text{s.t.} \quad g_i(w, b) = y_i * (\vec{w} \cdot \vec{x}_{i} + b) - 1 = p_i^2 \quad \forall i = 1,2,\dots,N
$$

由此我们可以得到下面这个拉格朗日方程式：

$$
L(w, b, \lambda_i, p_i) = \frac{\| \vec{w} \|^2}{2} - \sum_{i=1}^{N} \lambda_i \Big[ y_i (\vec{w} \cdot \vec{x_i} + b) - 1 - p_i^2 \Big]
$$

将拉格朗日函数对 $w$ 、 $b$ 、 $\lambda_i$ 和 $p_i$ 分别求导可得：

$$
\frac{\partial L}{\partial \vec{w}} = \vec{w} - \sum_{i=1}^{N} \lambda_i y_i \vec{x_i} = 0
$$

$$
\frac{\partial L}{\partial b} = - \sum_{i=1}^{N} \lambda_i y_i = 0
$$

$$
\frac{\partial L}{\partial p_i} = 2 \lambda_i p_i = 0
$$

$$
\frac{\partial L}{\partial \lambda_i} = - \bigl( y_i (\vec{w} \cdot \vec{x_i} + b) - 1 - p_i^2 \bigr) = 0
$$

联立下面两个等式可以得到：

$$
\lambda_i(y_i (\vec{w} \cdot \vec{x}_i + b) - 1) = 0
$$

根据条件 $y_i * (\vec{w} \cdot \vec{x}_i + b) - 1 \geq 0$ ，所以我们可以知道：

$$
\begin{cases}
y_i (\vec{w} \cdot \vec{x_i} + b) - 1 > 0, & \lambda_i = 0 \\[6pt]
y_i (\vec{w} \cdot \vec{x_i} + b) - 1 = 0, & \lambda_i \ne 0
\end{cases}
$$

如果我们将 $\lambda_i$ 看成惩罚因子，那么上面的两种情况可以解释成：当数据点不在正负超平面上时，该数据点不对整体产生贡献；当数据点在正负超平面时，该数据点会对整体产生贡献。这便是支持向量的深层含义：只有 **落在正负超平面上** 的数据点才会对拉格朗日函数 **造成约束** 。这也符合我们在几何空间上的直观理解。

并且我们还能得出拉格朗日的约束系数必须满足 $\lambda_i \geq 0$ ，因为当数据点不满足约束条件时必然有：

$$
y_i * (\vec{w} \cdot \vec{x}_i + b) - 1 < 0
$$

如果再加上 $\lambda_i < 0$ 则必然会有拉格朗日约束项小于零，这相当于变相鼓励支持向量机去违反约束条件，显然这种情况是不被允许的。

![支持向量机图像](src\content\posts\support-vector-machine\支持向量机11.jpg)

# 拉格朗日对偶问题

接下来的内容就是本篇博客的重点内容，也是支持向量机的核心难点内容。让我们一起来看一下什么是拉格朗日对偶问题。

> 以下推导部分参考下面两个视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=890417318&bvid=BV1HP4y1Y79e&cid=503516018&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=766832077&bvid=BV13r4y1z7AG&cid=516465204&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 拉格朗日乘数法

要想理解什么是拉格朗日对偶问题，那就不得不先了解什么是拉格朗日乘数法。不知道读者在第一次接触拉格朗日乘数法的时候是否会感到好奇，为什么这样一顿操作之后就能求解出带约束下函数的极值呢？不如用优美的几何图像与严谨的数学语言来理解一遍吧。

让我们来看一下这样一个简单的带约束优化问题：

$$
\text{求 } f(x,y) \text{ 的最小值, 并且 } y \leq g(x)
$$

$$
L(x,y) = f(x,y) + \lambda (y - g(x))
$$

$$
\Downarrow
$$

$$
\nabla L(x,y) = 0
$$

$$
\Downarrow
$$

$$
\begin{cases}
\dfrac{\partial f(x,y)}{\partial x} + \lambda \dfrac{\partial (y - g(x))}{\partial x} = 0 \\
\dfrac{\partial f(x,y)}{\partial y} + \lambda \dfrac{\partial (y - g(x))}{\partial y} = 0
\end{cases}
$$

如图所示（图中的数学符号不太契合我们现在探讨的问题，因此只需要关注图像即可），圆环套圆环表示类似于旋转抛物面的 $f(x,y)$ 的函数图像，直线则表示 $z = y - g(x) \leq 0$ 的边界线（可以想象是一个柱面投影在 $xOy$ 平面的图像）。

观察图像易得，当圆环与直线相切时，这个切点便是带约束下函数的极值点。并且此时两个函数的梯度 **恰好共线** ，如果再调节 $\lambda$ 的值则有可能使其 **正负相互抵消** ，因此将拉格朗日函数写成上面的形式（将原函数与约束线性组合）后再求导便可以得到带约束条件下函数的极值点。

![拉格朗日对偶问题](src\content\posts\support-vector-machine\拉格朗日对偶问题1.jpg)

我们再来看看在多个约束下的几何图像是什么样的。如图所示，我们再添加一个约束，此时两个约束的相交点为最优解，两个约束的梯度向量的线性组合可能会与函数的梯度向量共线且相等，对拉格朗日函数求导仍然可以得到带约束条件下函数的极值点。

![拉格朗日对偶问题](src\content\posts\support-vector-machine\拉格朗日对偶问题2.jpg)

如果我们再加入一个约束，如图所示，这个新加入的约束并不会改变先前所有约束条件的交集的形状，因此它的加入并不会对答案造成影响。

![拉格朗日对偶问题](src\content\posts\support-vector-machine\拉格朗日对偶问题3.jpg)

这其实是 **KKT 条件** （关于什么是 KKT 条件我会在下文介绍）中 **互补松弛条件** （Complementary Slackness Condition）的几何解释。如果一个条件对答案有影响，那么它对应的 $\lambda_i$ 必然大于零，我们则称其为 **紧致条件** ；如果一个条件对答案没有影响，那么它对应的 $\lambda_i$ 必然等于零，我们则称其为 **松弛条件** （因为 $\lambda < 0$ 会导致约束条件的梯度向量与函数的梯度向量同向而无法相互抵消，因此不可能出现）。由此我们又可以从 **互补松弛的角度** 再次了解什么是支持向量：支持向量是 **支持向量机最优化问题中的紧致条件** 。

## 凸问题与凸优化

拉格朗日乘数法非常强大，但它的缺点也非常明显：只能求解极值点/鞍点。拉格朗日乘数法并不能保证求解出的结果一定是最值点（但一定包含最值点），但如果我们要求解的问题是一个 **凸问题** （Convex Problem），那么这个问题中的极值点就是最值点（凸问题的性质）。

而我们的拉格朗日对偶问题有个非常美妙的结论：原问题的拉格朗日对偶问题 **一定是凸问题** 。

接下来我们就仔细地讲解一下拉格朗日对偶问题的推导过程，首先需要将拉格朗日问题稍微改写一下：

$$
\begin{align*}
\min \quad & f_0(x), \quad x \in \mathbb{R}^n \\
\text{s.t.} \quad & f_i(x) \leq 0, \quad i = 1, 2, \dots, m \\
& h_i(x) = 0, \quad i = 1, 2, \dots, q
\end{align*}
$$

$$
\Downarrow
$$

$$
L(x, \lambda, \nu) = f_0(x) + \sum_{i=1}^m \lambda_i f_i(x) + \sum_{i=1}^q \nu_i h_i(x) \\
\text{原问题：} \min_x \max_{\lambda, \nu} L(x, \lambda, \nu) \\
\quad \text{s.t.} \quad \lambda \geq 0
$$

当 $x$ 不在可行域内时有： $f_i(x) > 0$ 和 $h_i(x) ≠ 0$ 。若想最大化 $L(x, \lambda, \nu)$ ，我们可以让 $\lambda_i$ 取到正无穷，让 $\nu_i h_i(x)$ 取到正无穷：

$$
\max_{\lambda, \nu} L(x, \lambda, \nu) = f_0(x) + \infty + \infty = \infty
$$

当 $x$ 在可行域内时有： $f_i(x) \leq 0$ 和 $h_i(x) = 0$ 。若想最大化 $L(x, \lambda, \nu)$ ，我们可以让 $\lambda_i$ 取到 0 （因为 $h_i(x) = 0$ ，所以 $\nu_i$ 取任意值均可）：

$$
\max_{\lambda, \nu} L(x, \lambda, \nu) = f_0(x) + 0 + 0 = f_0(x)
$$

然后在此基础上再取 $min$ 可以得到：

$$
\min_{x} \max_{\lambda, \nu} L(x, \lambda, \nu) = \min_{x} \{ f_0(x), \infty \} = \min_{x} f_0(x)
$$

因此拉格朗日问题的两种形式是等价的。

接下来我们看看拉格朗日对偶问题的数学形式：

$$
\begin{align*}
\text{对偶函数：} & \quad g(\lambda, \nu) = \min_{x} L(x, \lambda, \nu) \\
\text{对偶问题：} & \quad \max_{\lambda, \nu} g(\lambda, \nu) = \max_{\lambda, \nu} \min_{x} L(x, \lambda, \nu) \\
& \quad \text{s.t. } \lambda \geq 0
\end{align*}
$$

很明显，原问题就是先求 $max$ 再求 $min$ 的过程，对偶问题就是先求 $min$ 再求 $max$ 的过程。

我们来看看凸问题的定义：当一个问题的 **约束条件是凸集** 且 **问题函数为凸函数** 时，该问题被称为凸问题。观察对偶函数 $L(x, \lambda, \nu)$ ，如果先对参数 $x$ 做最小值优化，则在做最大值优化的时候， $f_0(x^*)$ 、 $f_i(x^*)$ 和 $h_i(x^*)$ 都是常数，也就是说：此时的对偶函数 $g(\lambda, \nu)$ 是一个 **线性函数** ，而线性函数是一个 **凸函数** 。再加上对偶问题的约束条件是 $\lambda \geq 0$ ，这是一个 **半空间** ，而半空间是一个 **凸集** 。综上所述，对偶问题是一个 **凸问题** 。

$$
g(\lambda, \nu) = f_0(x^*) + \sum_{i=1}^m \lambda_i f_i(x^*) + \sum_{i=1}^q \nu_i h_i(x^*)
$$

## 弱对偶与强对偶

到此为止，我们已经知道了什么是拉格朗日对偶问题，也弄懂为什么拉格朗日对偶问题一定是一个凸问题。但我们要想用拉格朗日对偶问题来解决原问题，就必须证明两个问题得到的解之间是相关的，否则对偶问题有再多优美的性质，也无法帮我们去解决原问题。所以接下来，就让我们来看一下拉格朗日问题与其对偶问题之间的关系吧。

首先我们可以轻松地证明出：拉格朗日问题的解大于等于其对偶问题的解。下面是证明过程：

$$
\max_{\lambda, \nu} L(x, \lambda, \nu) \ge L(x, \lambda, \nu) \ge \min_{x} L(x, \lambda, \nu)
$$

$$
A(x) = \max_{\lambda, \nu} L(x, \lambda, \nu) \ge L(x, \lambda, \nu) \ge \min_{x} L(x, \lambda, \nu) = I(\lambda, \nu)
$$

$$
A(x) \ge I(\lambda, \nu) \quad (\forall\, x, \lambda, \nu)
$$

$$
A(x) \ge \min_{x} A(x) \ge \max_{\lambda, \nu} I(\lambda, \nu) \ge I(\lambda, \nu)
$$

$$
P^{*} = \min_{x} A(x) \ge \max_{\lambda, \nu} I(\lambda, \nu) = D^{*}
$$

而上述这个性质我们称之为 **弱对偶性** （Weak Duality Theorem）。也就是说：拉格朗日对偶问题与原问题 **一定满足弱对偶性** 。那么拉格朗日对偶问题在什么条件下与原问题之间满足 **强对偶性** （Strong Duality Theorem）呢？当原问题是 **凸问题** 且满足一定的 **正则条件** （Slater 条件就是其中之一）时，原问题与其对偶问题满足强对偶性（具体证明不再给出，需要的读者可以观看下面这个 PDF）。

[对偶理论（Duality）](https://bolei-zhang.github.io/course/06be4d689c17514cfe26a9a14ddff12d3911cd62/slides/lec5_duality_1-2.pdf)

但另一个问题也随之而来：既然原问题已经是凸问题，为什么仍要引出对偶问题这个概念呢？原因就是原问题虽然也是凸问题，但原问题本身往往非常复杂，求解起来十分困难，而对偶问题将繁杂的约束条件融入到拉格朗日函数中，求解起来十分简单，因此我们会更倾向于将原问题转化成它的对偶问题来进行求解（即便原问题不是凸问题我们也会尝试将其转化成对偶问题来求解）。

## KKT 条件

原理部分讲到这里其实已经足够了，但在[先前讲解拉格朗日乘数法](#拉格朗日乘数法)时所提到的 KKT 条件并不完整，因此在这里给出详细的 KKT 条件：

$$
\begin{cases}
\nabla f(x^*) + \sum_{i=1}^m \lambda_i \nabla g_i(x^*) + \sum_{j=1}^p \nu_j \nabla h_j(x^*) = 0 & \text{(Stationarity)} \\[1.2em]
g_i(x^*) \le 0, \quad i = 1, \dots, m & \text{(Primal feasibility)} \\[0.8em]
h_j(x^*) = 0, \quad j = 1, \dots, p & \text{(Equality constraints)} \\[0.8em]
\lambda_i \ge 0, \quad i = 1, \dots m, & \text{(Dual feasibility)} \\[0.8em]
\lambda_i g_i(x^*) = 0, \quad i = 1, \dots, m & \text{(Complementary slackness)}
\end{cases}
$$

KKT 条件的作用就是能让我们快速判断一个问题是否是强对偶问题：在绝大多数条件下（少数情况几乎都是人为构造，实际应用相当罕见），只要满足 KKT 条件的问题就是强队偶问题。

# 代码实现

根据拉格朗日对偶问题的原理，我们来推导一下支持向量机问题的对偶问题。

```py frame="code" title="main.py"
import numpy as np

# 假设 X: (n_samples, n_features), y: (n_samples,) 且值为 +1/-1
def linear_svm_train(X, y, lr=0.001, epochs=1000):
    n_samples, n_features = X.shape
    alpha = np.zeros(n_samples)

    # 梯度上升求解对偶问题
    for _ in range(epochs):
        for i in range(n_samples):
            # 对 α_i 的梯度
            grad = 1 - np.sum(alpha * y * y[i] * np.dot(X, X[i]))
            alpha[i] += lr * grad
            alpha[i] = max(alpha[i], 0)  # 保证 α_i >= 0

    # 计算 w
    w = np.sum((alpha * y)[:, None] * X, axis=0)

    # 找一个支持向量求 b
    sv_idx = np.where(alpha > 1e-5)[0][0]
    b = y[sv_idx] - np.dot(w, X[sv_idx])

    return w, b

def linear_svm_predict(X, w, b):
    # 加 sign 是为了做判别分析
    return np.sign(np.dot(X, w) + b)
```

引入拉格朗日乘子 $\alpha_i$ 并写出拉格朗日函数：

$$
L(w, b, \alpha) = \frac{\| \vec{w} \|^2}{2} - \sum_{i=1}^{N} \alpha_i \Big[ y_i (\vec{w} \cdot \vec{x_i} + b) - 1 \Big]
$$

将其对 $\vec{w}$ 和 $b$ 求偏导：

$$
\frac{\partial L}{\partial \vec{w}} = \vec{w} - \sum_{i=1}^{s} \alpha_i y_i \vec{x_i}
$$

$$
\frac{\partial L}{\partial b} = - \sum_{i=1}^{s} \alpha_i y_i
$$

令偏导为零并带入拉格朗日函数可得到支持向量机问题的对偶问题：

$$
\begin{align*}
\max_{\alpha} \quad & \sum_{i=1}^{n} \alpha_i - \frac{1}{2} \sum_{i=1}^{n} \sum_{j=1}^{n} \alpha_i \alpha_j y_i y_j \vec{x_i} \cdot \vec{x_j} \\
\text{s.t.} \quad & \alpha_i \ge 0, \quad \sum_{i=1}^{n} \alpha_i y_i = 0
\end{align*}
$$

接下来我们只需要用梯度上升（这里是求 $max$）的方式求解出参数 $\alpha$ 即可。

## 内容拓展

支持向量机其实还有很多可以优化的点。

- 首先就是上面的梯度上升算法：对于支持向量机来说，直接使用梯度上升算法是不太行的，由于对偶问题有 **等式约束** ，直接梯度很难保持约束。不仅如此，计算梯度还会遇到开销大、收敛慢等问题。因此我们往往会使用 **SMO 算法** 来替代梯度上升算法（SMO 算法的具体内容可以看下面的博客）。

[详细推导序列最小优化SMO算法](https://zhuanlan.zhihu.com/p/560529392)

- 然后就是对于线性不可分的数据：我们在前面这么长的推导过程其实都有一个前提假设 ———— 数据是线性可分的。但是在大多数情况下，数据往往是线性不可分的，那我们就得要引出我们的 **核技巧** （Kernel Trick）了。核技巧的原理非常简单，就是想办法将数据升维后，再进行支持向量机的构建，因为 **维度越高数据越有可能线性可分** （具体讲解可以看下面这个视频，限于篇幅原因不过多讲解）。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=637192057&bvid=BV1Nb4y1s7pE&cid=547472956&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

- 最后就是软间隔问题了：在[上文](#软间隔)我们讲到过什么是软间隔，但我们没有过多解释软间隔的数学原理，如果读者感兴趣可以观看下面的视频。

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=682759064&bvid=BV1AS4y1K7Jf&cid=565289579&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 深层问题思考

1. 为什么说支持向量机是一个自带 L2 正则化的机器学习算法？（什么是合叶损失函数？）

> 以下推导部分参考自该视频

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=549434532&bvid=BV1zq4y1g74J&cid=449456397&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

首先给出软间隔下的支持向量机最优化问题：

$$
\begin{align*}
\min_{W,b,\xi} \quad & \frac{1}{2} W^T W + C \sum_{i=1}^N \xi_i \\
\text{s.t.} \quad & 1 - Y^{(i)} (W^T X^{(i)} + b) \leq \xi_i, \quad i = 1, 2, \dots, N \\
& \xi_i \geq 0, \quad i = 1, 2, \dots, N
\end{align*}
$$

然后转换成如下形式：

$$
\begin{align*}
\min_{W,b,\xi} \quad & \frac{1}{2} W^T W + C \cdot \sum_{i=1}^N \xi_i \\
\text{s.t.} \quad & 
\begin{aligned}
\xi_i &\geq \max\left\{0, 1 - Y^{(i)}(W^T \cdot X^{(i)} + b)\right\}, & i = 1, 2, \dots, N \\
&= \left[1 - Y^{(i)}(W^T \cdot X^{(i)} + b)\right]_+, & i = 1, 2, \dots, N
\end{aligned}
\end{align*}
$$

最后将问题转化为拉格朗日函数可得：

$$
\min \frac{1}{2} W^T W + C \sum_{i=1}^{N} \left[ 1 - Y^{(i)} (W^T X^{(i)} + b) \right]_+
$$

$$
\Downarrow
$$

$$
\min \underbrace{\sum_{i=1}^{N} \left[ 1 - Y^{(i)} (W^T X^{(i)} + b) \right]_+}_{\textcolor{green}{\text{经验损失项}}} 
+ 
\underbrace{\lambda \frac{1}{2} W^T W}_{\textcolor{green}{\text{正则化项}}}
$$

上述形式中 “经验损失项” 就是所谓的 “合叶损失函数” ，“正则化项” 就是 “L2 正则化” 。

# 参考文献

1. [支持向量机（SVM）详解](https://blog.csdn.net/fyc1314/article/details/153789016)

2. [【ScikitLearn】支持向量机](https://scikit-learn.cn/stable/modules/svm.html)

3. [什么是支持向量机](https://blog.csdn.net/v20000727/article/details/135137095)

4. [支持向量机（SVM）——原理篇](https://www.zhihu.com/tardis/zm/art/31886934)

5. [【维基百科】支持向量机](https://zh.wikipedia.org/wiki/支持向量机)

6. [看了这篇文章你还不懂SVM你就来打我](https://zhuanlan.zhihu.com/p/49331510)

7. [支持向量机的工作原理](https://ww2.mathworks.cn/discovery/support-vector-machine.html)

8. [【图解数学】支持向量机](https://note.wcoder.com/MachineLearning/图解数学/files/支持向量机.pdf)