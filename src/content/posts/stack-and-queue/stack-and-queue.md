---
title: 【基础数据结构介绍】第二节：栈与队列
published: 2025-11-04
description: 介绍常见的数据结构
tags: [Data Structure, Course]
category: Data Structure
draft: false
---

# 栈的基本结构

栈（Stack）是一种特殊的线性表结构，其操作仅限于在同一端进行数据的插入和删除，另一端则保持封闭。栈的访问遵循 **后进先出** （Last In, First Out，简称 LIFO）的原则，即最后入栈的元素最先被弹出。

在具体实现上，栈通常依托数组或链表来构建，这两种方式都能高效地支持元素的压入与弹出操作。凭借这种独特的操作特性，栈在计算机科学中具有广泛的应用场景，例如深度优先搜索（DFS）、表达式求值、以及函数调用过程中的栈帧管理等，都离不开栈这一重要的数据结构。

## 顺序栈基本原理

顺序栈是利用数组来实现栈的存储结构的一种方式。通常定义一个栈顶指针 `top` ，用于指示当前栈顶元素的位置。初始化时，`top` 的值为 -1，表示栈为空，即此时栈中没有任何元素。每当有新元素入栈时，`top` 的值加 1；当有元素出栈时，`top` 的值减 1。通过这种方式，顺序栈能够高效地完成栈的插入与删除操作。

### 顺序栈入栈操作

在顺序栈中， **压栈操作** （Push）对应于在数组的末尾插入一个新元素。该操作的时间复杂度为 $O(1)$ ，因此非常高效。但需要注意的是，压栈前需要确保数组仍有可用空间。若空间已满，则必须进行扩容操作，而扩容通常涉及新建更大的数组并复制原有元素，这将带来额外的时间和空间开销。

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

在顺序栈中， **出栈操作** （Pop）是指移除当前栈顶的元素，并相应地更新栈顶指针 `top` 的位置，即将 `top` 的值减 1。该操作的时间复杂度为 $O(1)$ ，执行效率极高。在某些实现中，为了防止无用数据占用内存空间，还可以在出栈后显式地清空被移除元素的位置，以确保内存引用被及时释放。

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

下面给出顺序栈的完整代码实现。具体原理较为简单，可结合前文的原理说明进行对照和理解。

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

链栈是利用链式存储结构实现的栈。在实现过程中，通常需要定义一个指针 `top` ，用于指向当前的栈顶结点。链栈的操作过程与链表类似，通过指针的移动和结点的连接来完成元素的入栈与出栈操作。

### 链栈入栈操作

在链栈中， **压栈操作** （Push）通常在链表的头部插入一个新结点来实现，而链表头部插入的时间复杂度为 $O(1)$ 。此外，链式结构不受固定容量的限制，无需进行扩容处理，因此在需要频繁执行压栈操作或栈空间动态变化较大的场景中，链栈具有更好的灵活性和适应性。

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

**出栈操作** （Pop）通常通过删除链表头部结点来实现。具体做法是，将栈顶指针 `top` 指向当前头结点的下一个结点，并释放原栈顶结点所占用的内存空间。由于该操作仅涉及指针的移动和一次释放操作，其时间复杂度同样为 $O(1)$ 。

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

下面给出链栈的完整代码实现。具体原理较为简单，可结合前文的原理说明进行对照和理解。

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

---

# 队列的基本结构

队列（Queue）是一种特殊的线性表结构，数据元素的插入操作只能在表的一端进行（称为 **队尾** ，rear），而删除操作只能在另一端进行（称为 **队首** ，front）。由于这种 “先进入队列的元素先被移出” 的特性，队列通常被称为 **先进先出** （First In, First Out，简称 FIFO）的线性表。

![队列图像](src\content\posts\stack-and-queue\队列1.png)

队列的实现方式主要有两种： **顺序队列** （基于数组）和 **链队列** （基于链表）。

使用数组实现的队列需要预先分配固定的存储空间，虽然可能受到容量限制，但在元素的访问和操作上具有较高的执行效率。

相较之下，基于链表实现的队列没有固定的空间约束，能够根据需要动态扩展，但由于涉及频繁的内存分配与指针操作，其时间与空间开销相对更大。

## 循环队列基本原理

顺序队列是利用数组实现的队列结构。然而，由于数组的存储空间是有限且线性的，当队首指针 `front` 和队尾指针 `rear` 经过多次入队与出队操作后不断向后移动时，先前已经释放的空间将无法被再次利用，从而造成内存空间的浪费（在算法竞赛或工程实践中，也常直接使用普通数组实现的队列，或使用 `C++ STL` 提供的 queue 容器以简化实现）。

在实际应用中，为了解决这一问题，通常采用一种改进形式 ———— **循环队列** 。循环队列在顺序队列的基础上进行了一些简单的结构优化，使得数组的首尾可以逻辑上 “相连” ，从而实现空间的循环利用。

### 循环队列的入队操作

循环队列的基本操作在思想上与栈的操作类似，其核心仍然是对线性存储空间的有序管理。 **入队操作** （Enqueue）即在队尾位置插入一个新元素，时间复杂度为 $O(1)$ ，执行效率很高。由于循环队列在初始化时已确定固定容量，且空间可循环利用，因此无需频繁扩容，也不会出现空间浪费的问题。

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

**出队操作** （Dequeue）用于移除队首位置的元素，并将队首指针 `front` 向后移动一个位置。该操作的时间复杂度同样为 $O(1)$ ，执行效率依旧高效。由于循环队列的结构使得队首指针在到达数组末尾后可以重新回到起始位置，因此无论元素如何出队，整个队列都能保持连续、可循环的逻辑结构。

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

> **入队**

此时虽然队尾指针 `rear` 已经指向数组的末尾，但由于循环队列的结构设计，使得它能够重新利用之前已释放的空间，从而实现队列的循环使用。

![循环队列图像](src\content\posts\stack-and-queue\循环队列6.png)

> **出队**

同样地，当队首指针 `front` 移动到数组末尾时，也可以通过循环机制回到数组的起始位置，继续完成出队操作。

![循环队列图像](src\content\posts\stack-and-queue\循环队列7.png)

## 循环队列代码讲解

下面给出循环队列的完整代码实现。具体原理较为简单，可结合前文的原理说明进行对照和理解。

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

链队列是链式的队列结构，其拥有一个 `front` 指针作为队首，一般队首 `front` 是不带数据的；还有一个 `rear` 指针作为队尾，队尾 `rear` 指向队列的最后一个元素。链队列的操作和链表也有一些相似之处。

### 链队列的入队操作

**入队操作** （Enqueue）是指在链队列的队尾插入一个新结点。具体实现时，需要为新元素分配一个新的结点，并将当前队尾指针 `rear` 的 next 指向该新结点，然后再将 `rear` 更新为新结点。该操作的时间复杂度为 $O(1)$ ，无需像顺序队列那样考虑空间不足或扩容问题，因此在需要频繁入队的场景中具有较高的灵活性和效率。

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

**出队操作** （Dequeue）用于删除链队列队首的结点。具体实现时，将队首指针 `front` 指向的结点移除，并将 `front` 更新为其下一个结点。若出队后队列变为空，还需同时将队尾指针 `rear` 置为空指针，以保持队列结构的正确性。该操作的时间复杂度为 $O(1)$ ，且由于链式存储结构的动态特性，不会受到固定容量的限制。

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

下面给出链队列的完整代码实现。具体原理较为简单，可结合前文的原理说明进行对照和理解。

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