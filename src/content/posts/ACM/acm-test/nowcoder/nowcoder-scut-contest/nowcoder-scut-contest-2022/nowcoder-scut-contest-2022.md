---
title: 【ACM 算法比赛】华南理工 2022 程序设计竞赛
published: 2026-09-26
description: 记录一些 ACM 常规比赛
tags: [Algorithm, Contest, Nowcoder]
category: ACM Test
draft: false
---

# 重点题目详解

[这里是比赛链接](https://ac.nowcoder.com/acm/contest/49626)

## Problem A



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem F



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem B



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main(){
    int n; cin >> n;

    vector<ll> a(n);
    for (int i = 0; i < n; i++){
        cin >> a[i];
    }

    if (a[0] == 1 || n == 1){
        cout << "HowarLi" << endl;
        return 0;
    }

    for (int i = 0; i < n; i++){
        int cnt = 0;

        if (a[i] == 1){
            a[i] = 4;
            cnt = 1;
        }

        while (a[i] > 1){
            if (a[i] % 2){
                a[i] = a[i] * 3 + 1;
            }
            else{
                a[i] /= 2;
            }
            cnt++;
        }

        a[i] = cnt;
    }

    int mn = a[1];
    for (int i = 2; i < n; i++){
        mn = min(mn, (int)a[i]);
    }

    if (mn <= a[0]){
        cout << "Elo" << endl;
    }
    else{
        cout << "HowarLi" << endl;
    }
}
```

## Problem D



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem K



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem C



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem H



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```

## Problem G



## Solution



```cpp frame="code" title="main.cpp"
#include <bits/stdc++.h>
using namespace std;

int main(){

}
```