---
title: 【基础数据结构介绍】第一节：链表
published: 2025-11-07
description: 介绍常见的数据结构
tags: [Data Structure, Course]
category: Data Structure
draft: false
---

# 链表的基本结构

链表（Linked List）是一种在物理存储单元中 **非连续、非顺序** 的存储结构。它由一系列结点（每个元素称为一个结点）组成，结点可以 **动态创建** 。每个结点通常包含两个部分：一个是用于存放数据元素的 **数据域** ，另一个是用于指向下一个结点地址的 **指针域** 。

与数组一样，链表也可用于数据存储。但与数组的顺序存储不同，链表采用链式的动态存储方式，能够有效地解决两个主要问题：其一，当数组空间已满时，无法再插入新的数据；其二，数组在预留过多空间时容易造成存储浪费。

## 单向链表基本原理

单向链表是链表中最基本的一种形式。顾名思义，它的每个结点中都只包含一个指向 **后继结点** 的指针，因此链表中的结点只能沿着单一方向（从头到尾）依次访问。这种结构实现简单，但不便于从中间位置向前遍历或删除结点。

### 单向链表的创建

在单向链表中，每个结点（Node）都是链表的基本组成单位。可以将整个链表类比成一列火车：每节 “车厢” 对应一个结点，数据域就像车厢中装载的 “货物” ，而指针域则相当于连接下一节车厢的 “车钩” 。

![单向链表图像](src\content\posts\linked-list\单向链表1.png)

```cpp showLineNumbers
typedef int Elemtype; //数据类型

typedef struct Node {

    Elemtype data; //结构体数据域
    struct Node *next; //结构体指针域

} Linklist;
```

在实际使用中，链表通常需要一个头结点（Head Node）。头结点本身一般不存放有效数据，仅作为链表的入口，用于标识整个链表。你可以将它类比为火车的 “车头” ，虽然车头不载货，但它牵引着整列车厢向前运行。

![单向链表图像](src\content\posts\linked-list\单向链表2.png)

```cpp showLineNumbers
//链表的初始化
Linklist* Initial_linklist(){
    //向系统申请内存
    Linklist *head = (Linklist *)malloc(sizeof(Linklist));
    head->next = NULL;
    return head;
}
```

单向链表的初始数据个数可以是任意的。在创建链表时，常用的有两种插入方式： **头插法** 和 **尾插法** 。这里我们采用尾插法 ———— 每次在链表的末尾追加新结点，从而保持数据的顺序与输入顺序一致（后面会具体解释这个方法）。

![单向链表图像](src\content\posts\linked-list\单向链表3.png)

```cpp showLineNumbers
//创建初始链表  采用尾插法
void Create_linklist(Linklist *head, int n) {    
    Linklist *node, *end; //普通节点 尾节点
    end = head; //当链表为空时 头尾指向同一个节点
    printf("创建链表输入 %d 个元素:", n);
    for (int i = 0; i < n; i++) { //n为插入普通节点的个数
	node = (Linklist *)malloc(sizeof(Linklist));
	scanf("%d", &node->data);
	end->next = node; //当前end的next指向了新节点node
	end = node; //end往后移，此时新的节点变成尾节点
    }
    end->next = NULL; //end最后置NULL
}
```

### 单向链表插入操作（头插法）

**头插法** （Head Insertion）是一种在链表头部插入新结点的方式。每次插入时，新结点都会被放在链表第一个数据结点之前，成为新的首结点。

这种方法的特点是插入效率高（无需遍历链表），只需修改两个指针即可完成。由于插入顺序与输入顺序相反，所以最后生成的链表是逆序链表。

> 头插法图解

![单向链表图像](src\content\posts\linked-list\单向链表4.png)

![单向链表图像](src\content\posts\linked-list\单向链表5.png)

![单向链表图像](src\content\posts\linked-list\单向链表6.png)

![单向链表图像](src\content\posts\linked-list\单向链表7.png)

