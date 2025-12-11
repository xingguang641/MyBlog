---
title: 【基础数据结构介绍】第二节：栈与队列
published: 2025-11-04
description: 深入浅出讲解栈与队列：原理、实现与代码详解
tags: [Data Structure, Course, C/C++]
category: Data Structure
draft: false
---

# 栈的基本结构

栈（Stack）是一种特殊的线性表结构，其操作仅允许在同一端进行数据的插入和删除，而另一端保持封闭。栈遵循 **后进先出**（Last In First Out，简称 LIFO）的原则，即最后进入栈的元素会最先被弹出。这一特性使得栈在处理需要 “逆序访问” 数据的场景中非常有效。

在具体实现上，栈通常依托数组或链表来构建。数组实现简单、访问高效，但在动态扩容时可能涉及数据搬移；链表实现能够灵活应对动态大小的栈，但需要额外的指针空间。无论是哪种方式，都能够做到高效支持元素的压入（push）与弹出（pop）操作。

栈在计算机科学中有着广泛的应用。例如，在 **深度优先搜索（DFS）** 中，栈用于记录待访问的节点；在 **表达式求值** 中，操作数和运算符可以通过栈进行管理；在程序运行过程中，函数调用会产生 **栈帧**，记录函数的局部变量和返回地址。此外，栈还常用于括号匹配、撤销操作和浏览器的前进/后退功能等场景。凭借这些独特的操作特性，栈不仅是基础的数据结构，也是理解许多算法与系统机制的核心工具。

## 顺序栈基本原理

顺序栈是一种利用连续内存空间（通常为数组）来实现的栈结构。它通过 **栈顶指针** `top` 来标识当前栈顶元素的位置，从而方便地管理栈中的元素。顺序栈的核心特点是操作简单、访问速度快，非常适合频繁进行压入和弹出的场景。由于使用数组实现，顺序栈具有固定容量，如果元素数量超过初始设置，则需要扩容，否则会发生栈溢出。

* **初始化**：将 `top` 设置为 -1，表示栈为空，此时栈中没有任何元素。
* **入栈**：将 `top` 增加 1，并将新元素存入数组对应位置，使其成为新的栈顶。
* **出栈**：取出当前栈顶元素后，将 `top` 减 1，使栈顶指针回退到前一个元素的位置。

顺序栈的操作遵循 **后进先出（LIFO）** 原则，即最后入栈的元素最先被弹出。这种特性在函数调用管理、表达式求值、递归函数的执行等场景中非常重要，也是许多算法设计的基础。

### 顺序栈入栈操作

在顺序栈中，**压栈操作（push）** 是指将新元素插入到数组的末端（即栈顶位置）。操作步骤非常简单：先将栈顶指针 `top` 移动到下一个位置，然后将数据存入该位置即可，因此时间复杂度为 $O(1)$ 。

在实际操作中，需要先判断栈是否已满。如果 `top` 达到数组的最大下标，说明栈空间已用尽，再执行压栈操作会导致 **Stack Overflow** 错误。在应用中，顺序栈容量的设计应根据数据规模和使用场景合理设定，以避免频繁扩容带来的性能开销。

> 初始情况下的栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈1.png)

> 元素 1 入栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈2.png)

> 元素 2 入栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈3.png)

> 元素 3 入栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈4.png)

```c showLineNumbers
// 顺序栈入栈操作
void push(SqStack *s, Elemtype x){
    if(s->top == MAXSIZE - 1) return; // 栈已满，禁止入栈
    s->data[++s->top] = x;
}
```

### 顺序栈出栈操作

**出栈操作（pop）** 是指移除当前栈顶元素，并相应更新栈顶指针 `top` 的位置，使栈保持正确顺序。操作步骤同样简单：直接访问 `top` 指向的位置取出元素，然后将 `top` 减 1。由于每次只操作栈顶元素，时间复杂度为 $O(1)$ 。

在实际应用中，还需注意判断栈是否为空。如果 `top` 为 -1，表示栈中没有元素，此时不能进行出栈操作，否则会出现访问非法内存的错误。出栈操作与入栈操作相辅相成，共同维持了顺序栈 **后进先出（LIFO）** 的特性。

> 元素 3 出栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈5.png)

> 元素 2 出栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈6.png)

