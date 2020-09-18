# 

# 前言

本文总结electron、vue、elementui开发中的常见问题。

## 工具链说明

| 工具      | 文档                             | 版本    | 安装方式         |
| --------- | -------------------------------- | ------- | ---------------- |
| Node      | https://nodejs.org/zh-cn/docs/   | 12.16.1 | 下载二进制包安装 |
| electron  | https://www.electronjs.org/docs  | 8.11    | 通过npm下载      |
| vue       | https://cn.vuejs.org/v2/guide/   | 2.6     | cdn引入          |
| elementui | https://element.eleme.cn/#/zh-CN |         | cdn引入          |

## 为什么使用electron
* 优点：跨平台，技术有前景，轻量。
* 缺点：
  * 发布包很大：由于是桌面应用，所以对发布包大小不是特别敏感
  * UI响应不如native应用迅速：但在可接受范围内
  * 需要有前端开发经验。

## 为什么使用vue
前端开发有两种方式：

* 一种是不使用任何框架，纯html+css+js开发。这种方式方式太原始，并且较少社区资源支持。
* 另一种是选择一种前端框架，如react、vue等。我们选择的是vue。

vue的优点
* 响应式：数据值改变，自动同步到界面元素。
* html逻辑：在html里直接写简单的显示逻辑，不用再拼html字符串。

## 为什么使用elementui
elementui是基于vue开发的一套桌面风格的UI库。
优点：使用简单，界面美观。

# electron

开发electron项目，就像是开发浏览器，有两部分：

* html展示：通过编写html页面实现功能。
  * 每个html页面都运行在一个独立的渲染进程里。
  * 工作内容为操作vue相关的API。
* 其他部分：
  * 桌面应用UI部分：包括标题栏、菜单栏，工具栏等。通过操作electron的API实现。
  * 与html页面进行数据交换等操作。通过electron中的ipc接口实现。
  * 运行在唯一的主进程里。

**新建项目**

1. 下载模板文件：<a href="/工具研究/electron/myapp.zip" download="myapp.zip">myapp</a>
2. 修改文件夹名字`myapp`、`package.json`中的`name`字段为新项目的名字
3. 执行`npm install`或`cnpm install`下载依赖文件
4. 执行`npm start`运行项目

# vue

> vue的核心有两点：
>
> 1. 在网页开发中，引入了响应式编程的思想。
> 2. 支持使用模板语法来编写网页界面。

> 响应式编程出现之前，如果网页的内容、元素、布局要改变，都是由一段程序重新生成网页再渲染的。而响应式的思想在于，网页的元素本身(例如div、input等)的属性(例如可见性、颜色等)，可以绑定到一个变量，当此变量发生变化时，网页元素可以自动做出相应的改变。
>
> 这样就减少了大量网页显示方面的代码调用。
>
> 为此，vue在其内部维护了一个虚拟DOM树，开发人员可以将自定义的变量绑定到这棵树的节点上，当这些变量改变时，虚拟节点会自动做出做出响应。

> 使用模板语法来设计网页是一种很常见的做法，过程为**某段网页生成代码**读取**模板文件**，将模板文件渲染成最终的网页文件，喂给浏览器显示。每个项目几乎都要重复开发这一过程。vue将这个过程封装，并且支持直接在html中写模板语言。使得项目开发可以直接使用这一套机制，不必重复开发。
>

## 安装

完整的安装教程在：https://cn.vuejs.org/v2/guide/installation.html

可以使用简单的cdn引入：

```html
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
```

或者指定版本：

```html
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.11"></script>
```

## 编码过程

**1.创建vue实例并设置绑定**

```html
<script>
var app = new Vue({
    el: '#app',
    data: {
      message: 'Hello Vue!'
    }
})
</script>

<!--可以直接在html中访问绑定的变量-->
<div id="app">{{ message }}</div>
```

**2.编写vue指令，来控制网页元素的attribute**

| 举例                                     | 作用                                     |
| ---------------------------------------- | ---------------------------------------- |
| `<p v-if="seen">现在你看到我了</p>`      | p是否显示，决定于seen的真假              |
| `<p v-for="todo in todos">{{todo}}</p>`  | 利用循环显示todos列表的每一项            |
| `<button v-on:click="reverse"></button>` | 点击按钮时，触发在vue中注册的reverse方法 |
| `<input v-model="message">`              | 用户输入的数据等价于message变量          |
| `<span v-bind:title="message"></span>`   | 现在span.title会与message保持一致        |

**3.使用组件机制，来模块化界面设计**

创建模块：

```vue
Vue.component('todo-item', {
      props: ['todo'],
      template: '<li>{{ todo.text }}</li>'
})

var app = new Vue(...);
```

使用模块：

```html
<todo-item 
           v-for="item in groceryList" 
           v-bind:todo="item" 
           v-bind:key="item.id"
></todo-item>
```

## vue实例

