---
title: 【基础数据结构介绍】第二节：栈与队列
published: 2025-11-04
description: 从原理到实现，系统讲解栈与队列的数据结构特性及典型代码示例
tags: [Data Structure, Course, C/C++]
category: Data Structure
draft: false
---

# 栈的基本结构

栈（Stack）是一种特殊的线性表结构，其操作仅允许在同一端进行数据的插入和删除，而另一端保持封闭。这一端通常称为 **栈顶（Top）**，是进行 **压入** 和 **弹出** 的唯一操作点，而栈的另一端称为 **栈底（Bottom）**，始终保持固定不动。栈遵循 **后进先出**（Last In First Out，简称 LIFO）的原则，也就是说最后进入栈的元素会最先被弹出，而最早进入的元素则必须等待后续元素全部弹出后才能访问。这种特性使栈在需要 “逆序访问” 或 “回溯操作” 的场景中具有天然优势。

在具体实现上，栈通常依托 **数组** 或 **链表** 来构建。数组实现的栈结构简单、访问高效，通过下标即可快速定位栈顶元素，但在动态扩容时可能涉及整个数组的数据搬移，因此适用于栈容量可预知的场景。链表实现的栈则能够灵活应对动态大小变化，每次插入和删除仅涉及指针调整，不受固定大小限制，但需要额外的指针空间以维护链表结构。无论是哪种方式，栈都能够高效支持核心操作，包括元素压入、弹出以及读取栈顶元素，同时还能快速判断栈是否为空（IsEmpty）或已满（IsFull）。

栈在计算机科学与工程中有着非常广泛的应用价值。首先，在 **算法设计** 中，栈是 **深度优先搜索（DFS）**、拓扑排序、回溯算法的重要辅助工具，用于记录探索路径、保存状态以及控制访问顺序。其次，在 **表达式求值** 和 **编译原理** 中，操作数和运算符通过栈管理，以实现中缀表达式到后缀表达式的转换以及计算顺序控制。在 **程序运行机制** 层面，每一次函数调用都会在调用栈上生成一个 **栈帧（Stack Frame）**，用于保存函数的局部变量、参数以及返回地址，从而实现递归调用和函数返回的精确控制。除此之外，栈还广泛应用于括号匹配、撤销操作、浏览器的前进/后退功能、状态回退等场景。

## 顺序栈基本原理

顺序栈是一种利用 **连续内存空间**（通常为数组）实现的栈结构，它将栈中元素在内存中依次排列，利用索引实现对栈顶元素的快速访问和操作。顺序栈通过 **栈顶指针** `top` 来标识当前栈顶元素的位置，栈顶指针的变化直接反映了栈的状态，从而方便地进行元素管理。相比于链式栈，顺序栈操作简单、存取速度快，非常适合频繁进行压入和弹出的应用场景。由于采用数组实现，顺序栈具有固定容量，一旦元素数量超过初始分配的数组大小，就需要进行扩容或处理栈溢出，否则将无法继续存储新元素。

* **初始化**：将 `top` 设置为 -1，表示栈为空，此时栈中没有任何元素。
* **入栈**：将 `top` 增加 1，并将新元素存入数组对应位置，使其成为新的栈顶。
* **出栈**：取出当前栈顶元素后，将 `top` 减 1，使栈顶指针回退到前一个元素的位置。

顺序栈遵循 **后进先出（LIFO）** 原则，即最后入栈的元素最先被弹出，这一特性在 **函数调用管理** 、**递归函数执行** 、**表达式求值** 、**深度优先搜索** 等场景中至关重要。它不仅可以用来记录函数的局部状态和返回地址，还能够临时存储中间结果，从而支持算法的回溯和状态管理。由于顺序栈通过连续内存和指针（索引）直接管理数据，它具有操作高效、访问迅速的优势，是许多计算机程序和算法设计中最基础、最常用的数据结构之一。

### 顺序栈入栈操作

在顺序栈中 **压栈操作（Push）** 是指将新元素插入到数组的末端，也就是栈顶位置，使其成为新的栈顶元素。压栈的操作步骤如下：首先判断栈是否已满，即检查栈顶指针 `top` 是否已达到数组的最大下标。如果栈未满，则将 `top` 指针加 1，使其指向新的空位置，再将待入栈的元素存入该位置，从而完成插入。通过这种方式，新元素安全地加入栈顶，而原有元素的顺序保持不变。该操作的时间复杂度为 $O(1)$ ，简单高效。

在实际应用中，如果在栈已满的情况下继续执行压栈操作，会导致 **Stack Overflow（栈溢出）** 错误。因此在设计顺序栈时，需要合理设置数组容量，或者使用动态扩容策略来应对数据量变化。容量设计应兼顾存储需求与性能效率，既保证空间充足，又避免因频繁扩容造成开销。