> 元素 1 出栈

![顺序栈图像](src/content/posts/stack-and-queue/顺序栈7.png)

```c showLineNumbers
// 顺序栈出栈操作
void pop(SqStack *s, Elemtype *x){
    if(s->top == -1) return; // 栈为空，禁止出栈
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

链栈是利用链式存储结构实现的栈，其实现中通常定义一个指针 `top` 指向链表的头结点或首元结点。链栈的操作实际上对应单链表的头插法和头删法，即入栈时在链表头部插入一个新结点，出栈时删除链表的首元结点。由于链栈不依赖固定容量，它能够根据需要动态增长，因此非常适合栈深度不确定或变化较大的场景。

### 链栈入栈操作

在链栈中，入栈操作（push）即在链表头部插入新结点。操作时，首先为新元素分配结点空间，并将数据存入结点的 `data` 域，然后将新结点的 `next` 指针指向原栈顶结点，最后更新栈顶指针 `top` ，使其指向新结点，同时栈的长度加一。链式结构无需扩容，操作始终在链表头完成，保证了高效性。

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
    S->top = node; // top 指针更新为新结点

    S->length++;
}
```

### 链栈出栈操作

出栈操作（pop）是删除链表的首元结点。操作时首先判断栈是否为空，如果栈为空，则无法进行出栈操作。否则，将栈顶结点的数据保存下来，再将 `top` 指针指向下一个结点，使原栈顶结点脱离栈结构，并释放其占用的内存，同时栈的长度减一。出栈操作也始终在链表头完成，保证了栈的 **后进先出（LIFO）** 特性。

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

队列（Queue）是一种特殊的线性表结构，其操作具有严格的端点约束：数据元素只能从一端（**队尾** ，rear）插入，而从另一端（**队首** ，front）删除。这种结构保证了元素的处理顺序与插入顺序完全一致，即最先进入队列的元素最先被移出，遵循 **先进先出**（First In First Out，简称 FIFO）的原则。队列通过维护两个指针或索引来标记队首和队尾，使得插入和删除操作可以高效完成，而无需移动队列中其他元素。

由于这种独特的操作特性，队列在计算机科学中有着广泛的应用。例如，在操作系统中，队列可用于任务调度和进程管理；在算法中，广度优先搜索（BFS）依赖队列来保证层级遍历的顺序；在通信系统中，队列则常用于消息缓冲和数据包处理。无论是在理论学习还是实际编程中，队列都是理解顺序管理和资源调度的重要工具。

![队列图像](src/content/posts/stack-and-queue/队列1.png)

## 循环队列基本原理

顺序队列通常使用数组来实现，但在普通顺序队列中，随着 `front` 和 `rear` 指针不断向后移动，队列前端已出队的空间无法被再次利用，这种现象被称为 “假溢出” 。为了解决这一问题，可以将数组视作首尾相连的环状结构，这就是 **循环队列** 的核心思想。循环队列通过让指针在数组范围内循环移动，解决了普通顺序队列空间浪费的问题，同时保持队列操作的顺序性。

循环队列中，为了区分队空和队满状态，通常会牺牲一个存储单元。判断逻辑如下：

* **队空条件**：`front == rear` ，表示队列中没有元素。
* **队满条件**：`(rear + 1) % MAXSIZE == front` ，说明队列已满，不能再插入新元素。
* **队列长度计算**：`(rear - front + MAXSIZE) % MAXSIZE` ，可以正确记录队列中元素数量。

### 循环队列的入队操作

循环队列的 **入队操作（enqueue）** 是在队尾插入一个新元素，并将 `rear` 指针向后循环移动一位。入队操作的时间复杂度为 $O(1)$ 。在执行入队操作前，需要检查队列是否已满，防止覆盖已有数据。循环队列由于指针循环移动的特性，能够充分利用数组空间，无需扩容。

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
    Q->data[Q->rear] = e; // 存入元素
    Q->rear = (Q->rear + 1) % MAXSIZE; // rear 指针循环后移
}
```

### 循环队列的出队操作

**出队操作（dequeue）** 是从队首取出元素，并将 `front` 指针向后循环移动一位。出队操作的时间复杂度同样为 $O(1)$ 。在操作前需判断队列是否为空，避免访问不存在的元素。循环队列通过入队和出队操作的循环移动，保证了队列的先进先出（FIFO）特性，同时高效利用了数组空间。

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
    *e = Q->data[Q->front]; // 取出队首元素
    Q->front = (Q->front + 1) % MAXSIZE; // front 指针循环后移
}
```

