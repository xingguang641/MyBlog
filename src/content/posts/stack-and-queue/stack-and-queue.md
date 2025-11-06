---
title: 【基础数据结构介绍】第一节：栈与队列
published: 2025-11-04
description: 介绍常见的数据结构
tags: [Data Structure, Course]
category: Data Structure
draft: false
---

# 栈的基本结构

栈（stack）是一种特殊的线性表存储结构，其一端可以进行插入和弹出的操作，而另一端是封死的。栈的修改与访问是按照后进先出的原则进行的，因此栈通常被称为是 **后进先出** （last in first out）表，简称 LIFO 表。

## 顺序栈基本原理

顺序栈是用数组来实现栈的存储结构，一般会定义一个栈顶 top，初始情况下 top 值为 -1，表示栈为空，此时栈中无任何元素。每当有元素入栈 top 就 +1；有元素出栈 top 就 -1 。

### 顺序栈入栈操作

> 初始情况下的栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈1.png)

> 元素 1 入栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈2.png)

> 元素 2 入栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈3.png)

> 元素 3 入栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈4.png)

下面给出顺序栈的入栈操作的代码。

```cpp showLineNumbers
void pop(SqStack *s, Elemtype *x){
    if(s->top == -1) return; //栈空
    *x = s->data[s->top--];
}
```

### 顺序栈出栈操作

> 元素 3 出栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈5.png)

> 元素 2 出栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈6.png)

> 元素 1 出栈

![顺序栈图像](src\content\posts\stack-and-queue\顺序栈7.png)

下面给出顺序栈的出栈操作的代码。

```cpp showLineNumbers
void push(SqStack *s, Elemtype x){
    if(s->top == MAXSIZE - 1) return; //栈满
    s->data[++s->top] = x;
}
```

## 顺序栈代码讲解

下面是顺序栈的完整代码。具体原理较为简单，直接对照上方的基本原理介绍即可。

```cpp frame="code" title="main.cpp"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAXSIZE 1000

typedef int Elemtype;
typedef struct{

    Elemtype data[MAXSIZE];
    int top; //栈顶指针

}SqStack;

//初始化栈
void Init_SqStack(SqStack *s){
    s->top = -1;
}

//判断栈是否为空
bool IsEmpty(SqStack *s){
    return s->top == -1;
}

//元素入栈
void push(SqStack *s, Elemtype x){
    if(s->top == MAXSIZE - 1) return;
    s->data[++s->top] = x;
}

//元素出栈
void pop(SqStack *s, Elemtype *x){
    if(s->top == -1) return;
    *x = s->data[s->top--];
}

//取栈顶元素
Elemtype top(SqStack *s){
    if(IsEmpty(s)){
	printf("栈为空\n");
	return -1;
    }
    return s->data[s->top];
}

int main(){
    SqStack mystack;
    Init_SqStack(&mystack);

    for(int i = 1; i <= 5; i++)
	push(&mystack, i);
    printf("当前栈顶元素为: %d\n", top(&mystack));

    int e;
    pop(&mystack, &e);
    printf("出栈元素为: %d\n", e);
    printf("当前栈顶元素为: %d\n", top(&mystack));

    printf("全部元素出栈：\n");
    while(!IsEmpty(&mystack)){
    	printf("%d ", top(&mystack));
    	pop(&mystack, &e);
    }
}
```

## 链栈基本原理

链栈是用链式存储结构实现的，在实现过程中，需要定义一个 top 指针保持指向当前栈顶。操作过程和链表相似。

### 链栈入栈操作

> 初始情况下的链栈

![链栈图像](src\content\posts\stack-and-queue\链栈1.png)

> 元素 1 入栈

![链栈图像](src\content\posts\stack-and-queue\链栈2.png)

> 元素 2 入栈

![链栈图像](src\content\posts\stack-and-queue\链栈3.png)

> 元素 3 入栈

![链栈图像](src\content\posts\stack-and-queue\链栈4.png)

下面给出链栈的入栈操作的代码。

```cpp showLineNumbers
void LinkStack_push(LinkStack *S, ElemType e){
    LinkStacknode *node;            
    node = (LinkStacknode *) malloc(sizeof(LinkStack));
    node->data = e;            
    node->next = S->top; //新节点的next指向此时的top
    S->top = node; //top指针指向新的节点

    S->length++;
}
```

### 链栈出栈操作

> 元素 3 出栈

![链栈图像](src\content\posts\stack-and-queue\链栈5.png)

> 元素 2 出栈

![链栈图像](src\content\posts\stack-and-queue\链栈6.png)

