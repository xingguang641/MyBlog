---
title: 【基础数据结构介绍】第一节：链表
published: 2025-11-07
description: 深入浅出讲解链表数据结构：从单链表到双向链表
tags: [Data Structure, Course, C/C++]
category: Data Structure
draft: false
---

# 链表的基本结构

链表（Linked List）是一种在物理内存中 **非连续存储** 的线性结构。与数组不同，链表的每个结点（Node）在运行时动态申请，系统会将这些被分散分配的结点，通过 “指针” 链接起来，从而构成一个线性的结构。一个典型的链表结点通常包含两个部分：

1.  **数据域（data）**：用于存放实际的数据元素。
2.  **指针域（next）**：用于存储下一个结点的内存地址。

与数组一样，链表属于线性表。但与数组相比，它采用链式存储，因此有效解决了顺序表的两个核心问题：

1.  **空间限制**：数组必须预先定义大小，空间满后无法自动扩展（静态数组）。
2.  **内存浪费或碎片**：数组预留过多空间会造成浪费，且需要连续的内存空间。

## 单向链表基本原理

单向链表（Singly Linked List）是链表结构中最基本、也是最常用的一种形式。其核心特点在于：每个结点仅包含一个指向 **后继结点** 的指针，从而在物理结构上形成一条以头结点为起点、按顺序向后延伸的线性链式存储路径。受限于这种单向链接特性，链表中的数据访问只能沿着从头到尾的方向依次进行，无法通过指针直接回溯到前驱结点。

这种结构的优势在于设计简单、插入和删除操作对局部修改友好，不需要像顺序存储那样移动大量元素，因此在需要频繁调整结点位置的场景中具有一定的性能优势。然而，单向链表也存在明显局限：由于无法直接访问前驱结点，执行反向遍历、按位置删除指定结点或在任意位置插入需要前驱信息的操作时，往往必须从头结点开始顺序查找，从而在时间复杂度上产生额外消耗。

总体而言，单向链表以其结构简洁、操作灵活的特点成为链表体系的基础形态，但其单向链接带来的限制也决定了它在某些应用场景中不如双向链表等更复杂的结构高效。

### 单向链表的创建

在单向链表（Singly Linked List）中，可以将整个结构想象为一列以固定方向相连的车厢。每个结点都包含两部分内容：一部分用于存放实际数据，犹如车厢中承载的货物；另一部分则是指向后继结点的指针，它就像车钩，使得链表能够在同一方向上不断延展下去。正是这种结构，使单向链表能够以灵活的方式进行动态存储。

![单向链表图像](src/content/posts/linked-list/单向链表1.png)

链表节点在代码中的定义如下所示，采用结构体来表示结点，将数据域和指针域统一封装在一个类型中，以便在运行时按需创建和连接结点：

```c showLineNumbers
typedef int Elemtype; // 定义数据类型

typedef struct Node {
    Elemtype data;     // 数据域
    struct Node *next; // 指针域：指向下一个结点
} Linklist;
```

**关于头结点（Head Node）**

在实际工程与教学实现中，我们通常会在链表最前方设置一个 **哨兵结点（Sentinel Node）**，即 **头结点** 。头结点本身并不存储有效数据，但它能显著简化链表操作，使插入、删除等操作无需对链表是否为空、是否为首元位置做特殊判断。

*   **头结点（Head Node）**：不含有效数据，仅作为链表的统一入口。
*   **首元结点（First Node）**：链表中第一个真正存放数据的结点，紧随头结点之后。

如下图所示，你可以把头结点理解为整列火车的 “车头” ，负责牵引后续载货的车厢：

![单向链表图像](src/content/posts/linked-list/单向链表2.png)

链表的初始化如下：

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

单向链表的构建方式主要包括 **头插法** 和 **尾插法** 。如果希望链表中结点的排列顺序与输入顺序一致，那么更常用、更直观的选择就是 **尾插法** 。该方法通过维护一个始终指向当前尾结点的指针，将新结点依次追加到链表末端，从而逐步构造出完整的链表。

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

**头插法（Head Insertion）** 是将新结点直接放置在头结点之后的位置，即始终插入到链表的最前端。由于头结点是整个链表的统一入口，新结点只需要修改两个指针即可完成插入，因此这一操作不依赖链表长度，也不需要遍历任何已有结点，时间复杂度始终为 $O(1)$。这一特性使得头插法非常适合用于快速构建链表或需要频繁在表头添加数据的场景。

