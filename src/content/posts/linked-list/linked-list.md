---
title: 【基础数据结构介绍】第一节：链表
published: 2025-11-07
description: 从单链表到双向链表，系统讲解链表的结构特点、操作原理与代码实现
tags: [Data Structure, Course, C/C++]
category: Data Structure
draft: false
---

# 链表的基本结构

链表（Linked List）是一种在物理内存中 **非连续存储** 的线性结构。与数组不同，链表的每个结点（Node）在运行时动态申请，系统会将这些被分散分配的结点，通过指针链接起来，从而构成一个线性的结构。一个典型的链表结点通常包含两个部分：

1.  **数据域（data）**：用于存放实际的数据元素。
2.  **指针域（next）**：用于存储下一个结点的内存地址。

与数组一样，链表属于线性表。但与数组相比，它采用链式存储，因此有效解决了顺序表的两个核心问题：

1.  **空间限制**：数组必须预先定义大小，空间满后无法自动扩展（静态数组）。
2.  **内存浪费**：数组预留过多空间会造成浪费，且需要连续的内存空间。

## 单向链表原理

单向链表（Singly Linked List）是链表结构中最基本、也是最常用的一种形式。其核心特点在于：每个结点仅包含一个指向 **后继结点** 的指针，从而在物理结构上形成一条以头结点为起点、按顺序向后延伸的线性链式存储路径。受限于这种单向链接特性，链表中的数据访问只能沿着从头到尾的方向依次进行，无法通过指针直接回溯。

这种结构的优势在于设计简单、插入和删除操作对局部修改友好，不需要像顺序存储那样移动大量元素，因此在需要频繁调整结点位置的场景中具有一定的性能优势。然而，单向链表也存在明显局限：由于无法直接访问前驱结点，执行反向遍历、按位置删除指定结点或在任意位置插入需要前驱信息的操作时，往往必须从头结点开始顺序查找，从而在时间复杂度上产生额外消耗。

总体而言，单向链表以其结构简洁、操作灵活的特点成为链表体系的基础形态，但其单向链接带来的限制也决定了它在某些应用场景中不如双向链表等更复杂的结构高效。

### 单向链表的创建

对于单向链表（Singly Linked List），我们可以将整个结构想象为一列沿固定方向连接的车厢。每个节点包含两部分：一部分存放实际数据，就像车厢里承载的货物；另一部分是指向下一个节点的指针，好比车厢之间的车钩，使链表能够沿同一方向不断延伸。正是这种设计，使单向链表在内存中能够灵活地进行动态存储与扩展。

![单向链表图像](src/content/posts/linked-list/单向链表1.png)

链表节点在代码中的定义通常如下所示，采用 **结构体（struct）** 来表示节点，将 **数据域** 和 **指针域** 统一封装在同一个类型中。这种设计不仅便于在程序运行时按需创建节点，还可以灵活地将多个节点通过指针连接起来，形成链表的整体结构。

```c showLineNumbers
typedef int Elemtype; // 定义数据类型

typedef struct Node {
    Elemtype data;     // 数据域
    struct Node *next; // 指针域：指向下一个结点
} Linklist;
```

**关于头结点（Head Node）**

在实际工程和教学实现中，链表通常会在最前方设置一个 **哨兵结点（Sentinel Node）**，也称 **头结点** 。头结点本身不存储有效数据，但它在链表结构中起到了 “占位符” 和统一入口的作用，能够显著简化链表的各种操作。

例如，在插入或删除节点时，无需单独判断链表是否为空，也不必考虑操作节点是否位于首元位置，从而减少了边界条件处理的复杂性。头结点始终固定在链表起始位置，为链表的动态扩展和维护提供了统一的参照，使程序逻辑更加简洁和安全。

*   **头结点（Head Node）**：不含有效数据，仅作为链表的统一入口。
*   **首元结点（First Node）**：链表中第一个真正存放数据的结点。

如下图所示，你可以把头结点理解为整列火车的 “车头” ，负责牵引后续载货的车厢：

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