> 元素 1 出栈

![链栈图像](src\content\posts\stack-and-queue\链栈7.png)

下面给出链栈的出栈操作的代码。

```cpp showLineNumbers
void LinkStack_pop(LinkStack *S, ElemType *e){
    if(IsEmpty(S)) //栈空
        return;                  
    LinkStacknode *del = S->top; 
    *e = del->data;              
    S->top = del->next; //top跳过出栈节点，指向出栈节点的下一节点

    S->length--;
    free(del); //释放内存
}
```

## 链栈代码讲解

下面是链栈的完整代码。具体原理较为简单，直接对照上方的基本原理介绍即可。

```cpp frame="code" title="main.cpp"
#include <stdio.h>
#include <stdlib.h>

//定义数据类型
typedef int ElemType;

//链栈的节点结构
typedef struct LinkStacknode
{

    ElemType data; //存数据
    struct LinkStacknode *next; //存下个节点的地址

} LinkStacknode;

//链栈的整体结构  
typedef struct {

    LinkStacknode *top;
    int length;
    
} LinkStack;


//初始化链栈
void Create_LinkStack(LinkStack *S){
    S->top = NULL;
    S->length = 0;
}

//判断栈为空
bool IsEmpty(LinkStack *S){
    return S->length == 0;
}

//入栈
void LinkStack_push(LinkStack *S, ElemType e){
    LinkStacknode *node;            
    node = (LinkStacknode *) malloc(sizeof(LinkStack));
    node->data = e;            
    node->next = S->top; //新节点的next指向此时的top
    S->top = node; //top指针指向新的节点

    S->length++;
}

//出栈
void LinkStack_pop(LinkStack *S, ElemType *e){
    if(IsEmpty(S)) //栈空
        return;                  
    LinkStacknode *del = S->top; 
    *e = del->data;              
    S->top = del->next; //top跳过出栈节点，指向出栈节点的下一节点

    S->length--;
    free(del); //释放内存
}

//取栈顶
ElemType LinkStack_getTop(LinkStack *S){
    if(IsEmpty(S)){
        printf("栈为空\n");
        return -1;
    }
    return S->top->data;
}

int main(){
    LinkStack S;
    Create_LinkStack(&S);

    ElemType e;
    ElemType a[5] = {3,6,7,9,10};
    for(int i = 0; i < 5; i++)
        LinkStack_push(&S, a[i]);

    printf("栈顶元素：%d\n", LinkStack_getTop(&S));

    LinkStack_pop(&S, &e);
    printf("出栈元素：%d\n", e);   

    printf("全部元素出栈：\n");
    while(!IsEmpty(&S)){
        printf("%d ", LinkStack_getTop(&S));
        LinkStack_pop(&S, &e);
    }
    return 0;
}
```

## C++ STL 中的栈

C++ 中的 STL 也提供了一个容器 `std::stack` ，使用前需要引入 `<stack>` 头文件。

### STL 定义

```cpp title="STL 中对 stack 的定义"
// clang-format off
template<
    class T,
    class Container = std::deque<T>
> class stack;
```

> `T` 为 stack 中要存储的数据类型。
> 
> `Container` 为用于存储元素的底层容器类型。这个容器必须提供通常语义的下列函数：
> 
>    - `back()`
>    - `push_back()`
>    - `pop_back()`
> 
> STL 容器 `std::vector` 、 `std::deque` 和 `std::list` 满足这些要求。如果不指定，则默认使用 `std::deque` 作为底层容器。

### 基本操作

STL 中的 stack 容器提供了一众成员函数以供调用，其中较为常用的有：

1. 访问操作
    - `st.top()` 返回栈顶

2. 修改操作
    - `st.push()` 插入传入的参数到栈顶
    - `st.pop()` 弹出栈顶

3. 容量操作
    - `st.empty()` 返回是否为空
    - `st.size()` 返回元素数量

此外， `std::stack` 还提供了一些运算符。较为常用的是使用赋值运算符 = 为 stack 赋值，示例：

```cpp showLineNumbers
// 新建两个栈 st1 和 st2
std::stack<int> st1, st2;

// 为 st1 装入 1
st1.push(1);

// 将 st1 赋值给 st2
st2 = st1;

// 输出 st2 的栈顶元素
cout << st2.top() << endl;
// 输出: 1
```

# 栈的拓展应用



# 栈相关视频教程

> 栈的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1251847519&bvid=BV1WJ4m187cp&cid=1473438590&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 队列的基本结构