不过，头插法的结构特点也决定了它会改变数据的存储顺序：每次新插入的元素都会出现在首元位置，因此最终链表中的数据排列顺序与输入顺序完全相反，形成典型的逆序结构。

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

**尾插法（Tail Insertion）** 是将新结点追加到链表的末尾，使其成为新的尾结点。与头插法不同，尾插法能够完整地保留数据的原始输入顺序，因此在构建逻辑顺序与输入一致的链表时被广泛使用。若链表内部没有维护尾指针，则每次插入操作都必须从头结点顺序遍历到链表末端才能完成，使得时间复杂度维持在 $O(n)$ ；若有尾指针，则可以将复杂度降到 $O(1)$ 。由于尾插法更符合读者对 “向列表末尾追加数据” 的直觉，它在实际工程代码中也更常见，尤其是在需要按自然顺序构建数据结构的情况下。

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

当需要在链表的指定逻辑位置插入新元素时，通常采用 **按位置插入** 的方式。在第 $k$ 个数据结点（不包括头结点）之前插入新结点时，必须首先通过遍历找到第 $k-1$ 个结点，即目标位置的前驱结点。如果前驱结点不存在（例如 $k$ 超出链表长度），则无法完成插入，需要进行异常处理。

完成定位后，插入过程本质上是一次局部的指针调整：新结点的 `next` 指向目标位置原有的结点，而前驱结点的 `next` 则指向新结点。因此，指定位置插入能够保持链表的逻辑顺序，并允许在任意合法位置灵活调整结构，是链表操作中较为常见且重要的基本方法。

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

在单向链表中，遍历操作指的是沿着指针所指示的方向，从首元结点开始依次访问链表中的每一个结点，直到遇到 NULL 指针为止。由于链表的物理结构是离散的，结点之间通过指针相连，因此遍历是认识链表结构的基础操作。

遍历时，我们通常需要先检查链表是否为空；若首元结点不存在，则说明链表中没有任何有效数据，需要及时给出提示。在正常情况下，遍历过程只需不断将指针向后移动，即 “跳到下一节车厢” 继续访问。整个操作的时间复杂度为 $O(n)$ ，与链表长度成正比，是典型的线性时间过程。

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

在单向链表中删除第 $k$ 个结点时，关键在于正确找到其前驱结点，即第 $k-1$ 个结点。由于单向链表只保存指向后继的指针，没有办法直接由某个结点找到其前驱，因此删除操作通常需要从头结点开始依次移动指针，直到精确定位到前驱位置。

完成定位后，删除操作的核心是一次简单而精确的指针调整：将前驱结点的 `next` 指向待删除结点的后继，从而把第 $k$ 个结点从链条中 “绕开” 。被绕开的结点随后需要显式释放内存，以避免产生内存泄漏。若在过程中发现前驱不存在、后继不存在或位置超出链表长度，则应立即终止操作并提示异常情况。整体而言，单向链表的删除操作通过局部的指针重连完成，时间复杂度为 $O(n)$ ，与查找前驱所需的遍历开销一致。

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

双向链表（Doubly Linked List），又称双链表，是线性链式结构的一种重要变体。与仅依靠单个后继指针进行连接的单向链表不同，双向链表在每个结点内部同时维护两个指针域：一个用于指向其直接前驱 `prior` ，另一个用于指向其直接后继 `next` 。正因为如此，双向链表在逻辑上形成了一条可双向通行的链路，使得结点之间的移动不再局限于单方向的推进，而是可以在前后两个方向上灵活地进行遍历与操作。

在实际使用中，这种结构相较于单向链表带来了显著的性能优势。尤其是在需要频繁查找某个结点的前驱或在链表中进行双向扫描的场景下，双向链表能够将原本需要 $O(n)$ 时间复杂度的操作降低到 $O(1)$ ，因为每个结点都天然保存了对前驱的直接引用，无需再次从头开始遍历。正是这种前驱与后继的双重可达性，使得双向链表在插入、删除等局部操作上都表现得极为高效和灵活。

### 双向链表的创建

在构建双向链表时，我们依旧遵循链式结构 “动态生成、逐结点连接” 的基本原则。下面的示例采用 **不带头结点** 的实现方式，即链表的第一个结点直接用于存储输入数据，而不是设置一个空的头结点作为占位。这一点与前面单向链表的实现略有不同，因此在理解代码时，尤其需要关注第一个结点在初始化时应同时处理其前驱与后继指针，避免因指针未正确设置而造成错误链接。