单向链表的构建方式主要包括 **头插法** 和 **尾插法** 。如果希望链表中结点的排列顺序与输入顺序保持一致，更常用、更直观的选择就是 **尾插法** 。该方法通过维护一个始终指向当前尾结点的指针，将新结点依次追加到链表末端，从而逐步构造出完整的链表，同时保持输入顺序的直观性和操作逻辑的简洁性。

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

**头插法（Head Insertion）** 是一种将新结点直接插入到链表头部的方法。具体来说，每次插入操作都是将新结点放置在头结点之后的位置，也就是链表的最前端。由于链表的头结点作为整个链表的统一入口，头插法在插入新结点时只需要修改两个指针：一个指向新结点的 `next` 指针指向原本的首元结点，另一个将头结点的 `next` 指针指向新结点。这种操作不依赖链表的长度，也不需要遍历已有结点，因此时间复杂度始终为 $O(1)$ 。正因为这一特性，头插法非常适合于需要快速构建链表或者在链表表头频繁添加数据的场景，例如在栈的底层实现中或在需要高效前端插入的动态数据结构中。

然而，头插法的结构特点也带来了一定的局限性：每次新插入的元素都会被放在链表的首元位置，从而改变了元素的原始输入顺序。换句话说，链表中元素的排列顺序与其插入的顺序完全相反，最终形成典型的逆序结构。如果应用场景要求保留输入顺序，则头插法可能并不合适，通常需要采用尾插法来保持顺序。此外，头插法在链表操作中的灵活性也体现在其与其他操作的组合使用上。例如，可以在链表初始化时快速批量插入数据，或者在处理需要实时更新前端元素的算法时，通过头插法可以快速更新链表头部而不影响已有元素的访问效率。

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

**尾插法（Tail Insertion）** 是一种将新结点追加到链表末端的方法，即每次插入操作都会将新结点放在原有尾结点之后，使其成为新的尾结点。与头插法不同，尾插法能够完整保留数据的原始输入顺序，因此在需要构建逻辑顺序与输入一致的链表时被广泛使用，例如在队列的底层实现中或处理按时间顺序记录的数据时。

如果链表内部没有维护尾指针，每次进行尾插操作时都必须从头结点开始，顺序遍历整个链表直到末端，才能将新结点链接到最后一个结点之后。这种情况下，每次插入操作的时间复杂度为 $O(n)$ ，其中 $n$ 是链表当前的长度，随着链表长度增加，插入操作的耗时也会增加。为了优化效率，通常会在链表中维护一个尾指针，直接指向当前尾结点。这样，每次插入新结点时只需修改尾指针和新结点的 `next` 指针即可完成操作，使得时间复杂度降为 $O(1)$ ，大大提高了插入效率。

尾插法不仅保留数据顺序，也符合人们对 “向列表末尾追加数据” 的直观理解，因此在实际工程代码中使用非常普遍。尤其在需要按自然顺序构建数据结构的场景下，例如顺序记录日志、事件队列、消息缓冲区等，尾插法的使用可以保证链表中数据顺序与输入顺序一致，便于后续访问、遍历和处理。此外，尾插法与头插法结合使用，例如先在头部插入临时数据，再在尾部追加顺序数据，从而满足不同的业务逻辑需求。

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

当需要在单向链表中的特定逻辑位置插入一个新的元素时，通常采用 **按位置插入** 的方法，这种方法不仅能够在链表的任意合法位置灵活插入新结点，而且可以确保链表中已有元素的逻辑顺序保持不变，从而便于动态调整链表结构和实现更复杂的数据操作。

假设要在第 $k$ 个数据结点（不包括头结点）之前插入一个新结点，首先必须通过遍历链表找到第 $k-1$ 个结点，也就是目标位置的前驱结点。遍历过程中，如果发现前驱结点不存在（例如 $k$ 超出了链表当前长度），则无法完成插入操作，需要进行异常处理或报错。这个定位过程的时间复杂度为 $O(k)$，因为必须从头结点开始逐个访问，直到到达前驱结点。