队列（queue）是一种特殊的线性表结构，只从队尾插入新的元素，并且只从队首弹出元素。一般将队尾称为 rear，队首称为 front。由于该性质，队列通常也被称为 **先进先出** （first in first out）表，简称 FIFO 表。

![队列图像](src\content\posts\stack-and-queue\队列1.png)

## 循环队列基本原理

顺序队列是用数组实现的队列，但是由于定义的数组的空间有限，可以想象一下，当队首 front 和 队尾 rear 经过一系列操作都往后移动时，之前所使用到的空间都不会再被使用了，这造成了空间上的浪费（但在算法题中一般都使用普通的数组队列，或者使用 C++ STL 中的队列）。

所以定义顺序队列往往采用更加高效的 **循环队列** ，其基本上就是在顺序队列的基础上加了一点小小的修改。

解决假溢出的办法是采用循环的方式来组织存放队列元素的数组，即将数组下标为 0 的位置看做是最后一个位置的后继（数组下标为 x 的元素，它的后继为 (x + 1) % SIZE ），这样就形成了循环队列。

### 循环队列的入队操作

> 初始状态下的循环队列

![循环队列图像](src\content\posts\stack-and-queue\循环队列1.png)

> 元素 1 入队

![循环队列图像](src\content\posts\stack-and-queue\循环队列2.png)

> 元素 2、3、4、5 入队

![循环队列图像](src\content\posts\stack-and-queue\循环队列3.png)

下面给出循环队列的入队操作的代码。

```cpp showLineNumbers
void Enter_SqQueue(SqQueue *Q, int e){
    if((Q->rear + 1) % MAXSIZE == Q->front){
	printf("队列已满\n");
	return;
    }
    Q->data[Q->rear] = e; //在队尾指向的地址赋值
    Q->rear = (Q->rear + 1) % MAXSIZE; //队尾指针进1
}
```

### 循环队列的出队操作

> 元素 1 出队

![循环队列图像](src\content\posts\stack-and-queue\循环队列4.png)

> 元素 2、3、4、5 出队

![循环队列图像](src\content\posts\stack-and-queue\循环队列5.png)

下面给出循环队列的出队操作的代码。

```cpp showLineNumbers
void Depart_SqQueue(SqQueue *Q, int *e){
    if(IsEmpty(Q)){
	printf("队列中无元素\n");
	return;
    }
    *e = Q->data[Q->front]; //取出队首指针指向的地址元素
    Q->front = (Q->front + 1) % MAXSIZE; //队首指针进1
}
```

### 循环队列的循环示例

> 入队

此时队列 rear 虽然指向数组的最后，但循环操作可以使其重复利用之前使用的空间。

![循环队列图像](src\content\posts\stack-and-queue\循环队列6.png)

> 出队

类似的，此时队列 front 指向数组的最后。

![循环队列图像](src\content\posts\stack-and-queue\循环队列7.png)

## 循环队列代码讲解

下面是循环队列的完整代码。具体原理较为简单，直接对照上方的基本原理介绍即可。

```cpp showLineNumbers
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define MAXSIZE 1000

typedef int Elemtype;
typedef struct SqQueue{
	
    Elemtype data[MAXSIZE];
    int front; //队列前指针
    int rear; //队列后指针

}SqQueue;

//初始化
void Create_SqQueue(SqQueue *Q){
    Q->front = Q->rear = 0;
}

//判断队列是否为空
bool IsEmpty(SqQueue *Q){
    return Q->front == Q->rear;
}

//求得队列长度
int SqQueue_Length(SqQueue *Q){
    return (Q->rear - Q->front + MAXSIZE) % MAXSIZE;
}

//队列元素入队
void Enter_SqQueue(SqQueue *Q, int e){
    if((Q->rear + 1) % MAXSIZE == Q->front){
	printf("队列已满\n");
	return;
    }
    Q->data[Q->rear] = e; //在队尾指向的地址赋值
    Q->rear = (Q->rear + 1) % MAXSIZE; //队尾指针进1
}

//队列元素出队
void Depart_SqQueue(SqQueue *Q, int *e){
    if(IsEmpty(Q)){
	printf("队列中无元素\n");
	return;
    }
    *e = Q->data[Q->front]; //取出队首指针指向的地址元素
    Q->front = (Q->front + 1) % MAXSIZE; //队首指针进1
}

//取队首
int Get_front(SqQueue *Q){
    if(IsEmpty(Q)){
	printf("队列为空\n");
	return -1;
    }
    return Q->data[Q->front];
}


int main(){
    SqQueue myQueue;
    Elemtype a[5] = {35, 30, 11, 23, 9};

    Create_SqQueue(&myQueue);
    for(int i = 0; i < 5; i++)
        Enter_SqQueue(&myQueue, a[i]);

    Elemtype e;
    Depart_SqQueue(&myQueue, &e);
    printf("出队元素: %d\n", e);

    printf("元素22入队并将所有元素出队: \n");
    Enter_SqQueue(&myQueue, 22);

    while(!IsEmpty(&myQueue)){
    	printf("%d ", Get_front(&myQueue));
    	Depart_SqQueue(&myQueue, &e);
    }

    return 0;
}
```

