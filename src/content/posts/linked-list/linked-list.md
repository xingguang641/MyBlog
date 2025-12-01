---
title: 【基础数据结构介绍】第一节：链表
published: 2025-11-07
description: 深入浅出讲解链表数据结构：从单链表到双向链表
tags: [Data Structure, Course, C/C++]
category: Data Structure
draft: false
---

# 链表的基本结构

链表（Linked List）是一种在物理存储单元中 **非连续、非顺序** 的存储结构。它由一系列结点（Node）组成，这些结点在运行时 **动态分配** 。每个结点通常包含两个部分：
1.  **数据域**：用于存放实际的数据元素。
2.  **指针域**：用于存储下一个结点的内存地址。

与数组一样，链表也是一种线性表。但不同于数组的顺序存储，链表采用链式的动态存储方式，有效地解决了数组的两个主要痛点：
1.  **空间限制**：数组必须预先定义大小，空间满后无法自动扩展（静态数组）。
2.  **内存浪费或碎片**：数组预留过多空间会造成浪费，且需要连续的内存空间。

## 单向链表基本原理

单向链表（Singly Linked List）是链表中最基础的形式。顾名思义，它的每个结点中只包含一个指向 **后继结点** 的指针。因此，链表中的结点只能沿着单一方向（从头到尾）依次访问。

这种结构实现简单，但在进行反向遍历或删除指定结点（需要访问前驱）时效率较低。

### 单向链表的创建

在单向链表中，我们将整个链表类比为一列火车：每节 “车厢” 对应一个结点，数据域是车厢里的 “货物” ，而指针域则是连接下一节车厢的 “车钩” 。

![单向链表图像](src/content/posts/linked-list/单向链表1.png)

```c showLineNumbers
typedef int Elemtype; // 定义数据类型

typedef struct Node {
    Elemtype data;     // 数据域
    struct Node *next; // 指针域：指向下一个结点
} Linklist;
```

**关于头结点（Head Node）：**
在工程实践中，为了统一插入和删除的逻辑，我们通常会设置一个 **哨兵位** ，称为 “头结点” 。
*   **头结点**：不存放有效数据，仅作为链表的入口。
*   **首元结点**：第一个存放有效数据的结点，位于头结点之后。

如下图所示，头结点就像火车的 “车头” ，牵引着后续载货的车厢。

![单向链表图像](src/content/posts/linked-list/单向链表2.png)

```c showLineNumbers
// 链表的初始化（带头结点）
Linklist* Init_Linklist() {
    // 向系统申请内存
    Linklist *head = (Linklist *)malloc(sizeof(Linklist));
    if (head == NULL) return NULL; // 内存申请失败处理
    head->next = NULL; // 初始状态下，头结点的 next 指针为空
    return head;
}
```

单向链表的创建通常有两种方式：**头插法** 和 **尾插法** 。为了保持数据在链表中的顺序与输入顺序一致，我们通常采用 **尾插法** 。

![单向链表图像](src/content/posts/linked-list/单向链表3.png)

```c showLineNumbers
// 创建初始链表 - 采用尾插法
void Create_Linklist(Linklist *head, int n) {    
    Linklist *node, *end; // node:新结点, end:尾指针
    end = head; // 初始时，尾指针指向头结点
    
    printf("创建链表，请输入 %d 个元素: ", n);
    for (int i = 0; i < n; i++) {
        node = (Linklist *)malloc(sizeof(Linklist));
        scanf("%d", &node->data);
        
        end->next = node; // 1. 当前尾结点的 next 指向新结点
        end = node;       // 2. 更新 end 指针，使其指向新的尾结点
    }
    end->next = NULL; // 建表结束，尾结点的指针域置空
}
```

### 单向链表插入操作（头插法）

**头插法（Head Insertion）** 是将新结点插入到 **头结点之后、首元结点之前** 的位置。

*   **特点**：操作简单，无需遍历链表，时间复杂度为 $O(1)$ 。
*   **结果**：生成的链表数据顺序与插入顺序 **相反**（逆序）。

> 头插法图解

![单向链表图像](src/content/posts/linked-list/单向链表4.png)

![单向链表图像](src/content/posts/linked-list/单向链表5.png)

![单向链表图像](src/content/posts/linked-list/单向链表6.png)

![单向链表图像](src/content/posts/linked-list/单向链表7.png)

![单向链表图像](src/content/posts/linked-list/单向链表8.png)

```c showLineNumbers
// 头插法：插入单个数据
void Insert_Front(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->data = data;

    // 核心步骤：先连后断
    node->next = head->next; // 1. 新结点的 next 指向原首元结点
    head->next = node;       // 2. 头结点的 next 指向新结点
}
```