```js
var app = new Vue({
    el: '#app',
    
    data: {
        message: 'Hello Vue!'
    },

    methods: {
      getAnswer: function () {
        return this._answer;
      }
    },
    
    computed: {
      now: function () {
        return Date.now();
      },

      fullName: {
        get: function () {
          return this._fullName;
        },
        set: function (value) {
          this._fullName = value;
        }
      }
    },

    created: function () {
    },
    
    watch: {
      question: function (newValue, oldValue) {
      }
    },
});
```

## 指令-条件渲染

```vue
<div v-if="type === 'A'">
  A
</div>
<div v-else-if="type === 'B'">
  B
</div>
<div v-else-if="type === 'C'">
  C
</div>
<div v-else>
  Not A/B/C
</div>
```

## 指令-循环渲染

极简形式

```vue
<ul id="example-2">
  <li v-for="item in items">
      {{ item }}
  </li>
</ul>
```

完全体遍历数组

```vue
<ul id="example-2">
  <li v-for="(item, index) in items">
    {{ parentMessage }} - {{ index }} - {{ item.message }}
  </li>
</ul>
```

完全体遍历对象

```vue
<ul id="example-2">
  <li v-for="(value, key) in obj">
    {{ parentMessage }} - {{ key }} - {{ value }}
  </li>
</ul>
```

直接循环n次

```vue
<div>
  <span v-for="n in 10">{{ n }} </span>
</div>
```

结合`v-if`使用

```vue
<li v-for="todo in todos" v-if="!todo.isComplete">
  {{ todo }}
</li>
```

## 指令-输入绑定

v-model用于在类input元素，与程序变量之间，做绑定。

### 绑定单个值

| 元素类型   | html                                                | 变量类型 |
| ---------- | --------------------------------------------------- | -------- |
| 单行输入   | `<input/>`                                          | string   |
| 多行输入   | `<textarea/>`                                       | string   |
| 单个复选框 | `<input type="checkbox"/>`                          | bool     |
| 单选按钮   | `<input type="radio" value="One" v-model="picked">` | string   |

### 绑定多个checkbox的值

```vue
<input type="checkbox" id="jack" value="Jack" v-model="checkedNames">
<label for="jack">Jack</label>
<input type="checkbox" id="john" value="John" v-model="checkedNames">
<label for="john">John</label>
<input type="checkbox" id="mike" value="Mike" v-model="checkedNames">
<label for="mike">Mike</label>
```

此时`checkedNames`是["Jack", "John", "Mike"]的数组。

不要混用这种多个值和上面单个值的情况。

### 绑定单选下拉列表

```vue
<select v-model="selected">
    <option disabled value="">请选择</option>
    <option>A</option>
    <option>B</option>
    <option>C</option>
</select>
```

此时`selected`类型为`string`

绑定多选下拉列表

```vue
<select v-model="selected" multiple >
    <option>A</option>
    <option>B</option>
    <option>C</option>
</select>
```

此时`selected`类型为["A","B","C"]。

### 对绑定变量做预处理

|                      |                                              |
| -------------------- | -------------------------------------------- |
| 将变量转换为数字类型 | `<input type="number" v-model.number="age">` |
| 去掉输入框首尾的空格 | `<input v-model.trim="msg">`                 |

## 指令-处理事件

```vue
<button v-on:click="someMethod"></button>
```

```vue
<button @click="someMethod"></button>
```

```vue
<button @click="someMethod($event)"></button>
```

### 事件修饰符

使用事件修饰符来自动调用某些常用的事件处理方法

```vue
<a v-on:click.stop="someMethod"></a>
```

等价于执行：

```vue
<a v-on:click="$event.stop(); someMethod()"></a>
```

可用的事件修饰符

| 修饰符类型 | 作用                                                         |
| ---------- | ------------------------------------------------------------ |
| .stop      | 阻止事件继续传播                                             |
| .prevent   | 提交事件不再重载页面                                         |
| .capture   | 内部元素触发的事件先在此处理，然后才交由产生事件的内部元素进行处理 |
| .self      | 只有事件是由本元素产生时，才调用此处理方法                   |
| .once      | 事件将只会触发一次                                           |
| .passive   | 事件的默认行为会立即触发，而不是等待someMethod调用完才触发。<br />例如滚动事件发生时，不会等待someMethod执行完才真的进行滚动，而是同时进行的 |

### 按键修饰符

只有在按键是`enter`时才触发`someMethod`

```vue
<input v-on:keyup.enter="someMethod">
```

只有在按键是`page-down`时才触发`someMethod`

```vue
<input v-on:keyup.page-down="someMethod">
```

# 文件拖拽

```html
<div @dragover.prevent @drop.prevent="onFileDrop($event.dataTransfer)"></div>

<script>
  function onFileDrop(dataTransfer){
    //获取拖拽的文件
    dataTransfer.files;

    //从文件中读取数据
    let reader = new FileReader();
    reader.onload = function(e){
        reader.result;
    }.bind(this);
    reader.readAsDataURL(dataTransfer.files[i]);

  	//读取文本数据
    dataTransfer.getData("text/plain");
    dataTransfer.getData("text/uri-list");
}
</script>
```



