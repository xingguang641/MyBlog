---
title: 丰富代码示例
published: 2024-05-01
description: 使用丰富代码功能时，Markdown 中的代码块显示效果示例。
tags: [Markdown, Blogging, Demo]
category: Guides
draft: false
---

在这里，我们将展示使用 [Expressive Code](https://expressive-code.com/) 的显示效果。提供的示例基于官方文档，你可以参考官方文档获取更多详细信息。

## 丰富代码

### 高亮语法

[高亮语法](https://expressive-code.com/key-features/syntax-highlighting/)

#### 常规语法高亮

```js
console.log('This code is syntax highlighted!')
```

#### 渲染 ANSI 转义序列

```ansi
ANSI colors:
- Regular: [31mRed[0m [32mGreen[0m [33mYellow[0m [34mBlue[0m [35mMagenta[0m [36mCyan[0m
- Bold:    [1;31mRed[0m [1;32mGreen[0m [1;33mYellow[0m [1;34mBlue[0m [1;35mMagenta[0m [1;36mCyan[0m
- Dimmed:  [2;31mRed[0m [2;32mGreen[0m [2;33mYellow[0m [2;34mBlue[0m [2;35mMagenta[0m [2;36mCyan[0m

256 colors (showing colors 160-177):
[38;5;160m160 [38;5;161m161 [38;5;162m162 [38;5;163m163 [38;5;164m164 [38;5;165m165[0m
[38;5;166m166 [38;5;167m167 [38;5;168m168 [38;5;169m169 [38;5;170m170 [38;5;171m171[0m
[38;5;172m172 [38;5;173m173 [38;5;174m174 [38;5;175m175 [38;5;176m176 [38;5;177m177[0m

Full RGB colors:
[38;2;34;139;34mForestGreen - RGB(34, 139, 34)[0m

Text formatting: [1mBold[0m [2mDimmed[0m [3mItalic[0m [4mUnderline[0m
```

### 编辑器 & 终端框架

[编辑器 & 终端框架](https://expressive-code.com/key-features/frames/)

#### 代码编辑器框架

```js title="my-test-file.js"
console.log('Title attribute example')
```

---

```html
<!-- src/content/index.html -->
<div>File name comment example</div>
```

#### 终端框架

```bash
echo "This terminal frame has no title"
```

---

```powershell title="PowerShell 终端示例"
Write-Output "This one has a title!"
```

#### 显示框架类型

```sh frame="none"
echo "Look ma, no frame!"
```

---

```ps frame="code" title="PowerShell Profile.ps1"
# 如果不显示，这将是一个普通的终端框架。
function Watch-Tail { Get-Content -Tail 20 -Wait $args }
New-Alias tail Watch-Tail
```

### 文本 & 行标记

[文本 & 行标记](https://expressive-code.com/key-features/text-markers/)

#### 标记整行 & 行范围

```js {1, 4, 7-8}
// Line 1 - 通过行号定位
// Line 2
// Line 3
// Line 4 - 通过行号定位
// Line 5
// Line 6
// Line 7 - 通过范围 "7-8" 定位
// Line 8 - 通过范围 "7-8" 定位
```

#### 选择行标记类型（mark、ins、del）

```js title="line-markers.js" del={2} ins={3-4} {6}
function demo() {
  console.log('this line is marked as deleted')
  // 这一行及下一行被标记为新增。
  console.log('this is the second inserted line')

  return 'this line uses the neutral default marker type'
}
```

#### 为行标记添加标签

```jsx {"1":5} del={"2":7-8} ins={"3":10-12}
// labeled-line-markers.jsx
<button
  role="button"
  {...props}
  value={value}
  className={buttonClassName}
  disabled={disabled}
  active={active}
>
  {children &&
    !active &&
    (typeof children === 'string' ? <span>{children}</span> : children)}
</button>
```

#### 在单独的行上添加长标签

```jsx {"1. Provide the value prop here:":5-6} del={"2. Remove the disabled and active states:":8-10} ins={"3. Add this to render the children inside the button:":12-15}
// labeled-line-markers.jsx
<button
  role="button"
  {...props}

  value={value}
  className={buttonClassName}

  disabled={disabled}
  active={active}
>

  {children &&
    !active &&
    (typeof children === 'string' ? <span>{children}</span> : children)}
</button>
```

#### 使用类似 diff 的语法

```diff
+这一行将被标记为新增
-这一行将被标记为删除
这是一个普通行
```

---

```diff
--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
+this is an actual diff file
-all contents will remain unmodified
 no whitespace will be removed either
```

#### 将语法高亮与类似 diff 的语法结合使用

```diff lang="js"
  function thisIsJavaScript() {
    // 整个代码块将被高亮显示为 JavaScript
    // 并且我们仍然可以在其中添加 diff 标记
-   console.log('Old code to be removed')
+   console.log('New and shiny code!')
  }
```

#### 标记行内的单独文本

```js "given text"
function demo() {
  // Mark any given text inside lines
  return 'Multiple matches of the given text are supported';
}
```

#### 正则表达式

```ts /ye[sp]/
console.log('The words yes and yep will be marked.')
```

#### 转义正斜杠

```sh /\/ho.*\//
echo "Test" > /home/test.txt
```

#### 选择行内标记类型（mark、ins、del）

```js "return true;" ins="inserted" del="deleted"
function demo() {
  console.log('These are inserted and deleted marker types');
  // return 语句使用默认的标记类型
  return true;
}
```

### 自动换行

[自动换行](https://expressive-code.com/key-features/word-wrap/)

#### 为每个代码块配置自动换行

```js wrap
// 带自动换行的示例
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

---

```js wrap=false
// 关闭自动换行的示例
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

#### 配置自动换行功能的行缩进

```js wrap preserveIndent
// 启用 preserveIndent 的示例（默认开启）
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

---

```js wrap preserveIndent=false
// 禁用 preserveIndent 的示例
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

## 代码折叠语法

[代码折叠语法](https://expressive-code.com/plugins/collapsible-sections/)

```js collapse={1-5, 12-14, 21-24}
// 所有这些样板（boilerplate）设置代码将被折叠隐藏
import { someBoilerplateEngine } from '@example/some-boilerplate'
import { evenMoreBoilerplate } from '@example/even-more-boilerplate'

const engine = someBoilerplateEngine(evenMoreBoilerplate())

// 这部分代码默认会显示
engine.doSomething(1, 2, 3, calcFn)

function calcFn() {
  // 你可以设置多个折叠区域
  const a = 1
  const b = 2
  const c = a + b

  // 这部分将保持可见
  console.log(`Calculation result: ${a} + ${b} = ${c}`)
  return c
}

// 从这里开始到代码块结束的所有代码将再次被折叠
engine.closeConnection()
engine.freeMemory()
engine.shutdown({ reason: 'End of example boilerplate code' })
```

## 代码行编号

[代码行编号](https://expressive-code.com/plugins/line-numbers/)

### 按代码块显示行号

```js showLineNumbers
// 该代码块将显示行号
console.log('Greetings from line 2!')
console.log('I am on line 3')
```

---

```js showLineNumbers=false
// 该代码块已禁用行号
console.log('Hello?')
console.log('Sorry, do you know what line I am on?')
```

### 更改起始行号

```js showLineNumbers startLineNumber=5
console.log('Greetings from line 5!')
console.log('I am on line 6')
```