### 单向链表插入操作（尾插法）

**尾插法（Tail Insertion）** 是将新结点追加到链表的最后面。需要通过遍历找到当前的最后一个结点。

*   **特点**：保持了数据的插入顺序。
*   **复杂度**：若无专门的尾指针记录，每次插入需遍历链表，时间复杂度为 $O(n)$ 。

> 尾插法图解

![单向链表图像](src/content/posts/linked-list/单向链表9.png)

![单向链表图像](src/content/posts/linked-list/单向链表10.png)

![单向链表图像](src/content/posts/linked-list/单向链表11.png)

![单向链表图像](src/content/posts/linked-list/单向链表12.png)

```c showLineNumbers
// 尾插法：插入单个数据
void Insert_Back(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->data = data;
    node->next = NULL; // 新结点将成为尾结点，next 必须置空

    Linklist *end = head;
    // 遍历找到最后一个结点
    while (end->next != NULL) {
        end = end->next; 
    }
    end->next = node; // 将当前尾结点的 next 指向新结点
}
```

### 单向链表插入操作（指定位置插入）

在第 $k$ 个数据结点（不含头结点）之前插入新结点。
原理：需要先找到第 $k-1$ 个结点（前驱结点），然后执行插入操作。

```c showLineNumbers
// 指定位置插入
void Insert_Position(Linklist *head, int k) { 
    // k 表示在第 k 个数据结点的位置插入
    Linklist *t = head, *in;
    
    // 寻找第 k-1 个结点
    for (int i = 0; i < k - 1 && t != NULL; i++) {
        t = t->next;
    }

    if (t != NULL) {
        in = (Linklist *)malloc(sizeof(Linklist));
        printf("在第 %d 个位置插入数据: ", k);
        scanf("%d", &in->data);
        
        // 插入逻辑与头插法类似
        in->next = t->next; 
        t->next = in; 
    } else {
        puts("插入位置无效（超出链表长度）");
    }
}
```

### 单向链表遍历操作

遍历即通过指针依次访问链表中的每一个结点，直到指针指向 `NULL` 为止。

```c showLineNumbers
// 打印链表
void Show_Linklist(Linklist *head) {
    Linklist *t = head->next; // 从首元结点开始遍历

    if (t == NULL) {
        puts("链表为空");
        return;
    }

    while (t != NULL) {
        printf("%d ", t->data);
        t = t->next;
    }
    printf("\n\n");
}
```

### 单向链表删除操作

删除第 $k$ 个结点，本质是让 **第 $k-1$ 个结点**（前驱）的指针直接指向 **第 $k+1$ 个结点**（后继），从而将第 $k$ 个结点从链条中 “摘除” ，最后释放其内存。

> 结点删除图解

![单向链表图像](src/content/posts/linked-list/单向链表13.png)

![单向链表图像](src/content/posts/linked-list/单向链表14.png)

![单向链表图像](src/content/posts/linked-list/单向链表15.png)

```c showLineNumbers
// 删除指定位置的结点
void Delete_Position(Linklist *head, int k) {
    Linklist *t = head; 
    Linklist *del = NULL; // 指向待删除结点
    int i = 0;
    
    // 寻找第 k-1 个结点
    while (i < k - 1 && t != NULL) {
        t = t->next; 
        i++;
    }
    
    // t->next 必须存在，否则无法删除第 k 个
    if (t != NULL && t->next != NULL) {
        del = t->next;           // 锁定待删除结点
        t->next = del->next;     // 断开连接：前驱指向后继
        free(del);               // 释放内存
    } else {
        puts("删除位置无效");
    }
}
```

## 单向链表完整代码实现

以下是包含常用操作的完整代码。

