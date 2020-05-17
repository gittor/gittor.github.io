# 前言

对vue开发中最常用的部分做了总结，主要参考了官方文档。

官网文档：https://cn.vuejs.org/v2/guide/

# 核心

> vue的核心有两点：
>
> 1. 在网页开发中，引入了响应式编程的思想。
> 2. 支持使用模板语法来编写网页界面。

> 响应式编程出现之前，如果网页的内容、元素、布局要改变，都是由一段程序重新生成网页再渲染的。而响应式的思想在于，网页的元素本身(例如div、input等)的属性(例如可见性、颜色等)，可以绑定到一个变量，当此变量发生变化时，网页元素可以自动做出相应的改变。
>
> 这样就减少了大量网页显示方面的代码调用。
>
> 为此，vue在其内部维护了一个虚拟DOM树，开发人员可以将自定义的变量绑定到这棵树的节点上，当这些变量改变时，虚拟节点会自动做出做出响应。

> 使用模板语法来设计网页是一种很常见的做法，过程为**某段网页生成代码**读取**模板文件**，将模板文件渲染成最终的网页文件，喂给浏览器显示。每个项目几乎都要重复开发这一过程。
>
> vue将这个过程封装，并且支持直接在html中写模板语言。使得项目开发可以直接使用这一套机制，不必重复开发。

# 安装

完整的安装教程在https://cn.vuejs.org/v2/guide/installation.html

可以使用简单的cdn引入：

```html
<script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
```

或者指定版本：

```html
<script src="https://cdn.jsdelivr.net/npm/vue@2.6.11"></script>
```

# 组成部分

> 创建vue实例并设置绑定
>
> ```html
> <script>
>  var app = new Vue({
>    el: '#app',
>    data: {
>      message: 'Hello Vue!'
>    }
>  })
> </script>
> ```

> 可以直接在html中访问绑定的变量
>
> ```html
> <div id="app">
> {{ message }}
> </div>
> ```
>
> 这种语法不能修改html元素的attribute，只能修改text。


> 提供vue指令，来控制网页元素的attribute
> 
> | 举例                                     | 作用                                     |
> | ---------------------------------------- | ---------------------------------------- |
> | `<p v-if="seen">现在你看到我了</p>`      | p是否显示，决定于seen的真假              |
> | `<p v-for="todo in todos">{{todo}}</p>`  | 利用循环显示todos列表的每一项            |
> | `<button v-on:click="reverse"></button>` | 点击按钮时，触发在vue中注册的reverse方法 |
> | `<input v-model="message">`              | 用户输入的数据等价于message变量          |
> | `<span v-bind:title="message"></span>`   | 现在span.title会与message保持一致        |
> 


> 提供组件机制，来模块化界面设计
> 
> 创建模块：
> 
> ```vue
> Vue.component('todo-item', {
>       props: ['todo'],
>       template: '<li>{{ todo.text }}</li>'
> })
> 
> var app = new Vue(...);
> ```
> 
> 使用模块：
> 
> ```html
> <todo-item 
>            v-for="item in groceryList" 
>            v-bind:todo="item" 
>            v-bind:key="item.id"
> ></todo-item>
> ```

# vue实例

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

# 条件渲染

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

# 循环渲染

v-for中的`in`，语义上和js中的`of`相同

> 极简形式
>
> ```vue
> <ul id="example-2">
>   <li v-for="item in items">
>       {{ item }}
>   </li>
> </ul>
> ```

> 完全体遍历数组
>
> ```vue
> <ul id="example-2">
>   <li v-for="(item, index) in items">
>     {{ parentMessage }} - {{ index }} - {{ item.message }}
>   </li>
> </ul>
> ```

> 完全体遍历对象
>
> ```vue
> <ul id="example-2">
>   <li v-for="(value, key) in obj">
>     {{ parentMessage }} - {{ key }} - {{ value }}
>   </li>
> </ul>
> ```

> 直接循环n次
>
> ```vue
> <div>
>   <span v-for="n in 10">{{ n }} </span>
> </div>
> ```

> 结合`v-if`使用
>
> ```vue
> <li v-for="todo in todos" v-if="!todo.isComplete">
>   {{ todo }}
> </li>
> ```

# 处理事件

> 极简体
>
> ```vue
> <button v-on:click="someMethod"></button>
> ```
>
> ```vue
> <button @click="someMethod"></button>
> ```
>
> ```vue
> <button @click="someMethod($event)"></button>
> ```

## 事件修饰符

> 使用事件修饰符来自动调用事件的处理方法
>
> ```vue
> <a v-on:click.stop="someMethod"></a>
> ```
>
> 等价于执行：
>
> ```vue
> <a v-on:click="$event.stop(); someMethod()"></a>
> ```

> 可用的事件修饰符
>
> | 修饰符类型 | 作用                                                         |
> | ---------- | ------------------------------------------------------------ |
> | .stop      | 阻止事件继续传播                                             |
> | .prevent   | 提交事件不再重载页面                                         |
> | .capture   | 内部元素触发的事件先在此处理，然后才交由内部元素进行处理     |
> | .self      | 只有事件是由本元素产生时，才调用此处理方法                   |
> | .once      | 事件将只会触发一次                                           |
> | .passive   | 事件的默认行为会立即触发，而不是等待someMethod调用完才触发。<br />例如滚动事件发生时，不会等待someMethod执行完才真的进行滚动，而是同时进行的 |
>
> 

## 按键修饰符

> 只有在按键是`enter`时才触发`someMethod`
>
> ```vue
> <input v-on:keyup.enter="someMethod">
> ```
>
> 只有在按键是`page-down`时才触发`someMethod`
>
> ```vue
> <input v-on:keyup.page-down="someMethod">
> ```

# v-model

v-model用于在支持用户输入的元素，与程序变量之间，做绑定。

| 元素类型   | html                                                | 变量类型 |
| ---------- | --------------------------------------------------- | -------- |
| 单行输入   | `<input/>`                                          | string   |
| 多行输入   | `<textarea/>`                                       | string   |
| 单个复选框 | `<input type="checkbox"/>`                          | bool     |
| 单选按钮   | `<input type="radio" value="One" v-model="picked">` | string   |

---

## 绑定多个checkbox的值

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

---

## 下拉列表

```vue
<select v-model="selected">
    <option disabled value="">请选择</option>
    <option>A</option>
    <option>B</option>
    <option>C</option>
</select>
```

此时`selected`类型为`string`

---

## 列表选择

```vue
<select v-model="selected" multiple >
    <option>A</option>
    <option>B</option>
    <option>C</option>
</select>
```

此时`selected`类型为["A","B","C"]。

## 将变量转换为数字类型

```vue
<input type="number" v-model.number="age">
```

## 去掉输入框首尾的空格

```vue
<input v-model.trim="msg">
```