完成前驱结点定位后，插入过程本质上是一次局部的指针调整：新结点的 `next` 指针指向目标位置原有的结点，而前驱结点的 `next` 指针则指向新结点。通过这种方式，新结点被顺利嵌入链表中，原有结点的链接关系保持不变，逻辑顺序得以完整保留，同时链表结构也保持一致性和可操作性。

指定位置插入具有以下特点和注意事项：

1. **灵活性高**：可以在链表任意合法位置插入结点，而不仅限于表头或表尾。
2. **顺序保持**：通过正确调整前驱结点和新结点的指针，可以保证链表中元素的逻辑顺序不被打乱。
3. **边界处理**：在插入链表首尾结点前需要做特殊处理，以防出现空指针或越界访问。
4. **时间复杂度**：由于需要遍历到前驱结点，操作的时间复杂度为 $O(k)$ ，因此在长链表中效率较低。

这种按位置插入的方法在实际应用中非常常见，不仅适用于按优先级排序的任务队列或事件队列中插入任务，而且在动态维护和更新链表数据结构、调整元素顺序或实现复杂链表操作时，都可以采用该方法实现既高效又安全的插入操作，从而确保链表的逻辑结构始终符合预期要求。

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

在单向链表中，**遍历操作** 是指沿着结点的 `next` 指针方向，从首元结点开始，依次访问链表中的每一个结点，直到遇到 `NULL` 指针为止。由于链表的物理存储是离散的，每个结点在内存中可能不连续，结点之间通过指针相互连接，因此遍历操作是理解链表结构和进行各种链表操作的基础和前提。通过遍历，我们可以访问或处理链表中的每一个元素，例如打印数据、统计结点数量或进行查找和更新操作。

在执行遍历时，通常需要先判断链表是否为空。若首元结点不存在，则说明链表中没有有效数据，遍历操作无法继续进行，此时应及时提示或返回异常信息，避免空指针操作导致程序出错。在链表非空的情况下，遍历过程只需不断将指针移动到当前结点的 `next` 指向的下一个结点，这就像依次 “走过每节车厢” ，访问每一个结点中存储的数据，直至遇到 `NULL` 结束标志。

遍历操作的时间复杂度为 $O(n)$ ，因为每个结点都必须被访问一次才能完成整个链表的遍历。这种线性时间特性使得遍历操作在链表中的效率与链表长度直接相关，对于较长链表，遍历可能耗费较多时间，但这是访问链表中所有元素不可避免的代价。同时遍历还为插入、删除、查找等链表操作提供了必需的前提条件，是理解和操作链表不可或缺的一环。

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

在单向链表中，**删除第 $k$ 个结点** 的核心在于正确找到其前驱结点，即第 $k-1$ 个结点。由于单向链表每个结点只包含指向后继结点的指针，无法直接通过待删除结点找到其前驱，因此删除操作通常需要从头结点开始，逐个访问每个结点，通过指针跳转一步步定位到前驱结点的位置。在这一过程中，如果发现链表为空，或者 $k$ 的值超出了链表长度，则删除操作无法继续，应及时提示错误或返回异常状态，防止空指针访问或越界操作。

一旦定位到前驱结点，删除操作的关键步骤是进行 **局部的指针调整**：将前驱结点的 `next` 指针直接指向待删除结点的后继结点，从而将第 $k$ 个结点从链条中 “绕开” ，逻辑上将其从链表中移除。被绕开的结点所占的内存空间仍然存在，若使用动态内存分配（如 C 语言中的 `malloc` 或 `new`），则必须显式释放该结点的内存，否则会导致内存泄漏。在删除首元结点时，需要特别处理头结点的指针更新；在删除尾结点时，也应注意将新的尾结点的 `next` 指针设置为 `NULL` 。