```c frame="code" title="singly_linked_list.c"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h> // 引入 bool 类型

typedef int Elemtype;

typedef struct Node {
    Elemtype data;
    struct Node *next;
} Linklist;

// 初始化（带头结点）
Linklist* Init_Linklist() {
    Linklist *head = (Linklist *)malloc(sizeof(Linklist));
    if (head) head->next = NULL;
    return head;
}

// 创建链表（尾插法）
void Create_Linklist(Linklist *head, int n) {
    Linklist *node, *end;
    end = head;
    printf("创建链表输入 %d 个元素: ", n);
    for (int i = 0; i < n; i++) {
        node = (Linklist *)malloc(sizeof(Linklist));
        scanf("%d", &node->data);
        end->next = node;
        end = node;
    }
    end->next = NULL;
}

// 打印链表
void Show_Linklist(Linklist *head) {
    Linklist *t = head->next;
    if (t == NULL) {
        puts("链表为空");
        return;
    }
    while (t != NULL) {
        printf("%d ", t->data);
        t = t->next;
    }
    printf("\n\n");
}

// 头插法
void Insert_Front(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->data = data;
    node->next = head->next;
    head->next = node;
}

// 尾插法
void Insert_Back(Linklist *head, int data) {
    Linklist *node = (Linklist *)malloc(sizeof(Linklist));
    node->data = data;
    node->next = NULL;
    Linklist *end = head;
    while (end->next != NULL) end = end->next;
    end->next = node;
}

// 指定位置插入
void Insert_Position(Linklist *head, int k) {
    Linklist *t = head, *in;
    for (int i = 0; i < k - 1 && t != NULL; i++) t = t->next;

    if (t != NULL) {
        in = (Linklist *)malloc(sizeof(Linklist));
        printf("在第 %d 个结点插入数据: ", k);
        scanf("%d", &in->data);
        in->next = t->next;
        t->next = in;
    } else {
        puts("位置无效");
    }
}

// 修改指定位置数据
void Change_Position(Linklist *head, int n) {
    Linklist *t = head->next; // 从第一个有效结点开始
    for (int i = 1; i < n && t != NULL; i++) t = t->next;

    if (t != NULL) {
        printf("修改第 %d 个结点的数据: ", n);
        scanf("%d", &t->data);
    } else {
        puts("结点不存在");
    }
}

// 删除指定位置结点
void Delete_Position(Linklist *head, int k) {
    Linklist *t = head;
    Linklist *del = NULL;
    int i = 0;
    while (i < k - 1 && t != NULL) {
        t = t->next;
        i++;
    }
    if (t != NULL && t->next != NULL) {
        del = t->next;
        t->next = del->next;
        free(del);
    } else {
        puts("结点不存在");
    }
}

// 清空链表（保留头结点）
void Clear_Linklist(Linklist *head) {
    Linklist *t, *p;
    p = head->next;
    while (p != NULL) {
        t = p;
        p = p->next;
        free(t);
    }
    head->next = NULL;
}

// 判断是否为空
bool IsEmpty(Linklist *head) {
    return head->next == NULL;
}

int main() {
    Linklist *mylist;
    mylist = Init_Linklist();
    if (!mylist) return -1;

    Create_Linklist(mylist, 5);
    printf("初始链表: ");
    Show_Linklist(mylist);

    Insert_Front(mylist, 99);
    printf("头部插入 99 后: ");
    Show_Linklist(mylist);

    Insert_Back(mylist, 88);
    printf("尾部插入 88 后: ");
    Show_Linklist(mylist);

    Insert_Position(mylist, 3);
    printf("第 3 位插入后: ");
    Show_Linklist(mylist);

    Delete_Position(mylist, 1);
    printf("删除第 1 位后: ");
    Show_Linklist(mylist);

    Clear_Linklist(mylist);
    printf("清空后判空: %s\n", IsEmpty(mylist) ? "是" : "否");

    return 0;
}
```

## 双向链表基本原理

双向链表（Doubly Linked List）也叫双链表。其特点是每个结点中都有两个指针：
1.  **prior**：指向直接前驱结点。
2.  **next**：指向直接后继结点。

与单向链表相比，双向链表既可以正向遍历，也可以反向遍历。这使得在查找某个结点的前驱时，时间复杂度从 $O(n)$ 降低到了 $O(1)$ 。

### 双向链表的创建

**注意**：下方的双向链表实现示例采用的是 **不带头结点**（第一个结点即存储数据）的方式，这与上方单向链表的实现略有不同，请留意代码逻辑的区别。

![双向链表图像](src/content/posts/linked-list/双向链表1.png)

```c showLineNumbers
typedef int Elemtype;

typedef struct Node {
    Elemtype data;
    struct Node *prior; // 前驱指针
    struct Node *next;  // 后继指针
} Duplist;
```

在创建初始双向链表时，我们同样采用尾插法。

![双向链表图像](src/content/posts/linked-list/双向链表2.png)

```c showLineNumbers
// 创建双向链表 (注意：此实现不带 dummy head，第一个结点存数据)
Duplist* Create_DuplexLinklist(Duplist *head, int n) {
    head = (Duplist*)malloc(sizeof(Duplist));
    head->next = NULL;
    head->prior = NULL;            
    Duplist *end = head; // end 指向当前尾部                      

    printf("创建双向链表，输入 %d 个数据: ", n);
    scanf("%d", &head->data); // 先处理第一个结点
    
    for (int i = 1; i < n; i++) {
        Duplist *node = (Duplist *)malloc(sizeof(Duplist));
        node->prior = NULL;
        node->next = NULL;
        scanf("%d", &node->data);

        end->next = node;  // 1. 旧尾部指向新结点
        node->prior = end; // 2. 新结点回指旧尾部
        end = node;        // 3. 更新尾指针
    }
    return head;
}
```