## 链队列基本原理

链队列是链式的队列结构，其拥有一个 front 指针作为队首，一般队首 front 是不带数据的；还有一个 rear 指针作为队尾，队尾 rear 指向队列的最后一个元素。链队列的操作和链表也有一些相似之处。

### 链队列的入队操作

> 初始状态下的链队列

![链队列图像](src\content\posts\stack-and-queue\链队列1.png)

> 元素 1 入队

![链队列图像](src\content\posts\stack-and-queue\链队列2.png)

> 元素 2、3 入队

![链队列图像](src\content\posts\stack-and-queue\链队列3.png)

下面给出链队列的入队操作的代码。

```cpp showLineNumbers
void Enter_LinkQueue(LinkQueue *Q, int e){
    Linknode *node = (Linknode*)malloc(sizeof(Linknode));
    node->data = e;
    node->next = NULL;

    Q->rear->next = node; //原先队列尾指针后继next指向新节点node
    Q->rear = node; //尾指针重新指向新节点node
}
```

### 链队列的出队操作

> 元素 1 出队

![链队列图像](src\content\posts\stack-and-queue\链队列4.png)

下面给出链队列的出队操作的代码。

```cpp showLineNumbers
void Depart_LinkQueue(LinkQueue *Q, int *e){
    if(Q->rear == Q->front) return;
    Linknode *p;
    p = Q->front->next; //要删除的节点暂存给p
    *e = p->data; //取出删除队头节点的数据
    Q->front->next = p->next; //队头节点的后继next直接跨过删除的节点指向其下一个节点
	
    if(Q->rear == p) //当队列只有一个元素的情况
    	Q->rear = Q->front;   
    free(p);
}
```

## 链队列代码讲解

下面是链队列的完整代码。具体原理较为简单，直接对照上方的基本原理介绍即可。

```cpp frame="code" title="main.cpp"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

typedef int Elemtype;
//队列节点结构
typedef struct Linknode{

    Elemtype data; //队列节点数据域
    struct Linknode *next; //队列next指针域
	
}Linknode;

//链队列整体结构
typedef struct LinkQueue{

    Linknode *front; //链队列首指针  队首指针不带数据
    Linknode *rear; //链队列尾指针

}LinkQueue;

//初始化创建链队列
void Create_LinkQueue(LinkQueue *Q){
    Q->front = Q->rear = (Linknode*)malloc(sizeof(Linknode));
    Q->front->next == NULL;
}

//链队列元素入队
void Enter_LinkQueue(LinkQueue *Q, int e){
    Linknode *node = (Linknode*)malloc(sizeof(Linknode));
    node->data = e;
    node->next = NULL;

    Q->rear->next = node; //原先队列尾指针后继next指向新节点node
    Q->rear = node; //尾指针重新指向新节点node
}

//链队列元素出队
void Depart_LinkQueue(LinkQueue *Q, int *e){
    if(Q->rear == Q->front) return;
    Linknode *p;
    p = Q->front->next; //要删除的节点暂存给p
    *e = p->data; //取出删除队头节点的数据
    Q->front->next = p->next; //队头节点的后继next直接跨过删除的节点指向其下一个节点
	
    if(Q->rear == p) //当队列只有一个元素的情况
    	Q->rear = Q->front;  
    
    free(p);
}

//判断是否为空
bool IsEmpty(LinkQueue *Q){
    return Q->front == Q->rear;
}

//取队首
int Front_LinkQueue(LinkQueue *Q){
    if(IsEmpty(Q)){
	printf("队列为空\n");
	return -1;
    }
    return Q->front->next->data;
}

int main(){
    LinkQueue myQueue;
    Create_LinkQueue(&myQueue);

    Enter_LinkQueue(&myQueue, 1);
    Enter_LinkQueue(&myQueue, 2);
    Enter_LinkQueue(&myQueue, 3);
    printf("当前队首元素为 %d \n", Front_LinkQueue(&myQueue));
    
    Elemtype e;
    Depart_LinkQueue(&myQueue, &e);
    printf("出队的元素为 %d \n", e);
    printf("当前队首元素为 %d \n", Front_LinkQueue(&myQueue)); 
   	
    printf("\n所有元素出队：\n");
    while(!IsEmpty(&myQueue)){
    	printf("%d ", Front_LinkQueue(&myQueue));
    	Depart_LinkQueue(&myQueue, &e);
    }

    return 0;
}
```