压栈操作具有广泛应用价值，例如函数调用的参数传递与返回地址管理、表达式求值、递归函数执行、括号匹配检测、撤销操作以及浏览器的前进/后退功能等，都是依赖于将新数据推入栈顶这一基本操作来实现的。

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

在顺序栈中 **出栈操作（Pop）** 是指将当前栈顶元素移除，同时更新栈顶指针 top 的位置，从而保持栈的正确顺序和结构。具体操作步骤如下：首先判断栈是否为空，即检查 top 是否等于 -1。如果栈非空，则访问 top 指向的位置获取栈顶元素的值，然后将 top 减 1，使栈顶指针回退到前一个元素的位置。通过这种方式，栈顶元素被安全移除，原有的栈中元素顺序保持不变。由于出栈操作每次只涉及栈顶的访问和指针调整，其时间复杂度为 $O(1)$ ，操作简单且高效。

在实际应用中，出栈操作在功能上与入栈操作密切配合，共同维持顺序栈的核心特性。它被广泛应用于程序运行中，例如在函数调用的返回过程中，保存函数局部变量和返回地址的栈帧通过出栈操作依次释放；在表达式求值和计算器算法中，操作数和运算符通过出栈进行处理；在递归算法执行、括号匹配检测、撤销操作以及浏览器前进/后退功能等场景中，出栈操作也起着关键作用。

此外，为了提高顺序栈的安全性和鲁棒性，通常会在出栈操作中加入错误处理机制，例如在栈空时返回错误码或抛出异常，防止程序因为非法操作而崩溃。这种严格的操作控制保证了顺序栈在各种应用场景下都能稳定运行。

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

## 完整代码实现

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

## 链式栈基本原理

链栈是一种利用链式存储结构实现的栈，其核心思想是通过动态分配结点来存储元素，而不依赖固定的连续内存空间，因此能够根据实际需要灵活增长或缩减栈容量。链栈的实现方式与单链表的头插法和头删法高度相似，入栈时在链表头部插入新结点，出栈时删除链表首元结点，从而保持 **后进先出（LIFO）** 的原则。

在入栈操作中，需要动态分配一个新的结点，将待入栈的元素存入该结点的数据域，并将新结点的 `next` 指向当前的栈顶结点，然后更新 `top` 指针指向新结点，使其成为新的栈顶。出栈操作则直接访问 `top` 所指向的结点，获取其中的值后，将 `top` 更新为其 `next` 指向的结点，并释放原栈顶结点的内存，从而安全地移除栈顶元素。由于所有操作都集中在链表头部，入栈和出栈的时间复杂度均为 $O(1)$ ，无论栈中元素多少，操作效率始终稳定。

链栈结构的优势在于无需预先设定栈容量，能够动态应对栈深度变化，有效避免顺序栈可能出现的栈溢出问题。此外，链栈在处理递归调用、函数调用栈管理、表达式求值、括号匹配、撤销操作以及动态任务调度等场景中表现出极高的灵活性和安全性。尤其在数据量不确定或变化频繁的情况下，链栈相比顺序栈更加适合实际应用，既节省空间又能保证操作的高效性，同时避免了数组扩容带来的额外开销和复杂性。

### 链栈入栈操作

在链栈中 **入栈操作（Push）** 是将新元素插入到链表的头部，使其成为新的栈顶。操作步骤较为直接，但每一步都必须谨慎处理，以保证链栈结构的完整性和数据的安全性。首先，为待入栈的元素动态分配一个新的结点，并将元素值存入该结点的 `data` 域中；接着，将新结点的 `next` 指针指向当前的栈顶结点，这一步确保新结点能够正确连接到原有链表的前端；最后，将栈顶指针 `top` 更新为新结点，使其成为新的栈顶，并将栈的长度加一以便进行后续操作统计。

由于链栈的存储方式是链式结构，所有入栈操作均发生在链表头部，不依赖连续内存空间，因此不存在数组扩容或空间不足的问题，这使得入栈操作在任何情况下的时间复杂度都维持在 $O(1)$，操作效率非常高。入栈操作的安全性同样重要：在动态分配内存时，需要检查分配是否成功，避免因内存不足导致程序异常；同时更新指针的顺序必须严格按照 “新结点指向旧栈顶 → 更新栈顶指针” 的顺序，否则可能破坏链栈的结构。

链栈入栈操作广泛应用于实际场景，例如函数调用时将局部变量和返回地址压入调用栈、表达式求值时将操作数和运算符临时存储、撤销操作记录以及动态任务调度等。得益于链栈的灵活性和高效性，入栈操作能够在数据量不确定或频繁变化的情况下依然保持稳定和可靠。

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