在具体实现中，我们采用尾插法逐步扩展链表。与单向链表相比，这里需要特别注意的是双向指针的维护：每当创建新的结点时，不仅要将旧尾结点的 `next` 指向新结点，还必须让新结点的 `prior` 指向旧尾结点，以确保链表在两个方向上的连接关系保持一致。随着尾部指针不断更新，整个链表便依次构建完成。

![双向链表图像](src/content/posts/linked-list/双向链表1.png)

```c showLineNumbers
typedef int Elemtype;

typedef struct Node {
    Elemtype data;
    struct Node *prior; // 前驱指针
    struct Node *next;  // 后继指针
} Duplist;
```

在创建初始双向链表时，我们同样采用尾插法。创建过程如下所示：

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

整体来说，双向链表的创建过程虽然比单向链表稍显繁琐，但仅是在指针维护方面需要更加谨慎地处理前驱与后继两个方向的连接。其内部逻辑依然保持结构清晰、易于理解，只要在插入时保证双向指针均被正确赋值，链表便能够稳定且高效地完成各种操作。

### 双向链表插入操作

在双向链表中进行插入操作时，需要同时维护前驱与后继两个方向的连接关系，因此相较于单向链表，指针的处理更加精细。无论插入位置位于链表的开头、末尾还是中间，都必须确保四条指针关系被正确更新：前驱结点的 `next`、后继结点的 `prior`，以及新结点自身的 `prior` 与 `next`。

**头插法（插入到链表首部）**

当新结点需要成为链表新的第一个元素时，应先让其 `next` 指向原先的头结点，同时将原头结点的 `prior` 改为指向新结点。完成这些调整后，再更新头指针，使链表从这一结点开始。

> 头插法图解

![双向链表图像](src/content/posts/linked-list/双向链表3.png)

![双向链表图像](src/content/posts/linked-list/双向链表4.png)

**尾插法（插入到链表尾部）**

当插入位置位于表尾时，需要将当前尾结点的 `next` 指向新结点，并让新结点的 `prior` 回指到原尾结点。如果程序中维护了尾指针，还应同步更新该指针以保持链表状态一致。

> 尾插法图解

![双向链表图像](src/content/posts/linked-list/双向链表7.png)

![双向链表图像](src/content/posts/linked-list/双向链表8.png)

**指定位置插入（一般位置）**

插入到链表的中间区间时，新结点必须同时连接 “前驱” 和 “后继” 两个方向。在常见的 “在结点 `p` 之后插入” 这一场景中，指针调整的顺序如下：

1. `node->next = p->next;`
2. `node->prior = p;`
3. `if (p->next) p->next->prior = node;`
4. `p->next = node;`

通过这一系列操作，新结点能够无缝地接入链表，同时保持双向关系的正确性。

> 指定位置插入操作图解

![双向链表图像](src/content/posts/linked-list/双向链表5.png)

![双向链表图像](src/content/posts/linked-list/双向链表6.png)

```c showLineNumbers
// 插入新结点（支持头插、尾插及中间插入）
// pos 从 1 开始计数
Duplist *Insert_DuplexLinklist(Duplist *head, int pos, int data) {
    Duplist *node = (Duplist *)malloc(sizeof(Duplist));
    node->data = data;
    node->prior = NULL;
    node->next = NULL;

    // 情况 1：插入到链表头部
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

        // 情况 2：插入到链表尾部
        if (t->next == NULL) { 
            t->next = node; 
            node->prior = t; 
        } else {
            // 情况 3：插入到链表中间
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

在双向链表中删除结点的操作相对简洁，这是因为结点既能访问后继，也能通过 `prior` 指针直接定位其前驱，从而避免了单向链表中必须顺序查找前驱的低效过程。删除操作的核心在于：让目标结点的前驱与后继重新连在一起，并安全地释放该结点的内存。

*   **删除核心逻辑**：

    `p->prior->next = p->next;`
    
    `p->next->prior = p->prior;`

当然，在实际实现中还需考虑一些边界情况，例如当删除的结点位于链表开头或结尾时，需要对头指针或尾部指针进行特殊处理，以确保链表在删除操作后依旧保持结构完整。

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