## C++ STL 中的队列

C++ 在 STL 中提供了一个容器 `std::queue` ，使用前需要先引入 `<queue>` 头文件。

### STL 定义

```cpp title="STL 中对 queue 的定义"
// clang-format off
template<
    class T,
    class Container = std::deque<T>
> class stack;
```

> `T` 为 queue 中要存储的数据类型。
> 
> `Container` 为用于存储元素的底层容器类型。这个容器必须提供通常语义的下列函数：
> 
>    - `back()`
>    - `front()`
>    - `push_back()`
>    - `pop_back()`
> 
> STL 容器 `std::deque` 和 `std::list` 满足这些要求。如果不指定，则默认使用 `std::deque` 作为底层容器。

### 基本操作

STL 中的 queue 容器提供了一众成员函数以供调用。其中较为常用的有：

1. 访问操作
    - `q.front()` 返回队首元素
    - `q.back()` 返回队尾元素

2. 修改操作
    - `q.push()` 在队尾插入元素
    - `q.pop()` 弹出队首元素

3. 容量操作
    - `q.empty()` 返回是否为空
    - `q.size()` 返回元素数量

此外， `std::queue` 还提供了一些运算符。较为常用的是使用赋值运算符 = 为 queue 赋值，示例：

```cpp showLineNumbers
// 新建两个队列 q1 和 q2
std::queue<int> q1, q2;

// 向 q1 的队尾插入 1
q1.push(1);

// 将 q1 赋值给 q2
q2 = q1;

// 输出 q2 的队首元素
std::cout << q2.front() << std::endl;
// 输出: 1
```

## C++ STL 中的双端队列

C++ 在 STL 中也提供了一个容器 `std::deque` ，使用前需要先引入 `<deque>` 头文件。

### STL 定义

```cpp title="STL 中对 deque 的定义"
// clang-format off
template<
    class T,
    class Allocator = std::allocator<T>
> class deque;
```

> `T` 为 deque 中要存储的数据类型。
> 
> `Allocator` 为分配器，此处不做过多说明，一般保持默认即可。

### 基本操作

STL 中的 deque 容器提供了一众成员函数以供调用。其中较为常用的有：

1. 访问操作
    - `q.front()` 返回队首元素
    - `q.back()` 返回队尾元素

2. 修改操作
    - `q.push_back()` 在队尾插入元素
    - `q.pop_back()` 弹出队首元素
    - `q.push_front()` 在队首插入元素
    - `q.pop_front()` 弹出队首元素
    - `q.insert()` 在指定位置前插入元素（传入迭代器和元素）
    - `q.erase()` 删除指定位置的元素（传入迭代器）

3. 容量操作
    - `q.empty()` 返回是否为空
    - `q.size()` 返回元素数量

此外， `std::deque` 还提供了一些运算符。其中较为常用的有：

- 使用赋值运算符 = 为 deque 赋值，类似 queue
- 使用 [ ] 访问元素，类似 vector

# 队列的拓展应用



# 队列相关视频教程

> 队列的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1953089204&bvid=BV12C411G7LR&cid=1504391699&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

&nbsp;

# 参考文献

## 栈相关博客

1. [【OI WiKi】栈相关知识讲解](https://oi-wiki.org/ds/stack/)

2. [为什么函数式编程语言都离不开栈？](https://blog.csdn.net/qq_65596720/article/details/130743499)

3. [【数据结构】从零理解栈的数据结构](https://blog.csdn.net/qq_37945670/article/details/143643382)

4. [【数据结构】栈（Stack）超详细教学](https://blog.csdn.net/2401_87820834/article/details/145663154)

5. [[数据结构] 栈 (C语言)](https://www.cnblogs.com/MarisaMagic/p/17062088.html)

## 队列相关博客

1. [【OI WiKi】队列相关知识讲解](https://oi-wiki.org/ds/queue/)

2. [[数据结构] 队列 (C语言) ](https://www.cnblogs.com/MarisaMagic/p/17063234.html)

3. [数据结构：图文详解 队列 | 循环队列 的各种操作](https://blog.csdn.net/m0_69519887/article/details/135050236)

4. [数据结构-队列【超详细小白指南】](https://blog.csdn.net/dawn_007_seven/article/details/144294755)