![单向链表图像](src\content\posts\linked-list\单向链表8.png)

下面给出单向链表头插法的代码。

```cpp showLineNumbers
//头插法 插入单个数据
void Insert_Front(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->next = NULL;
    node->data = data;

    node->next = head->next; //新节点node的next指向当前head的next
    head->next = node; //head的next重新指向新节点node
}
```

### 单向链表插入操作（尾插法）

**尾插法** （Tail Insertion）是在链表尾部追加新结点的一种插入方式。与头插法不同，尾插法会将新结点依次添加到链表的末尾，因此生成的链表顺序与输入顺序一致。

> 尾插法图解

![单向链表图像](src\content\posts\linked-list\单向链表9.png)

![单向链表图像](src\content\posts\linked-list\单向链表10.png)

![单向链表图像](src\content\posts\linked-list\单向链表11.png)

![单向链表图像](src\content\posts\linked-list\单向链表12.png)

下面给出单向链表尾插法的代码。

```cpp showLineNumbers
//尾插法 插入单个数据
void Insert_Back(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->next = NULL;
    node->data = data;

    Linklist *end = head; //起初end指向头节点
    while (end->next != NULL)
	end = end->next; //end指针往后移，直到最后一个节点
    end->next = node; //当前end的next指向了新节点node
}
```

### 单向链表插入操作（指定位置插入）

指定位置插入是指在第 $k$ 个带数据结点（不含头结点）之前插入一个新结点。
其原理与头插法类似，只不过此时需要先找到第 $k−1$ 个结点，再在其后插入新结点。

若从头结点开始遍历，指针需移动 $k−1$ 次 才能定位到目标位置。
需要注意的是，当 $k=1$ 时，即在第一个数据结点前插入，此时第 $k−1$ 个结点 就是头结点，操作过程与头插法完全相同。

下面给出单向链表在指定位置插入的代码。

```cpp showLineNumbers
//指定位置插入单个节点
void Insert_position(Linklist *head, int k) { 
    //k表示在第k个普通节点的位置插入新节点
    Linklist *t = head, *in; //t为遍历指针
    //in是要插入的新节点
    for (int i = 0; i < k - 1; i++)
	t = t->next;

    if (t != NULL) {
	in = (Linklist *)malloc(sizeof(Linklist));
	in->next = NULL;
	printf("在第 %d 个节点处插入新节点的数据: ", k);
	scanf("%d", &in->data);
	in->next = t->next; //插入节点in的next指向当前第k-1个普通节点的next指向的节点
	t->next = in; //第k-1个普通节点的next重新指向插入的节点in

	//原理和头插法类似 就好像把第k-1个普通节点t看做是头节点
    } else {
	puts("节点不存在");
    }
}
```

### 单向链表遍历操作

我们需要用指针去访问链表中的数据。定义了一个指针 $t$ ，来对链表的每一个存有数据的节点进行访问并读取数据，直到当前节点为 NULL，停止遍历。

通俗地来说，就好比一个卸货员工，他挨个从头到尾取下每一节火车车厢的货物，直到最后到达尾部车厢的时候，他便不再取下货物。

下面给出单向链表遍历操作的代码。

```cpp showLineNumbers
//打印链表
void Show_linklist(Linklist *head) {
    Linklist *t = head->next; //t为遍历指针 访问每个节点数据

    if (t == NULL)
	puts("链表为空");

    while (t != NULL) {
	printf("%d ", t->data);
	t = t->next;
    }
    printf("\n\n");
}
```

### 单向链表删除操作

删除单个结点的操作相对简单。只需先找到待删除结点的前驱结点，然后让该结点的指针域直接指向待删除结点的下一个结点，即可实现跳过中间结点，从而完成删除操作。

> 节点删除图解

![单向链表图像](src\content\posts\linked-list\单向链表13.png)

![单向链表图像](src\content\posts\linked-list\单向链表14.png)

![单向链表图像](src\content\posts\linked-list\单向链表15.png)

