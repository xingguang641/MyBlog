---
title: 【博客指南】Expressive-Code示例
published: 2024-05-01
description: 演示如何在 Markdown 中使用丰富代码功能
tags: [Markdown, Blogging, Demo]
category: Blog Guides
draft: false
---

> 写在前面：本文将展示基于 [Expressive Code](https://expressive-code.com/) 构建的增强型代码块显示效果

## 核心语法功能演示

### 1. 语法高亮功能

[📚 官方文档：语法高亮](https://expressive-code.com/key-features/syntax-highlighting/)

#### 常规语法高亮
支持主流编程语言的自动着色。

```js
console.log('This code is syntax highlighted!')
```

#### 渲染 ANSI 转义序列
可以直接渲染终端输出中的 ANSI 颜色代码，非常适合展示 CLI 工具的输出结果。

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

### 2. 终端样式功能

[📚 官方文档：窗口框架](https://expressive-code.com/key-features/frames/)

#### 代码编辑器样式
模拟 IDE 窗口，支持显示文件名或完整路径。

```js title="my-test-file.js"
console.log('Title attribute example')
```

```html
<!-- src/content/index.html -->
<div>File name comment example</div>
```

#### 终端窗口样式
模拟命令行终端外观。

```bash
echo "This terminal frame has no title"
```

```powershell title="PowerShell 终端示例"
Write-Output "This one has a title!"
```

#### 自定义窗口类型
你可以强制指定使用某种外框，或者完全移除外框。

```sh frame="none"
echo "Look ma, no frame! (无边框模式)"
```

```ps frame="code" title="PowerShell Profile.ps1"
# 强制使用代码编辑器样式，而非默认的终端样式
function Watch-Tail { Get-Content -Tail 20 -Wait $args }
New-Alias tail Watch-Tail
```

### 3. 文本标记功能

[📚 官方文档：文本标记](https://expressive-code.com/key-features/text-markers/)

#### 标记整行与多行
通过行号或范围（如 `7-8` ）来高亮特定代码行。

```js {1, 4, 7-8}
// Line 1 - 通过行号 {1} 选中
// Line 2
// Line 3
// Line 4 - 通过行号 {4} 选中
// Line 5
// Line 6
// Line 7 - 通过范围 {7-8} 选中
// Line 8 - 通过范围 {7-8} 选中
```

#### 指定标记类型（高亮、新增、删除）
除了默认的高亮，还支持 `ins`（新增/绿色）和 `del`（删除/红色）样式。

```js title="line-markers.js" del={2} ins={3-4} {6}
function demo() {
  console.log('这一行被标记为删除 (del)')
  // 下面两行被标记为新增 (ins)
  console.log('this is the second inserted line')

  return '这一行使用默认的中性标记 (mark)'
}
```

#### 带标签的行标记
可以在高亮行的右侧添加文本标签，用于解释代码逻辑。

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

#### 长标签文本布局
当标签文本较长时，会自动调整布局以保持美观。

```jsx {"1. 在此处传入 value 属性:":5-6} del={"2. 移除 disabled 和 active 状态:":8-10} ins={"3. 添加此逻辑以渲染按钮内部的子元素:":12-15}
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

#### Diff 语法支持
直接支持标准的 diff 格式。

```diff
+这一行将被标记为新增
-这一行将被标记为删除
这是一个普通行
```

```diff
--- a/README.md
+++ b/README.md
@@ -1,3 +1,4 @@
+this is an actual diff file
-all contents will remain unmodified
 no whitespace will be removed either
```

#### 混合使用 Diff 与语法高亮
你可以在保留 JavaScript 等语言高亮的同时，使用 diff 标记。

```diff lang="js"
  function thisIsJavaScript() {
    // 整个代码块将被高亮显示为 JavaScript
    // 同时我们仍然可以使用 diff 符号
-   console.log('Old code to be removed')
+   console.log('New and shiny code!')
  }
```

#### 行内文本高亮
不标记整行，而是通过字符串匹配高亮行内的特定文本。

```js "given text"
function demo() {
  // Mark any given text inside lines
  return 'Multiple matches of the given text are supported';
}
```

#### 正则表达式匹配
支持使用正则进行灵活的文本匹配。

```ts /ye[sp]/
console.log('The words yes and yep will be marked.')
```

#### 转义处理
在正则模式中匹配正斜杠。

```sh /\/ho.*\//
echo "Test" > /home/test.txt
```

#### 自定义行内标记样式
行内文本同样支持 `ins` 和 `del` 样式。

```js "return true;" ins="inserted" del="deleted"
function demo() {
  console.log('These are inserted and deleted marker types');
  // return 语句使用默认的标记类型
  return true;
}
```

### 4. 自动换行功能

[📚 官方文档：自动换行](https://expressive-code.com/key-features/word-wrap/)

#### 开启与关闭
控制长代码行是否自动换行。

```js wrap
// 开启自动换行 (wrap)
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

```js wrap=false
// 关闭自动换行 (wrap=false)
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

#### 智能缩进保留
开启换行时，是否保留第二行的缩进对齐。

```js wrap preserveIndent
// 开启缩进保留 (默认行为)
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

```js wrap preserveIndent=false
// 关闭缩进保留 (文字将顶格换行)
function getLongString() {
  return 'This is a very long string that will most probably not fit into the available space unless the container is extremely wide'
}
```

## 插件语法功能演示

### 1. 代码折叠功能

[📚 官方文档：代码折叠](https://expressive-code.com/plugins/collapsible-sections/)

支持将不重要的样板代码（Boilerplate）折叠隐藏，点击即可展开。

```js collapse={1-5, 12-14, 21-24}
// 这部分样板代码默认会被折叠
import { someBoilerplateEngine } from '@example/some-boilerplate'
import { evenMoreBoilerplate } from '@example/even-more-boilerplate'

const engine = someBoilerplateEngine(evenMoreBoilerplate())

// 这部分代码默认可见
engine.doSomething(1, 2, 3, calcFn)

function calcFn() {
  // 这里也可以设置折叠区域
  const a = 1
  const b = 2
  const c = a + b

  // 这部分保持可见
  console.log(`Calculation result: ${a} + ${b} = ${c}`)
  return c
}

// 结尾的代码再次折叠
engine.closeConnection()
engine.freeMemory()
engine.shutdown({ reason: 'End of example boilerplate code' })
```

### 2. 代码行号功能

[📚 官方文档：行号显示](https://expressive-code.com/plugins/line-numbers/)

#### 控制行号显示

```js showLineNumbers
// 显式开启行号
console.log('Greetings from line 2!')
console.log('I am on line 3')
```

```js showLineNumbers=false
// 显式禁用行号
console.log('Hello?')
console.log('Sorry, do you know what line I am on?')
```

#### 自定义起始行号
在展示代码片段（而非完整文件）时非常有用。

```js showLineNumbers startLineNumber=5
console.log('Greetings from line 5!')
console.log('I am on line 6')
```