### 双向链表插入操作

双向链表的插入操作需要同时维护四个指针方向（前驱的 next、后继的 prior、新结点的 prior、新结点的 next）。

**头插法（针对首个位置）**：
*   新结点的 `next` 指向原头结点。
*   原头结点的 `prior` 指向新结点。
*   更新头指针。

> 头插法图解

![双向链表图像](src/content/posts/linked-list/双向链表3.png)

![双向链表图像](src/content/posts/linked-list/双向链表4.png)

**尾插法（针对末尾位置）**：
*   原尾结点的 `next` 指向新结点。
*   新结点的 `prior` 指向原尾结点。
*   更新尾指针（如果有维护尾指针的话）。

> 尾插法图解

![双向链表图像](src/content/posts/linked-list/双向链表7.png)

![双向链表图像](src/content/posts/linked-list/双向链表8.png)

**指定位置插入**：
最通用的情况（插入中间位置 `p` 之后）：
1. `node->next = p->next;`
2. `node->prior = p;`
3. `if (p->next) p->next->prior = node;`
4. `p->next = node;`

> 指定位置插入操作图解

![双向链表图像](src/content/posts/linked-list/双向链表5.png)

![双向链表图像](src/content/posts/linked-list/双向链表6.png)

```c showLineNumbers
// 插入新结点 (处理头插、尾插、中间插入)
// pos 从 1 开始计数
Duplist *Insert_DuplexLinklist(Duplist *head, int pos, int data) {
    Duplist *node = (Duplist *)malloc(sizeof(Duplist));
    node->data = data;
    node->prior = NULL;
    node->next = NULL;

    // 情况1：插在链表头
    if (pos == 1) { 
        node->next = head; 
        if (head != NULL) head->prior = node; 
        head = node; // 更新头指针
    } else {
        Duplist *t = head;
        // 寻找第 pos-1 个结点
        for (int i = 1; i < pos - 1 && t != NULL; i++) {
            t = t->next;
        }

        if (t == NULL) {
            printf("插入位置无效\n");
            free(node);
            return head;
        }

        // 情况2：插在链表尾 (t 是最后一个结点)
        if (t->next == NULL) { 
            t->next = node; 
            node->prior = t; 
        } else {
            // 情况3：插在中间
            t->next->prior = node; // 后继结点的 prior 指向新结点
            node->next = t->next;  // 新结点的 next 指向后继
            t->next = node;        // 前驱结点的 next 指向新结点
            node->prior = t;       // 新结点的 prior 指向前驱
        }
    }
    return head;
}
```

### 双向链表删除操作

双向链表删除结点非常方便，因为可以通过 `prior` 指针直接找到前驱。

*   **删除核心逻辑**：

    `p->prior->next = p->next;`
    
    `p->next->prior = p->prior;`

当然，需要额外处理 **删除头结点** 和 **删除尾结点** 的边界情况。

> 结点删除图解

![双向链表图像](src/content/posts/linked-list/双向链表9.png)

```c showLineNumbers
// 删除指定位置结点
Duplist* Delete_DuplexLinklist(Duplist *head, int pos) {
    Duplist *t = head;
    // 找到待删除的第 pos 个结点
    for (int i = 1; i < pos && t != NULL; i++) {
        t = t->next; 
    }

    if (t != NULL) {
        // 情况1：删除头结点
        if (t->prior == NULL) { 
            head = t->next; 
            if (head != NULL) head->prior = NULL;
            free(t);
        } 
        // 情况2：删除尾结点
        else if (t->next == NULL) { 
            t->prior->next = NULL; 
            free(t);
        } 
        // 情况3：删除中间结点
        else { 
            t->prior->next = t->next; 
            t->next->prior = t->prior; 
            free(t);
        }
    } else {
        printf("结点不存在\n");
    }
    return head;
}
```

## 双向链表完整代码实现

以下是包含常用操作的完整代码。