下面给出单向链表删除操作的代码。

```cpp showLineNumbers
void Delete_position(Linklist *head, int k) { //k表示要删除第k个节点
    Linklist *t = head, *del = NULL; //t为遍历指针
    int i = 0;
    while (i < k - 1 && t != NULL) {
	t = t->next; //t指向删除的第k个的前一个节点
	i++;
    }
    if (t != NULL) {
	del = t->next;                  
	t->next = del->next;
	free(del);
    } else {
	puts("节点不存在");
    }
}
```

## 单向链表代码讲解

下面给出单向链表的完整代码实现，其中包含了前面未提到的一些常用基础操作，便于更全面地理解单向链表的结构与实现方式。

```cpp showLineNumbers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef int Elemtype; //数据类型

typedef struct Node {

    Elemtype data; //结构体数据域
    struct Node *next; //结构体指针域

} Linklist;

//链表的初始化
Linklist* Initial_linklist(){
    //向系统申请内存
    Linklist *head = (Linklist *)malloc(sizeof(Linklist));
    head->next = NULL;
    return head;
}

//创建初始链表  采用尾插法
void Create_linklist(Linklist *head, int n) { //头节点(不带数据)
    Linklist *node, *end; //普通节点 尾节点
    end = head; //当链表为空时 头尾指向同一个节点
    printf("创建链表输入 %d 个元素:", n);
    for (int i = 0; i < n; i++) { //n为插入普通节点的个数
	node = (Linklist *)malloc(sizeof(Linklist));
	scanf("%d", &node->data);
	end->next = node; //当前end的next指向了新节点node
	end = node; //end往后移，此时新的节点变成尾节点
    }
    end->next = NULL; //end最后置NULL
}

//打印链表
void Show_linklist(Linklist *head) {
    Linklist *t = head->next; //t为遍历指针 访问每个节点数据
    if (t == NULL)
	puts("链表为空");

    while (t != NULL) {
	printf("%d ", t->data);
	t = t->next;
    }
    printf("\n\n");
}

//头插法 插入单个数据
void Insert_Front(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->next = NULL;
    node->data = data;

    node->next = head->next; //新节点node的next指向当前head的next
    head->next = node; //head的next重新指向新节点node
}

//尾插法 插入单个数据
void Insert_Back(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->next = NULL;
    node->data = data;

    Linklist *end = head; //起初end指向头节点
    while (end->next != NULL)
	end = end->next; //end指针往后移，直到最后一个节点
    end->next = node; //当前end的next指向了新节点node
}

//指定位置插入单个数据
void Insert_position(Linklist *head, int k) { //k表示在第k个普通节点的位置插入新节点
    Linklist *t = head, *in; //t为遍历指针
    //in是要插入的新节点
    for (int i = 0; i < k - 1; i++)
	t = t->next;

    if (t != NULL) {
	in = (Linklist *)malloc(sizeof(Linklist));
	in->next = NULL;
	printf("在第 %d 个节点处插入新节点的数据: ", k);
	scanf("%d", &in->data);
	in->next = t->next; //插入节点in的next指向当前第k-1个普通节点的next指向的节点
	t->next = in; //第k-1个普通节点的next重新指向插入的节点in

	//原理和头插法类似 就好像把第k-1个普通节点t看做是头节点
    } else {
	puts("节点不存在");
    }
}

//指定位置改变节点的数据
void Change_position(Linklist *head, int n) { //n表示要改变的是第n个普通节点
    Linklist *t = head; //t为遍历指针
    for (int i = 0; i < n; i++)
        t = t->next; //t指向要改变的节点

    if (t != NULL) {
	printf("修改第 %d 个节点的数据: ", n);
	scanf("%d", &t->data);
    } else {
	puts("节点不存在");
    }
}

//指定位置删除节点
void Delete_position(Linklist *head, int k) { //k表示要删除第k个节点
    Linklist *t = head, *del = NULL; //t为遍历指针
    int i = 0;
    while (i < k - 1 && t != NULL) {
	t = t->next; //t指向删除的第k个的前一个节点
	i++;
    }
    if (t != NULL) {
	del = t->next;                  
	t->next = del->next;
	free(del);
    } else {
	puts("节点不存在");
    }
}

//查找元素返回节点位置
void Find_Element(Linklist *head, int x) {
    Linklist *t = head->next;
    while (t != NULL) {
	int sub = 1;
	if (t->data == x)
	    printf("元素 %d 的位置为: %d \n", x, sub);

	t = t->next;
	sub++;
    }
    if (t == NULL)
	puts("元素不存在");
}

//读取指定节点位置元素
void Read_position(Linklist *head, int k) {
    Linklist *t = head->next;
    for (int i = 0; i < k; i++)
	t = t->next;
    printf("第 %d 个节点位置的数据为: %d \n", k, t->data);
}

//计算链表的长度
void List_length(Linklist *head){
    Linklist *t = head->next;
    int len = 0;
    while(t){
	len++;
        t = t->next;
    }
    printf("链表的长度为: %d \n", len);
}

//清空链表
void Clear_linklist(Linklist *head) {
    Linklist *t;
    while (head->next != NULL) {
	t = head->next;
	head->next = t->next;
	free(t);
    }
}

//判断是否为空
bool IsEmpty(Linklist *head){
    return head->next == NULL;
}

int main() {
    //头指针初始化
    Linklist *mylist;
    mylist = Initial_linklist();

    Create_linklist(mylist, 10);
    printf("初始状态链表:\n");
    Show_linklist(mylist);

    Insert_Front(mylist, 30);
    Insert_Back(mylist, 30);
    printf("链表进行首尾插入数字30后:\n");
    Show_linklist(mylist);

    Insert_position(mylist, 5);
    printf("链表进行在第5个节点后插入新节点后:\n");
    Show_linklist(mylist);

    Change_position(mylist, 4);
    printf("链表进行改变第4个数据后:\n");
    Show_linklist(mylist);

    Delete_position(mylist, 1);
    printf("链表进行删除第1个数据后:\n");
    Show_linklist(mylist);

    Clear_linklist(mylist);
    printf("链表进行清空后:\n");
    if(IsEmpty(mylist))
	puts("链表为空");

    return 0;
}
```

