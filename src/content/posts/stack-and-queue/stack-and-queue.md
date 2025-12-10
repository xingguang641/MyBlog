---
title: 【基础数据结构介绍】第二节：栈与队列
published: 2025-11-04
description: 深入浅出讲解栈与队列：原理、实现与代码详解
tags: [Data Structure, Course, C/C++]
category: Data Structure
draft: false
---

# 栈的基本结构

栈（Stack）是一种特殊的线性表结构，其操作仅限于在同一端进行数据的插入和删除，另一端则保持封闭。栈的访问遵循 **后进先出** （Last In, First Out，简称 LIFO）的原则，即最后入栈的元素最先被弹出。

在具体实现上，栈通常依托数组或链表来构建，这两种方式都能高效地支持元素的压入与弹出操作。凭借这种独特的操作特性，栈在计算机科学中具有广泛的应用场景，例如深度优先搜索（DFS）、表达式求值、递归函数的栈帧管理等。

## 顺序栈基本原理

顺序栈是利用连续的内存空间（数组）来实现栈的存储结构。通常定义一个栈顶指针 `top` ，用于指示当前栈顶元素的位置。

*   **初始化**：`top` 的值为 -1，表示栈为空。
*   **入栈**：`top` 加 1，存入数据。
*   **出栈**：取出数据，`top` 减 1。

### 顺序栈入栈操作

在顺序栈中，**压栈操作**（Push）对应于在数组的末尾插入一个新元素。该操作的时间复杂度为 $O(1)$ 。

**注意**：压栈前需检查栈是否已满（`Stack Overflow`）。

> 初始情况下的栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈1.png)

> 元素 1 入栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈2.png)

> 元素 2 入栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈3.png)

> 元素 3 入栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈4.png)

```c showLineNumbers
// 元素入栈
void push(SqStack *s, Elemtype x){
    if(s->top == MAXSIZE - 1) return; // 栈满
    s->data[++s->top] = x;
}
```

### 顺序栈出栈操作

在顺序栈中，**出栈操作**（Pop）是指移除当前栈顶的元素，并相应地更新栈顶指针 `top` 的位置。该操作的时间复杂度为 $O(1)$ 。

> 元素 3 出栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈5.png)

> 元素 2 出栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈6.png)

> 元素 1 出栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈7.png)

```c showLineNumbers
// 元素出栈
void pop(SqStack *s, Elemtype *x){
    if(s->top == -1) return; // 栈空
    *x = s->data[s->top--];
}
```

## 顺序栈代码讲解

下面给出顺序栈的完整代码实现。

```c frame="code" title="SeqStack.c"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h> // 引入 bool 类型

#define MAXSIZE 1000

typedef int Elemtype;
typedef struct{
    Elemtype data[MAXSIZE];
    int top; // 栈顶指针
} SqStack;

// 初始化栈
void Init_SqStack(SqStack *s){
    s->top = -1;
}

// 判断栈是否为空
bool IsEmpty(SqStack *s){
    return s->top == -1;
}

// 元素入栈
void push(SqStack *s, Elemtype x){
    if(s->top == MAXSIZE - 1) {
        printf("栈已满\n");
        return;
    }
    s->data[++s->top] = x;
}

// 元素出栈
void pop(SqStack *s, Elemtype *x){
    if(s->top == -1) {
        printf("栈为空\n");
        return;
    }
    *x = s->data[s->top--];
}

// 取栈顶元素
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

    printf("--- 入栈测试 ---\n");
    for(int i = 1; i <= 5; i++)
        push(&mystack, i);
    printf("当前栈顶元素为: %d\n", top(&mystack));

    printf("--- 出栈测试 ---\n");
    int e;
    pop(&mystack, &e);
    printf("出栈元素为: %d\n", e);
    printf("当前栈顶元素为: %d\n", top(&mystack));

    printf("--- 清空栈测试 ---\n");
    while(!IsEmpty(&mystack)){
        printf("%d ", top(&mystack));
        pop(&mystack, &e);
    }
    printf("\n");
    return 0;
}
```

## 链栈基本原理

链栈是利用链式存储结构实现的栈。在实现过程中，通常定义一个指针 `top` 指向链表的 **头结点**（或首元结点）。

链栈的操作实际上就是单链表的 **头插法**（入栈）和 **头删法**（出栈）。

### 链栈入栈操作

**压栈操作**（Push）即在链表头部插入一个新结点。链式结构不受固定容量限制，无需扩容，非常适合栈深度动态变化较大的场景。

> 初始情况下的链栈

![链栈图像](src/content/posts/stack-and-queue/链栈1.png)

> 元素 1 入栈

![链栈图像](src/content/posts/stack-and-queue/链栈2.png)