```c frame="code" title="doubly_linked_list.c"
#include <stdio.h>
#include <stdlib.h>

typedef int Elemtype;

typedef struct Node {
    Elemtype data;
    struct Node *prior;
    struct Node *next;
} Duplist;

// 创建初始化双向链表 (无哨兵位)
Duplist *Create_DuplexLinklist(Duplist *head, int n) {
    head = (Duplist*)malloc(sizeof(Duplist));
    head->next = NULL;
    head->prior = NULL;            
    Duplist *end = head;

    printf("创建双向链表，输入 %d 个数据: ", n);
    scanf("%d", &head->data); // 输入第一个结点数据

    for (int i = 1; i < n; i++) {
        Duplist *node = (Duplist *)malloc(sizeof(Duplist));
        node->prior = NULL;
        node->next = NULL;
        scanf("%d", &node->data);

        end->next = node; 
        node->prior = end; 
        end = node; 
    }
    return head;
}

// 插入新结点
Duplist *Insert_DuplexLinklist(Duplist *head, int pos, int data) {
    Duplist *node = (Duplist *)malloc(sizeof(Duplist));
    node->data = data;
    node->prior = NULL;
    node->next = NULL;

    if (pos == 1) { 
        node->next = head; 
        if (head != NULL) head->prior = node;
        head = node; 
    } else {
        Duplist *t = head;
        for (int i = 1; i < pos - 1 && t != NULL; i++) t = t->next;

        if (t == NULL) {
            printf("位置越界\n");
            return head;
        }

        if (t->next == NULL) { 
            t->next = node; 
            node->prior = t; 
        } else {
            t->next->prior = node; 
            node->next = t->next; 
            t->next = node; 
            node->prior = t; 
        }
    }
    return head;
}

// 删除指定位置结点
Duplist* Delete_DuplexLinklist(Duplist *head, int pos) {
    Duplist *t = head;
    for (int i = 1; i < pos && t != NULL; i++) t = t->next;

    if (t != NULL) {
        if (t->prior == NULL) { 
            head = t->next; 
            if (head) head->prior = NULL;
            free(t);
        } else if (t->next == NULL) { 
            t->prior->next = NULL; 
            free(t);
        } else { 
            t->prior->next = t->next; 
            t->next->prior = t->prior; 
            free(t);
        }
    } else {
        printf("结点不存在\n");
    }
    return head;
}

// 改变指定位置数据
void Change_DuplexLinklist(Duplist *head, int pos, int data){
    Duplist *t = head;
    for(int i = 1; i < pos && t != NULL; i++) t = t->next;

    if(t != NULL) t->data = data;
    else puts("结点不存在");
}

// 正向打印
void Show_DuplexLinklist(Duplist *head) {
    Duplist *t = head;
    while (t != NULL) {
        printf("%d ", t->data);
        t = t->next;
    }
    printf("\n");
}

// 反向打印
void Reverse_DuplexLinklist(Duplist *head){
    if (head == NULL) return;
    Duplist *t = head;
    while (t->next != NULL) t = t->next; // 走到尾部

    while (t != NULL) {
        printf("%d ", t->data);
        t = t->prior;
    }
    printf("\n");
}

int main() {
    Duplist *mylist = NULL; 

    mylist = Create_DuplexLinklist(mylist, 5);
    printf("初始状态: ");
    Show_DuplexLinklist(mylist);

    mylist = Insert_DuplexLinklist(mylist, 1, 99);
    printf("头部插入 99 后: ");
    Show_DuplexLinklist(mylist);

    mylist = Change_DuplexLinklist(mylist, 2, 88);
    printf("修改第 2 个为 88 后: ");
    Show_DuplexLinklist(mylist);

    mylist = Delete_DuplexLinklist(mylist, 1);
    printf("删除第 1 个后: ");
    Show_DuplexLinklist(mylist);

    printf("反向输出: ");
    Reverse_DuplexLinklist(mylist);

    return 0;
}
```

---

# 链表相关教程

## 链表相关视频

> 链表的实现与可视化

<iframe width="100%" height="468" src="//player.bilibili.com/player.html?isOutside=true&aid=664924086&bvid=BV1ea4y1r75V&cid=1370356359&p=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

## 链表相关博客

1. [【OI WiKi】链表相关知识讲解](https://oiwiki.org/ds/linked-list/)

2. [【数据结构】单向链表及其基本操作(C语言)](https://www.cnblogs.com/MarisaMagic/p/17060466.html)

3. [【数据结构】双向链表及双向循环链表(C语言)](https://www.cnblogs.com/MarisaMagic/p/17058633.html)

4. [【算法通关手册（LeetCode）】链表基础](https://algo.itcharge.cn/02_linked_list/02_01_linked_list_basic/)

5. [【labuladong 的算法笔记】链表（链式存储）基本原理](https://labuladong.online/algo/data-structure-basic/linkedlist-basic/)

6. [【CSDN】深入理解链表：基础概念、操作及应用](https://blog.csdn.net/m0_46566693/article/details/140022120)