## 双向链表基本原理

双向链表也叫双链表，其每个数据结点中都有两个指针，分别指向直接 **后继** 和直接 **前驱** 。与单向链表相比，双向链表既可以正向遍历，也可以反向遍历。这使得在查找某个结点的前驱时，无需像单向链表那样重新遍历整个链表，从而大幅提高了操作效率。

### 双向链表的创建

双向链表的单个节点含有两个指针域和一个值域。

![双向链表图像](src\content\posts\linked-list\双向链表1.png)

```cpp showLineNumbers
typedef int Elemtype;

typedef struct Node {

    Elemtype data;
    struct Node *prior; //前驱指针
    struct Node *next; //后驱指针

} Duplist;
```

从结构上看，双向链表可以看作是在单向链表的基础上，为每个结点 **额外增加了一个指向前驱结点的指针** 。通过这种方式，链表中的结点不仅能与后继建立链接关系，也能与前驱结点互相连接。

在创建初始的双向链表时，通常采用尾插法来依次插入新结点。

![双向链表图像](src\content\posts\linked-list\双向链表2.png)

```cpp showLineNumbers
//创建初始化双向链表(头节点有数据，便于表头插入)
Duplist* Create_DuplexLinklist(Duplist *head, int n) {
    head = (Duplist*)malloc(sizeof(Duplist));
    head->next = NULL;
    head->prior = NULL;            
    Duplist *end = head;                       

    printf("创建双向链表输入 %d 个数据: ", n);
    scanf("%d", &head->data);
    for (int i = 1; i < n; i++) {
	Duplist *node = (Duplist *)malloc(sizeof(Duplist));
	node->prior = NULL;
	node->next = NULL;
	scanf("%d", &node->data);

	end->next = node; //end的next指向新节点node
	node->prior = end; //新节点node的前驱prior指向之前的end
	end = node; //end指向最后的node节点
    }
    return head;
}
```