在链栈中 **出栈操作（Pop）** 是指将当前栈顶元素从链表中移除，同时保持链栈结构的完整性。操作的第一步是判断栈是否为空，即检查栈顶指针 `top` 是否为 `NULL` 。如果栈为空，则出栈操作无法执行，需要进行错误处理或提示用户。若栈非空，首先将栈顶结点的数据保存到临时变量，以便后续使用或返回；然后将栈顶指针 `top` 更新为原栈顶结点的 `next` 指针所指向的下一个结点，从而使原栈顶结点脱离链表结构；接着释放原栈顶结点占用的内存，防止内存泄漏；最后将栈的长度减一。

由于链栈的出栈操作始终发生在链表头部，无需遍历整个链表，因此操作效率高且时间复杂度为 $O(1)$ 。出栈操作确保了元素被按插入顺序逆序取出，同时保留链栈的灵活性，使其能够在动态变化的环境中安全可靠地管理数据。这种操作在函数调用、表达式求值、撤销操作以及任务调度等场景中被广泛使用。

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

## 完整代码实现

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

队列（Queue）是一种特殊的线性表结构，其操作具有严格的端点约束：数据元素只能从一端（**队尾** ，rear）插入，而从另一端（**队首** ，front）删除。这种结构保证了元素的处理顺序与插入顺序完全一致，即最先进入队列的元素最先被移出，遵循 **先进先出**（First In First Out，简称 FIFO）的原则。队列通过维护两个指针或索引来标记队首和队尾，从而可以在插入或删除元素时无需移动队列中其他数据，提高了操作效率。

队列的实现方式主要有两种：**顺序队列** 和 **链式队列** 。顺序队列通常利用数组连续存储元素，通过队首和队尾索引管理队列操作，访问速度快但容量固定，可能面临 “假溢出” 问题，需要循环利用数组空间；链式队列则利用链表动态分配内存，每个结点存储一个元素及指向下一个结点的指针，队列长度不受预设容量限制，更加灵活，适合栈深度或队列长度变化不确定的场景。

队列在计算机科学与工程中具有广泛应用。例如，在操作系统中，队列可用于任务调度、进程管理和时间片轮转；在算法中，广度优先搜索（BFS）依赖队列来保证层级遍历顺序；在通信系统中，队列常用于消息缓冲、数据包处理和事件管理；在软件开发中，队列也用于异步任务管理、缓存队列以及生产者-消费者模型。队列这种严格的端点操作模式，使其成为理解数据流、顺序处理和资源调度的核心基础工具。

![队列图像](src/content/posts/stack-and-queue/队列1.png)

## 环队列基本原理

顺序队列通常利用数组来存储元素，通过 `front` 指向队首、`rear` 指向队尾进行入队和出队操作。然而在普通顺序队列中，随着元素不断出队，数组前端的空间虽然已被释放，但指针不断向后移动，导致这些空间无法再次利用，这种现象被称为 **“假溢出”** 。为了充分利用数组空间，同时保持队列的顺序性，循环队列（Circular Queue）将数组逻辑上首尾相连，形成一个环状结构。这样 `front` 和 `rear` 指针可以在数组范围内循环移动，实现空间的重复利用，从而显著提高存储效率。

在循环队列中，为了能够区分 **队空** 和 **队满** 的状态，通常会牺牲一个存储单元作为缓冲。其核心判定逻辑如下：

* **队空条件**：`front == rear`，表示队列中没有任何元素。
* **队满条件**：`(rear + 1) % MAXSIZE == front`，表示队列已满，此时无法再插入新元素。
* **队列长度计算**：`(rear - front + MAXSIZE) % MAXSIZE`，可以精确计算当前队列中元素的数量。

循环队列的优势在于无需数据搬移即可充分利用整个数组空间，适用于高频率入队和出队的场景。其典型应用包括操作系统中的任务调度队列、网络通信中的消息缓冲区、生产者-消费者模型以及各种实时数据流处理系统。通过循环逻辑，循环队列在保证先进先出顺序的同时，也实现了高效的空间管理和操作性能。

### 循环队列的入队操作

循环队列的 **入队操作（Enqueue）** 是将新元素添加到队尾，同时通过循环方式更新 `rear` 指针，使其始终指向下一个可用位置。该操作时间复杂度为 $O(1)$ ，因为无论队列中有多少元素，插入新元素只涉及一次指针移动和一次数据写入。