### 循环队列的循环示例

**入队循环**：在循环队列中，当 `rear` 指针移动到数组末尾时，如果数组前端仍有空闲位置，新的元素不会被阻塞，而是会让 `rear` 自动回绕到下标 0。这样可以充分利用数组前部之前出队腾出的空间，避免顺序队列中常见的 “假溢出” 问题，提高存储利用率。

![循环队列图像](src/content/posts/stack-and-queue/循环队列6.png)

**出队循环**：类似地，当 `front` 指针移动到数组末尾时，它也会循环回到数组开头，以确保队首元素依然能够按先进先出的顺序被访问。通过这种循环机制，循环队列能够在固定大小的数组中高效地支持多次入队和出队操作，同时保证队列逻辑的正确性。

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

链队列是一种基于链表实现的队列结构。为了便于操作，通常会维护两个指针 `front` 和 `rear` 。其中 `front` 指向 **头结点**（Dummy Head，不存储有效数据）或首元结点，而 `rear` 指向队尾的最后一个结点。在本教程中，我们采用 **带头结点** 的链队列实现方式，因此 `front` 本身不存储数据，真正的队首元素是 `front->next` 。这种设计可以简化入队和出队操作，避免对空队列进行特殊处理时出现额外判断。

### 链队列的入队操作

链队列的 **入队操作（enqueue）** 是在链表尾部插入一个新结点，并更新 `rear` 指针以指向新的队尾结点。与顺序队列相比，链队列不受固定容量限制，可以动态增加结点，非常适合元素数量不确定或变化频繁的场景。

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
    Q->rear = node;       // rear 指针更新为新结点
}
```

### 链队列的出队操作

链队列的 **出队操作（dequeue）** 是删除头结点之后的第一个结点，即首元结点，并返回其数据。出队后，需要将 `front->next` 指向下一个结点，从而保持链表结构完整。在特殊情况下，如果队列中只剩一个元素，出队后必须将 `rear` 指针指回 `front`（头结点），否则 `rear` 会成为野指针，导致后续操作出错。

> 元素 1 出队

![链队列图像](src/content/posts/stack-and-queue/链队列4.png)

```c showLineNumbers
void Depart_LinkQueue(LinkQueue *Q, int *e){
    if(Q->rear == Q->front) return; // 队列为空

    Linknode *p = Q->front->next; // p 指向要删除的首元结点
    *e = p->data;

    Q->front->next = p->next; // 跨过 p 指向下一个结点

    // 若删除的是队列中最后一个结点，需修正 rear 指针
    if(Q->rear == p) 
        Q->rear = Q->front;

    free(p); // 释放内存
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

# 栈与队列相关教程

## 栈相关视频

> 栈的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1251847519&bvid=BV1WJ4m187cp&cid=1473438590&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 栈相关博客

1. [【OI WiKi】栈相关知识讲解](https://oi-wiki.org/ds/stack/)

2. [【数据结构】栈 (C语言)](https://www.cnblogs.com/MarisaMagic/p/17062088.html)

3. [为什么函数式编程语言都离不开栈？](https://blog.csdn.net/qq_65596720/article/details/130743499)

4. [【数据结构】从零理解栈的数据结构](https://blog.csdn.net/qq_37945670/article/details/143643382)

5. [【数据结构】栈（Stack）超详细教学](https://blog.csdn.net/2401_87820834/article/details/145663154)

## 队列相关视频

> 队列的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=1953089204&bvid=BV12C411G7LR&cid=1504391699&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 队列相关博客

1. [【OI WiKi】队列相关知识讲解](https://oi-wiki.org/ds/queue/)

2. [【数据结构】队列 (C语言) ](https://www.cnblogs.com/MarisaMagic/p/17063234.html)

3. [数据结构：图文详解 队列 | 循环队列 的各种操作](https://blog.csdn.net/m0_69519887/article/details/135050236)

4. [数据结构-队列【超详细小白指南】](https://blog.csdn.net/dawn_007_seven/article/details/144294755)