整体而言，单向链表的删除操作本质上是一次 **查找加局部重连** 的过程，时间复杂度为 $O(n)$ ，主要开销来自于遍历链表以查找前驱结点。尽管删除本身只涉及指针的局部调整，但为了保证链表结构的完整性和数据安全，需要额外注意边界条件、异常处理以及内存释放问题。通过正确的操作，删除结点可以实现链表的动态维护，使链表在插入、删除和查找等操作下保持稳定且高效的结构。

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

## 完整代码实现

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

## 双向链表原理

双向链表（Doubly Linked List），又称双链表，是线性链式结构的一种重要变体。在双向链表中，每个结点除了存储数据元素外，还包含两个指针域：一个指向其直接前驱结点 `prior` ，另一个指向其直接后继结点 `next` 。这种设计使得链表不仅能从头结点沿 `next` 指针依次向后访问，也可以通过 `prior` 指针从任意结点向前回溯，从而实现双向遍历的能力。这一点与单向链表明显不同，单向链表只能沿着后继方向逐步推进，无法直接访问前驱结点。

双向链表的这种双向连接特性带来了多个实际优势。首先，在需要频繁访问或修改某个结点的前驱或后继时，双向链表无需像单向链表那样从头开始逐个查找前驱，能够直接通过 `prior` 指针获取前驱结点，从而将原本 $O(n)$ 的查找操作降低到 $O(1)$ 。其次，在执行插入和删除操作时，双向链表可以直接修改相关结点的前驱和后继指针即可完成操作，无需遍历整个链表寻找前驱结点，这使得局部操作更加高效和灵活。

此外，双向链表的结构虽然比单向链表稍复杂，需要额外维护前驱指针，但它在 **操作效率、灵活性和双向可达性** 上明显优于单向链表。通过合理使用双向链表，可以在保证链表逻辑结构完整性的同时，实现更高效的数据操作和更丰富的应用场景。

### 双向链表的创建

在构建双向链表时，依旧遵循链式结构 “动态生成、逐结点连接” 的基本原则。双向链表的每个结点除了存储数据外，还包含两个指针域：`prior` 指向前驱结点，`next` 指向后继结点。这种双向指针结构要求在创建链表时，既要正确建立每个结点与其前驱结点的联系，又要保证后继指针的连续性，以确保链表双向都可以正常遍历。

本实验示例采用 **不带头结点** 的实现方式，即链表的第一个结点直接用于存储输入数据，而不设置一个空的头结点作为占位。这一点与单向链表实现略有不同，因此在初始化第一个结点时，必须同时处理其前驱与后继指针：`prior` 指向 `NULL`，`next` 初始也指向 `NULL`。如果忽略这一步，后续结点的连接将可能出现错误，导致链表结构不完整或遍历异常。

在具体构建过程中，通常采用 **尾插法** 逐步扩展链表。尾插法的核心思想是每次将新结点追加到链表末尾，使其成为新的尾结点。与单向链表相比，双向链表的尾插法需要额外维护前驱指针：当创建新结点时，首先将当前尾结点的 `next` 指向新结点，然后将新结点的 `prior` 指向旧尾结点，最后更新尾指针使其指向新结点。这样，每插入一个结点，链表在前后方向上的连接关系都得到完整维护。

在操作过程中需要特别注意以下几点：

1. **首结点初始化**：创建第一个结点时，`prior` 和 `next` 均指向 `NULL`，保证链表起点正确。
2. **尾结点更新**：插入新结点后及时更新尾指针，确保能继续追加结点。
3. **双向指针维护**：新结点的 `prior` 指向旧尾结点，旧尾结点的 `next` 指向新结点，保证双向结构完整。
4. **动态生成结点**：每次插入新结点都动态分配内存，保证链表长度灵活可变。

通过上述方法，随着数据逐一插入，双向链表在逻辑上形成一条完整的双向链路。完成构建后，链表不仅能够从头到尾正向遍历，还可以从尾到头逆向访问，为后续的插入、删除和查找操作提供了高效的基础。

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