> 元素 2 入栈

![链栈图像](src/content/posts/stack-and-queue/链栈3.png)

> 元素 3 入栈

![链栈图像](src/content/posts/stack-and-queue/链栈4.png)

```c showLineNumbers
void LinkStack_push(LinkStack *S, ElemType e){
    LinkStacknode *node;            
    node = (LinkStacknode *) malloc(sizeof(LinkStacknode));
    node->data = e;            
    node->next = S->top; // 新结点的 next 指向旧栈顶
    S->top = node;       // top 指针更新为新结点

    S->length++;
}
```

### 链栈出栈操作

**出栈操作**（Pop）即删除链表的首元结点。将 `top` 指针指向下一个结点，并释放原内存。

> 元素 3 出栈

![链栈图像](src/content/posts/stack-and-queue/链栈5.png)

> 元素 2 出栈

![链栈图像](src/content/posts/stack-and-queue/链栈6.png)

> 元素 1 出栈

![链栈图像](src/content/posts/stack-and-queue/链栈7.png)

```c showLineNumbers
void LinkStack_pop(LinkStack *S, ElemType *e){
    if(IsEmpty(S)) return; // 栈空
                  
    LinkStacknode *del = S->top; 
    *e = del->data;              
    S->top = del->next; // top 指向下一结点

    S->length--;
    free(del); // 释放内存
}
```

## 链栈代码讲解

下面给出链栈的完整代码实现。

```c frame="code" title="LinkedStack.c"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef int ElemType;

// 链栈的结点结构
typedef struct LinkStacknode {
    ElemType data; 
    struct LinkStacknode *next; 
} LinkStacknode;

// 链栈的整体控制结构  
typedef struct {
    LinkStacknode *top;
    int length;
} LinkStack;

// 初始化链栈
void Create_LinkStack(LinkStack *S){
    S->top = NULL;
    S->length = 0;
}

// 判断栈为空
bool IsEmpty(LinkStack *S){
    return S->length == 0; // 或者 return S->top == NULL;
}

// 入栈
void LinkStack_push(LinkStack *S, ElemType e){
    LinkStacknode *node;            
    node = (LinkStacknode *) malloc(sizeof(LinkStacknode)); // 注意 sizeof 应该是结点的大小
    node->data = e;            
    node->next = S->top; 
    S->top = node; 
    S->length++;
}

// 出栈
void LinkStack_pop(LinkStack *S, ElemType *e){
    if(IsEmpty(S)) return;
                  
    LinkStacknode *del = S->top; 
    *e = del->data;              
    S->top = del->next; 

    S->length--;
    free(del); 
}

// 取栈顶
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
    ElemType a[5] = {3, 6, 7, 9, 10};
    
    printf("--- 入栈测试 ---\n");
    for(int i = 0; i < 5; i++)
        LinkStack_push(&S, a[i]);

    printf("栈顶元素：%d\n", LinkStack_getTop(&S));

    printf("--- 出栈测试 ---\n");
    LinkStack_pop(&S, &e);
    printf("出栈元素：%d\n", e);   

    printf("--- 清空栈测试 ---\n");
    while(!IsEmpty(&S)){
        printf("%d ", LinkStack_getTop(&S));
        LinkStack_pop(&S, &e);
    }
    printf("\n");
    return 0;
}
```

---

# 队列的基本结构

队列（Queue）是一种特殊的线性表结构，数据元素的插入操作只能在表的一端进行（ **队尾** ，rear），而删除操作只能在另一端进行（ **队首** ，front）。

这种 “先进入队列的元素先被移出” 的特性，称为 **先进先出**（First In, First Out，简称 FIFO）。

![队列图像](src/content/posts/stack-and-queue/队列1.png)

## 循环队列基本原理

顺序队列利用数组实现。但在普通顺序队列中，随着 `front` 和 `rear` 向后移动，前面已出队的空间无法再次利用（称为 “假溢出” ）。

为了解决这个问题，我们将数组看作首尾相接的圆环，这就是 **循环队列** 。

### 循环队列的判断逻辑

*   **牺牲一个单元**：为了区分队空和队满，通常会少用一个存储空间。
*   **队满条件**：`(rear + 1) % MAXSIZE == front`
*   **队空条件**：`front == rear`
*   **队列长度**：`(rear - front + MAXSIZE) % MAXSIZE`

### 循环队列的入队操作

**入队操作**（Enqueue）即在队尾插入新元素，并将 `rear` 指针循环后移。

> 初始状态下的循环队列

![循环队列图像](src/content/posts/stack-and-queue/循环队列1.png)

> 元素 1 入队

![循环队列图像](src/content/posts/stack-and-queue/循环队列2.png)