### 双向链表插入操作

双向链表的头插法与单向链表类似，只是在操作时需要同时维护前驱指针。具体步骤如下：

- 将原头结点 `head` 的 `prior` 指向新结点 `node`
- 将新结点 `node` 的 `next` 指向原头结点 `head`
- 更新头指针 `head = node` ，使新结点成为新的表头

> 头插法图解

![双向链表图像](src\content\posts\linked-list\双向链表3.png)

![双向链表图像](src\content\posts\linked-list\双向链表4.png)

双向链表的尾插法与单向链表类似，只是在操作时需要同时维护前驱指针。具体步骤如下：

- 将当前尾结点 `end` 的 `next` 指向新结点 `node`
- 将新结点 `node` 的 `prior` 指向原尾结点 `end`
- 更新尾指针 `end = node` ，使其成为新的链表尾部

>  尾插法图解

![双向链表图像](src\content\posts\linked-list\双向链表7.png)

![双向链表图像](src\content\posts\linked-list\双向链表8.png)

双向链表在指定位置插入节点的操作与上面一样，需要同时维护前驱和后继。具体步骤如下：

- 将新结点 `node` 的 `next` 指向 `p -> next`
- 将新结点 `node` 的 `prior` 指向 `p`
- 若 `p -> next` 不为空，则将 `p -> next -> prior` 指向 `node`
- 最后将 `p -> next` 指向 `node`

>  指定位置插入操作图解

![双向链表图像](src\content\posts\linked-list\双向链表5.png)

![双向链表图像](src\content\posts\linked-list\双向链表6.png)

```cpp showLineNumbers
//插入新节点(包含三种情况 头插 尾插 和 指定位置插入)
Duplist *Insert_DuplexLinklist(Duplist *head, int pos, int data) {
	Duplist *node = (Duplist *)malloc(sizeof(Duplist));
	node->data = data;
	node->prior = NULL;
	node->next = NULL;
	//pos表示要插入的位置（head为1）
	if (pos == 1) { //插在链表头的情况
		node->next = head; //新节点node的next指向之前的头head
		head->prior = node; //之前的head的前驱prior指向了node
		head = node; //head重新指向了插在表头的新节点
	} else {
		Duplist *t = head; //t为遍历指针
		for (int i = 1; i < pos - 1; i++) //t指向要插入位置的前一个节点
			t = t->next;

		if (t->next == NULL) { //插在链表尾的情况
			t->next = node; //t指向表尾，t的next指向新节点node
			node->prior = t; //新节点node的前驱prior指向t
		} else {
			//插在表中的情况
			t->next->prior = node; //t的下一个节点(要代替位置的节点)的前驱指向新node
			node->next = t->next; //新node的next指向了之前t的下一个节点
			t->next = node; //t的next重新指向新node
			node->prior = t; //node前驱prior指向了t
		}
	}

	return head;
}
```

### 双向链表删除操作

在双向链表中删除结点时，需要同时维护其前驱和后继结点的连接关系。不同于单向链表，双向链表可以通过前驱指针直接找到要删除结点的前一个结点，因此无需遍历整个链表。

删除结点后，只需让前驱与后继重新建立连接即可。若删除的是表头或表尾结点，还需要相应地更新头指针或尾指针。

这种结构使得双向链表的删除操作更加高效、灵活。

>  节点删除图解

![双向链表图像](src\content\posts\linked-list\双向链表9.png)

下面给出双向链表删除操作的代码。