在双向链表中进行插入操作时，相比单向链表需要处理的指针更多，因为每个结点都保存着前驱 `prior` 和后继 `next` 指针。无论插入位置位于链表的开头、末尾还是中间，都必须确保四条指针关系被正确更新：新结点的 `prior` 和 `next`，以及相邻结点的 `next` 和 `prior`。正确维护这些指针关系能够保证链表在双向上始终连通，避免出现断链或指针混乱的情况。

**头插法（插入到链表首部）**

当新结点需要成为链表的新首元结点时，应先将新结点的 `next` 指向原来的首结点，同时将原首结点的 `prior` 指向新结点。完成上述操作后，再更新链表的头指针指向新结点，使其成为新的首结点。该方法操作简单，时间复杂度为 $O(1)$ ，特别适合频繁在链表头部插入数据的场景。

> 头插法图解

![双向链表图像](src/content/posts/linked-list/双向链表3.png)

![双向链表图像](src/content/posts/linked-list/双向链表4.png)

**尾插法（插入到链表尾部）**

当新结点需要插入到链表尾部时，应将当前尾结点的 `next` 指向新结点，同时将新结点的 `prior` 指向原尾结点。如果程序中维护了尾指针，还应同步更新尾指针指向新结点，以保证链表的尾部状态始终正确。尾插法能够保持数据的输入顺序，与尾部追加的逻辑相符，非常适合用于顺序构建链表。

> 尾插法图解

![双向链表图像](src/content/posts/linked-list/双向链表7.png)

![双向链表图像](src/content/posts/linked-list/双向链表8.png)

**指定位置插入（链表中间位置）**

在链表中间位置插入新结点时，需要同时处理新结点与前驱、后继的连接关系，确保双向链表的完整性。假设要在结点 `p` 之后插入新结点 `node`，操作顺序如下：

1. `node->next = p->next` —— 新结点的 `next` 指向 `p` 的后继结点。
2. `node->prior = p` —— 新结点的 `prior` 指向 `p`。
3. `p->next->prior = node` —— 若 `p` 的后继结点存在，将其 `prior` 指向新结点。
4. `p->next = node` —— 将 `p` 的 `next` 指向新结点。

通过这四步操作，新结点即可正确插入链表的中间位置，同时保持双向链表的完整性和逻辑顺序不变。这种插入方式在按优先级或逻辑顺序维护链表时非常常用，也为后续的删除、遍历等操作提供了可靠的指针结构保证。

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

在双向链表中删除结点比单向链表更加高效，因为每个结点不仅有指向后继的 `next` 指针，还保存前驱指针 `prior` ，可以直接访问目标结点的前驱，无需像单向链表那样从头遍历查找前驱，显著减少操作开销。删除操作的核心是将目标结点从链表中移除，同时保持链表中其他结点的双向连接不受影响，并安全释放内存。

删除操作的基本步骤如下：首先定位要删除的结点 `p`，然后调整其前驱和后继结点的指针，使前驱结点的 `next` 指向 `p` 的后继结点，后继结点的 `prior` 指向 `p` 的前驱结点，从而将 `p` 从链表中 “断开” 。随后释放 `p` 所占用的内存，以避免内存泄漏。核心指针调整逻辑如下：

```c showLineNumbers
p->prior->next = p->next;
p->next->prior = p->prior;
```

在实际实现中，还需处理一些特殊情况：

1. **删除首结点**：若 `p` 为链表首结点，则需更新头指针指向 `p->next` ，并将新头结点的 `prior` 置为 `NULL` 。
2. **删除尾结点**：若 `p` 为尾结点，则需更新尾指针指向 `p->prior` ，并将新尾结点的 `next` 置为 `NULL` 。
3. **特殊情况判断**：删除前应检查链表是否为空，或链表中是否仅有一个结点，以防止空指针异常。

通过这些操作，双向链表可以在 $O(1)$ 时间内完成局部结点的删除，同时保证链表的结构完整性和双向可达性。这种高效且灵活的删除特性，使双向链表在需要频繁插入和删除操作的应用中非常实用，例如任务队列管理、浏览器历史记录维护以及各种动态数据结构的管理。

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

## 完整代码实现

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