> 元素 2、3、4、5 入队

![循环队列图像](src/content/posts/stack-and-queue/循环队列3.png)

```c showLineNumbers
void Enter_SqQueue(SqQueue *Q, int e){
    if((Q->rear + 1) % MAXSIZE == Q->front){
        printf("队列已满\n");
        return;
    }
    Q->data[Q->rear] = e; // 赋值
    Q->rear = (Q->rear + 1) % MAXSIZE; // 指针循环进 1
}
```

### 循环队列的出队操作

**出队操作**（Dequeue）即取出队首元素，并将 `front` 指针循环后移。

> 元素 1 出队

![循环队列图像](src/content/posts/stack-and-queue/循环队列4.png)

> 元素 2、3、4、5 出队

![循环队列图像](src/content/posts/stack-and-queue/循环队列5.png)

```c showLineNumbers
void Depart_SqQueue(SqQueue *Q, int *e){
    if(IsEmpty(Q)){
        printf("队列中无元素\n");
        return;
    }
    *e = Q->data[Q->front]; // 取出数据
    Q->front = (Q->front + 1) % MAXSIZE; // 指针循环进 1
}
```

### 循环队列的循环示例

> **入队循环**：当 `rear` 指向数组末尾时，若数组头部有空位，`rear` 会回到下标 0。

![循环队列图像](src/content/posts/stack-and-queue/循环队列6.png)

> **出队循环**：同理，`front` 指针也会循环移动。

![循环队列图像](src/content/posts/stack-and-queue/循环队列7.png)

## 循环队列代码讲解

下面给出链队列的完整代码实现。

```c frame="code" title="CircularQueue.c"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAXSIZE 1000

typedef int Elemtype;
typedef struct SqQueue{
    Elemtype data[MAXSIZE];
    int front; // 队首指针
    int rear;  // 队尾指针
} SqQueue;

// 初始化
void Create_SqQueue(SqQueue *Q){
    Q->front = Q->rear = 0;
}

// 判断队列是否为空
bool IsEmpty(SqQueue *Q){
    return Q->front == Q->rear;
}

// 求得队列长度
int SqQueue_Length(SqQueue *Q){
    return (Q->rear - Q->front + MAXSIZE) % MAXSIZE;
}

// 入队
void Enter_SqQueue(SqQueue *Q, int e){
    if((Q->rear + 1) % MAXSIZE == Q->front){
        printf("队列已满\n");
        return;
    }
    Q->data[Q->rear] = e;
    Q->rear = (Q->rear + 1) % MAXSIZE;
}

// 出队
void Depart_SqQueue(SqQueue *Q, int *e){
    if(IsEmpty(Q)){
        printf("队列中无元素\n");
        return;
    }
    *e = Q->data[Q->front];
    Q->front = (Q->front + 1) % MAXSIZE;
}

// 取队首
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
    
    printf("--- 入队测试 ---\n");
    for(int i = 0; i < 5; i++)
        Enter_SqQueue(&myQueue, a[i]);

    Elemtype e;
    Depart_SqQueue(&myQueue, &e);
    printf("出队元素: %d\n", e);

    printf("--- 循环测试 ---\n");
    printf("元素 22 入队，随后清空队列: \n");
    Enter_SqQueue(&myQueue, 22);

    while(!IsEmpty(&myQueue)){
        printf("%d ", Get_front(&myQueue));
        Depart_SqQueue(&myQueue, &e);
    }
    printf("\n");

    return 0;
}
```

## 链队列基本原理

链队列是基于链表实现的队列。为了操作方便，通常设置：
*   `front` 指针：指向 **头结点**（Dummy Head，不存数据）或首元结点。
*   `rear` 指针：指向队尾的最后一个结点。

**注意**：本教程采用 **带头结点** 的链队列实现方式，即 `front` 指向一个不存有效数据的头结点，`front->next` 才是真正的队首数据。

### 链队列的入队操作

**入队操作** （Enqueue）即在链表尾部插入新结点，并更新 `rear` 指针。

> 初始状态下的链队列

![链队列图像](src/content/posts/stack-and-queue/链队列1.png)

> 元素 1 入队

![链队列图像](src/content/posts/stack-and-queue/链队列2.png)

> 元素 2、3 入队

![链队列图像](src/content/posts/stack-and-queue/链队列3.png)

```c showLineNumbers
void Enter_LinkQueue(LinkQueue *Q, int e){
    Linknode *node = (Linknode*)malloc(sizeof(Linknode));
    node->data = e;
    node->next = NULL;

    Q->rear->next = node; // 原尾结点的 next 指向新结点
    Q->rear = node;       // rear 指向新结点
}
```