在进行入队前，需要先判断队列是否已满，防止新元素覆盖已有数据，这也是循环队列设计中必须考虑的安全约束。由于循环队列的 `rear` 指针会在数组末端自动回绕到起始位置，它能够高效利用数组空间，避免传统顺序队列中 “假溢出” 的问题，因此在连续插入操作中不会浪费存储空间。

入队操作不仅保证新元素被正确放置，还维持了队列的顺序结构，使得后续的出队操作能够按照数据进入的顺序依次访问。循环队列的这种设计在内存利用和操作效率上都具有明显优势，尤其适合需要高频入队的场景。

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

循环队列的 **出队操作（Dequeue）** 是指从队首移除一个元素，并通过循环方式更新 `front` 指针，使其始终指向队列中新的首元素位置。出队操作的时间复杂度为 $O(1)$ ，因为每次仅涉及指针的移动和对元素的访问，无需对队列中其他元素进行移动或调整。

在执行出队操作前，需要先判断队列是否为空，以避免访问不存在的元素或产生非法操作，这是确保队列安全性的必要步骤。通过 `front` 的循环移动，出队操作与入队操作相配合，使队列始终保持连续、可循环利用的数组空间结构。

出队操作不仅保证元素被正确移出，而且维持了队列的顺序结构，使得元素按照进入队列的先后顺序依次被访问和处理。循环队列的这种设计在保证操作效率的同时，也避免了顺序队列中由于元素前移导致的额外开销，使得队列在高频率入队和出队的场景下依旧保持高效性能。

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

## 完整代码实现

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

链队列是一种基于链表实现的队列结构，其核心思想是通过动态分配结点来存储队列元素，从而不依赖固定容量，能够根据实际需要灵活增长。为了方便操作和管理队列，通常会维护两个指针：`front` 和 `rear`。其中，`front` 指向队列的头结点（Dummy Head，不存储有效数据）或首元结点，而 `rear` 指向队列的尾结点，即最后一个实际存储数据的结点。

在本教程中，我们采用 **带头结点** 的链队列实现方式，因此 `front` 本身不存储有效数据，真正的队首元素是 `front->next` 。这种设计具有显著优势：在入队和出队操作中无需对空队列进行额外判断，同时可以统一操作逻辑，使代码更简洁可靠。此外，带头结点的链队列可以方便地处理链表中第一个结点的插入和删除操作，避免了操作过程中头指针的特殊处理问题，从而提升程序的安全性和可维护性。

链队列结构灵活、动态扩展性强，尤其适合队列长度不固定、入队和出队操作频繁的场景，如任务调度、消息缓冲、生产者-消费者模型以及各种需要顺序处理数据的应用。通过维护 `front` 和 `rear` 两个指针，链队列能够高效地支持队列的基本操作，同时保持队列中元素的正确顺序和结构完整性。

### 链队列的入队操作

链队列的 **入队操作（Enqueue）** 是指将一个新元素添加到队列的尾部。在操作过程中，首先为新元素动态分配一个结点空间，并将待插入的数据存储到结点的 `data` 域中。随后，将当前尾结点的 `next` 指针指向新结点，使其成为链表的新尾部，并将 `rear` 指针更新为指向该结点。这样，新元素就被安全地加入到队列末端，同时链表结构保持完整。

由于链队列采用链式存储，不依赖固定容量，因此可以根据需要动态增加结点，避免了顺序队列可能出现的容量限制或 “队满” 问题。整个入队过程操作局部、无需移动其他结点，时间复杂度稳定为 $O(1)$ ，高效且安全。这种方式确保了队列中元素严格按照插入顺序排列，为后续的出队操作提供了可靠的基础。

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

链队列的 **出队操作（Dequeue）** 是指从队列头部移除一个元素，也就是删除头结点之后的第一个结点（首元结点），并获取其存储的数据。在执行操作前，需要先判断队列是否为空：如果 `front->next` 为 `NULL` ，则队列中没有有效元素，不能进行出队操作，以避免访问非法内存。

当队列非空时，将首元结点的指针暂存，读取其 `data` 域的数据，然后将 `front->next` 指向原首元结点的下一个结点，将该结点从链表中移除。随后释放被删除结点占用的内存，以防止内存泄漏。在特殊情况下，如果队列中只有一个元素，出队后队列将变为空，此时必须将 `rear` 指针指回头结点 `front`，以保证队列结构的完整性并避免野指针问题。

链队列的出队操作始终在链表头部完成，操作局部、无需移动其他结点，时间复杂度为 $O(1)$ ，能够高效地支持队列中元素的顺序访问。通过这种方式，链队列能够安全、可靠地管理动态变化的元素数量，同时保持元素插入顺序与删除顺序一致。

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

## 完整代码实现

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