```cpp showLineNumbers
//删除指定位置节点
Duplist* Delete_DuplexLinklist(Duplist *head, int pos) {
	Duplist *t = head;
	for (int i = 1; i < pos; i++)
		t = t->next; //找到要删除的节点

	if (t != NULL) {
		if (t->prior == NULL) { //如果是头节点
			head = t->next; //head往后移
			free(t);
			head->prior = NULL;
			return head;
		} else if (t->next == NULL) { //如果是尾节点
			t->prior->next = NULL; //表尾的前一个节点的next置NULL
			free(t);
			return head;
		} else { //删除表中节点的情况
			t->prior->next = t->next; //要删除节点的前一个节点的next跨越直接指向下下个节点
			t->next->prior = t->prior; //要删除节点的后一个节点的prior跨越指向上上个节点
			free(t);
			return head;
		}
	} else
		printf("节点不存在\n");

    return head;
}
```

## 双向链表代码讲解

下面给出双向链表的完整代码实现，其中包含了前面未提到的一些常用基础操作，便于更全面地理解单向链表的结构与实现方式。

```cpp showLineNumbers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int Elemtype;

typedef struct Node {

	Elemtype data;
	struct Node *prior; //前驱指针
	struct Node *next; //后驱指针

} Duplist;

//创建初始化双向链表(头节点有数据，便于表头插入，要与单向链表区分)
Duplist *Create_DuplexLinklist(Duplist *head, int n) {
	head = (Duplist*)malloc(sizeof(Duplist));
	head->next = NULL;
	head->prior = NULL;            
	Duplist *end = head; //用于在尾部插入新节点

	printf("创建双向链表输入 %d 个数据: ", n);
	scanf("%d", &head->data);
	for (int i = 1; i < n; i++) {
		Duplist *node = (Duplist *)malloc(sizeof(Duplist));
		node->prior = NULL;
		node->next = NULL;
		scanf("%d", &node->data);

		end->next = node; //之前的end的next指向新节点node
		node->prior = end; //新节点node的前驱prior指向之前的end
		end = node; //end永远指向最后的node节点
	}

	return head;
}

//插入新节点(包含三种情况 头插 尾插 和 指定位置插入)
Duplist *Insert_DuplexLinklist(Duplist *head, int pos, int data) {
	Duplist *node = (Duplist *)malloc(sizeof(Duplist));
	node->data = data;
	node->prior = NULL;
	node->next = NULL;
	//pos表示要插入的位置（head为1）
	if (pos == 1) { //插在链表头的情况
		node->next = head; //新节点node的next指向之前的头head
		head->prior = node; //之前的head的前驱prior指向了node
		head = node; //head重新指向了插在表头的新节点
	} else {
		Duplist *t = head; //t为遍历指针
		for (int i = 1; i < pos - 1; i++) //t指向要插入位置的前一个节点
			t = t->next;

		if (t->next == NULL) { //插在链表尾的情况
			t->next = node; //t指向表尾，t的next指向新节点node
			node->prior = t; //新节点node的前驱prior指向t
		} else {
			//插在表中的情况
			t->next->prior = node; //t的下一个节点(要代替位置的节点)的前驱指向新node
			node->next = t->next; //新node的next指向了之前t的下一个节点
			t->next = node; //t的next重新指向新node
			node->prior = t; //node前驱prior指向了t
		}
	}

	return head;
}

//删除指定位置节点
Duplist* Delete_DuplexLinklist(Duplist *head, int pos) {
	Duplist *t = head;
	for (int i = 1; i < pos; i++)
		t = t->next; //找到要删除的节点

	if (t != NULL) {
		if (t->prior == NULL) { //如果是头节点
			head = t->next; //head往后移
			free(t);
			head->prior = NULL;
			return head;
		} else if (t->next == NULL) { //如果是尾节点
			t->prior->next = NULL; //表尾的前一个节点的next置NULL
			free(t);
			return head;
		} else { //删除表中节点的情况
			t->prior->next = t->next; //要删除节点的前一个节点的next跨越直接指向下下个节点
			t->next->prior = t->prior; //要删除节点的后一个节点的prior跨越指向上上个节点
			free(t);
			return head;
		}
	} else
		printf("节点不存在\n");

    return head;
}

//读取单个数据
void Read_DuplexLinklist(Duplist *head, int pos) {
	Duplist *t = head;
	for (int i = 1; i < pos; i++)
		t = t->next;

	if (t != NULL)
		printf("第 %d 个位置的数据为 %d", pos, t->data);
	else
		puts("节点不存在");
}

//改变指定位置数据
Duplist* Change_DuplexLinklist(Duplist *head, int pos, int data){
	Duplist *t = head;
	for(int i = 1; i < pos; i++)
		t = t->next;

	if(t != NULL)
		t->data = data;
	else
		puts("节点不存在");

	return head;
}

//查找数据返回下标
int Find_DuplexLinklist(Duplist *head, int n) {
	Duplist *t = head;
	int pos = 1;
	while (t != NULL) {
		if (t->data == n) {
			printf("该数据的位置为 %d", pos);
		}
		t = t->next;
		pos++;
	}
	return -1;
}

//遍历打印双向链表
void Show_DuplexLinklist(Duplist *head) {
	Duplist *t = head;
	while (t != NULL) {
		printf("%d ", t->data);
		t = t->next;
	}
	printf("\n");
}

//反向打印双向链表  
void Reverse_DuplexLinklist(Duplist *head){
	Duplist *t = head;
	while (t->next != NULL) //指向最后一个节点
		t = t->next;

	while (t != NULL)
	{
		printf("%d ",t->data);
		t = t->prior;
	}
	printf("\n");
}

int main() {
	Duplist *mylist = NULL; 

	mylist = Create_DuplexLinklist(mylist, 10);
	puts("初始状态双向链表:");
	Show_DuplexLinklist(mylist);
	printf("\n");

    mylist = Insert_DuplexLinklist(mylist, 11, 30);
	mylist = Insert_DuplexLinklist(mylist, 1, 30);
	puts("在头和尾 的位置插入数据30后:");
	Show_DuplexLinklist(mylist);
	printf("\n");

	mylist = Change_DuplexLinklist(mylist,5,22);
	puts("改变第 5 的位置数据为 22 后:");
	Show_DuplexLinklist(mylist);
	printf("\n");

	mylist = Delete_DuplexLinklist(mylist, 8);
	mylist = Delete_DuplexLinklist(mylist, 1);
	puts("删除第 1 和 8 的位置数据后:");
	Show_DuplexLinklist(mylist);
	printf("\n");

	puts("双向链表反向输出:");
	Reverse_DuplexLinklist(mylist);
	printf("\n");

	return 0;
}
```