### 链队列的出队操作

**出队操作** （Dequeue）即删除头结点之后的第一个结点（首元结点）。

**特殊处理**：如果队列中只有一个元素，出队后 `rear` 指针需要指回 `front`（头结点），否则 `rear` 会变成野指针。

> 元素 1 出队

![链队列图像](src/content/posts/stack-and-queue/链队列4.png)

```c showLineNumbers
void Depart_LinkQueue(LinkQueue *Q, int *e){
    if(Q->rear == Q->front) return; // 队列为空
    
    Linknode *p = Q->front->next; // p 指向要删除的首元结点
    *e = p->data; 
    
    Q->front->next = p->next; // 跨过 p 连接下一个
	
    // 关键点：若删除的是队列中最后一个结点，需修正 rear 指针
    if(Q->rear == p) 
        Q->rear = Q->front;   
    
    free(p);
}
```

## 链队列代码讲解

下面给出链队列的完整代码实现。

```c frame="code" title="LinkedQueue.c"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef int Elemtype;

// 队列结点结构
typedef struct Linknode{
    Elemtype data; 
    struct Linknode *next; 
} Linknode;

// 链队列控制结构
typedef struct LinkQueue{
    Linknode *front; // 队首指针 (指向头结点)
    Linknode *rear;  // 队尾指针 (指向最后一个元素)
} LinkQueue;

// 初始化（创建带头结点的空队列）
void Create_LinkQueue(LinkQueue *Q){
    // 创建头结点
    Q->front = Q->rear = (Linknode*)malloc(sizeof(Linknode));
    Q->front->next = NULL; // 注意：这里是赋值 =，不是判断 ==
}

// 判断是否为空
bool IsEmpty(LinkQueue *Q){
    return Q->front == Q->rear;
}

// 入队
void Enter_LinkQueue(LinkQueue *Q, int e){
    Linknode *node = (Linknode*)malloc(sizeof(Linknode));
    node->data = e;
    node->next = NULL;

    Q->rear->next = node; 
    Q->rear = node; 
}

// 出队
void Depart_LinkQueue(LinkQueue *Q, int *e){
    if(IsEmpty(Q)) return;

    Linknode *p = Q->front->next; // 待删除结点
    *e = p->data; 
    
    Q->front->next = p->next; 
	
    // 若原队列只有一个结点，删除后变空，rear 需归位
    if(Q->rear == p) 
        Q->rear = Q->front;  
    
    free(p);
}

// 取队首
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

    printf("--- 入队测试 ---\n");
    Enter_LinkQueue(&myQueue, 1);
    Enter_LinkQueue(&myQueue, 2);
    Enter_LinkQueue(&myQueue, 3);
    printf("当前队首元素为 %d \n", Front_LinkQueue(&myQueue));
    
    Elemtype e;
    printf("--- 出队测试 ---\n");
    Depart_LinkQueue(&myQueue, &e);
    printf("出队的元素为 %d \n", e);
    printf("当前队首元素为 %d \n", Front_LinkQueue(&myQueue)); 
   	
    printf("--- 清空测试 ---\n");
    while(!IsEmpty(&myQueue)){
        printf("%d ", Front_LinkQueue(&myQueue));
        Depart_LinkQueue(&myQueue, &e);
    }
    printf("\n");

    return 0;
}
```

---

# 栈相关教程

## 栈相关视频

> 栈的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1251847519&bvid=BV1WJ4m187cp&cid=1473438590&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 栈相关博客

1. [【OI WiKi】栈相关知识讲解](https://oi-wiki.org/ds/stack/)

2. [【数据结构】栈 (C语言)](https://www.cnblogs.com/MarisaMagic/p/17062088.html)

3. [为什么函数式编程语言都离不开栈？](https://blog.csdn.net/qq_65596720/article/details/130743499)

4. [【数据结构】从零理解栈的数据结构](https://blog.csdn.net/qq_37945670/article/details/143643382)

5. [【数据结构】栈（Stack）超详细教学](https://blog.csdn.net/2401_87820834/article/details/145663154)

---

# 队列相关教程

## 队列相关视频

> 队列的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1953089204&bvid=BV12C411G7LR&cid=1504391699&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 队列相关博客

1. [【OI WiKi】队列相关知识讲解](https://oi-wiki.org/ds/queue/)

2. [【数据结构】队列 (C语言) ](https://www.cnblogs.com/MarisaMagic/p/17063234.html)

3. [数据结构：图文详解 队列 | 循环队列 的各种操作](https://blog.csdn.net/m0_69519887/article/details/135050236)

4. [数据结构-队列【超详细小白指南】](https://blog.csdn.net/dawn_007_seven/article/details/144294755)