# 链表相关教程

## 链表相关视频

> 链表的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=664924086&bvid=BV1ea4y1r75V&cid=1370356359&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 链表相关博客

1. [【OI WiKi】链表相关知识讲解](https://oiwiki.org/ds/linked-list/)

2. [【数据结构】单向链表及其基本操作(C语言)](https://www.cnblogs.com/MarisaMagic/p/17060466.html)

3. [【数据结构】双向链表及双向循环链表(C语言)](https://www.cnblogs.com/MarisaMagic/p/17058633.html)

4. [【数据结构】链表(单链表实现+详解+原码)](https://blog.csdn.net/Edward_Asia/article/details/120876314)

5. [【算法通关手册（LeetCode）】链表基础](https://algo.itcharge.cn/02_linked_list/02_01_linked_list_basic/)

6. [【labuladong 的算法笔记】链表（链式存储）基本原理](https://labuladong.online/algo/data-structure-basic/linkedlist-basic/)

7. [深入理解链表：基础概念、操作及应用](https://blog.csdn.net/m0_46566693/article/details/140022120)

8. [【链表】单链表的基本操作详解(C语言)](https://blog.csdn.net/ffortunateoy/article/details/90731996)

9. [【数据结构】：单链表之头插法和尾插法（动图+图解）](https://blog.csdn.net/weixin_46629453/article/details/125643226)