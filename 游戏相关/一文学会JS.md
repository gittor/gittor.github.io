# 前言

本文主要来自于《你不知道的JavaScript》，分成几个角度总结了js开发中的方方面面。

* 易混淆主题：例如普通变量与作用域主题。分为原理(要记住)和自测(检验是否学会)两部分。
* 最佳实践：例如`如何`系列和`不要`系列。
* 重要API介绍。

# 普通变量与作用域

>  普通变量指的是不在类内部的变量及函数。

> 通用分析方法
>
> js代码的完整运行过程，分为编译阶段和运行阶段。

1. 编译阶段的主要工作是做提升。编译器会将变量声明和函数声明，提升到作用域开头。例如`var a=2;`会被分成`var a;`和`a=2;`两部分，而`var a;`部分会被提升到作用域开头，见自测1。有几个原则：
   1. 先提升函数声明，再提升变量声明。
   2. 遇到同名变量/函数，则使用先声明的，后声明的会被忽略。
   3. 遇到同名函数，则使用后定义的，后定义的覆盖先定义的。
   4. 删除不必要的作用域。在ES5及其之前，只有全局作用域，函数级作用域，表达式作用域，with作用域，没有块级作用域。
      1. 提升时使用的作用域，不是函数作用域就是全局作用域。
      2. 表达式作用域的唯一应用场景是在表达式内定义函数：`foo(function some(){console.log("in some");});`，此时some只能在some内部访问。
      3. ES6中的let，①支持将变量定义在块作用域中；②不会产生变量声明提升；③在`for(let i=0;i<10;++i)`中，每次循环都会创建一个新的循环变量`i`。
      4. ES6及其之后，还有文件作用域。也就是在文件中声明`var a=10;`，a并不属于全局对象。
2. 模拟运行得到结果。
   1. 确定是strict模式还是!strict模式。
      1. strict模式下，读取和赋值不存在的变量都会报错。
      2. !strict模式下，读取时找不到会报错，赋值时会在全局作用域创建一个变量。
   2. 需要明确变量查找规则，使用的是编译时作用域还是运行时作用域。
      1. 编译时作用域的上级作用域，是写代码定义时就可以看到的，不需要分析调用栈。
      2. 运行时作用域的上级作用域，等于调用它的运行栈，用于分析this的指向。

## 自测

```javascript
console.log(a); //undefined
var a = 2;

foo(); //可以正常执行，因为foo的声明被提升了。
function foo(){
    console.log("foo");
}

```

```js
function foo()
{
    {
        var a = 2;
    }
    console.log(a); //2。
}

foo();
```

```js
console.log(a); // ReferenceError。
```

# JS中的面向对象

> 导致js中面向对象与其他语言不同的根本，在于js中使用了原型链的方式来实现面向对象中的封装、继承、多态。

> 不同的语言实现面向对象的方式都不同。但在js中，支持三种方式。
>
> 一种是不使用原型链，而是将父类数据和函数复制到子类。
>
> 另一种是使用原型链，只通过prototype关联父子对象的形式。
>
> 第三种是使用ES6新增的class关键字，但底层使用的其实还是原型链。

## 不使用原型链实现

> 显式混合
>
> ```js
> function mixin(source, target) {
>     for(var key in source){
>         if(!(key in target)){
>             target[k] = source[k];
>         }
>     }
>     return target;
> }
> 
> var Vehicle = {
>     engines: 1,
>     drive: function(){
>         console.log("vehicle.drive:", this.engines);
>     }
> };
> 
> var Car = mixin(Vehicle, {
>     engines: 2,
>     drive: function(){
>         Vehicle.drive.call(this);
>         console.log("car.drive", this.engines);
>     }
> });
> ```
>
> Vechicle和Car实际都是对象，但在概念上将其看做类。
>
> 通过复制Vehicle和Car的方式创建实例。

> 寄生混合
>
> ```js
> function Vehicle() {
>     engines: 1
> }
> Vehicle.prototype.drive = function(){
>     console.log("Vehicle.drive:", this.engines);
> }
> 
> //寄生类
> function Car() {
>     var car = new Vehicle(); //先创建基类对象
> 
>     car.engines = 2; //进行差异化修改
> 
>     var basedrive = car.drive;
> 
>     car.drive = function() //进行差异化修改
>     {
>         basedrive.call(this);
>         console.log("Car.drive");
>     }
> 
>     return car;
> }
> 
> var car = new Car();
> car.drive();
> ```

> 隐式混合
>
> 与显式混合类似。
>
> ```js
> var Vehicle = {
>     init: function(){
>         this.engines = 1;
>     },
>     drive: function(){
>         console.log("vehicle.drive:", this.engines);
>     }
> };
> 
> var Car = {
>     init: function() {
>         Vehicle.init.call(this); //隐式混合
>         this.engines = 2;
>     },
>     drive: function(){
>         Vehicle.drive.call(this);
>         console.log("Car.drive");
>     }
> }
> 
> Car.init();
> Car.drive();
> ```

## 使用原型链实现

> Function有显式的prototype属性，可以直接访问。
>
> Object只有隐式的prototype属性，必须通过Object.getPrototypeOf(obj)访问。
>
> 使用原型链的实现方式也有几种。

> 通过`var obj = Object.create(proto);`实现。
>
> ```js
> var base = {
>     count: 1,
>     say: function(){
>         console.log(this.count);
>     }
> }
> var derived = Object.create(base);
> derived.say(); //1
> ```

> 通过`var obj = new Student();`实现。
>
> ```js
> function Base(){
>     this.count = 1;
> }
> Base.prototype.say = function(){
>     console.log(this.count);
> }
> 
> function Derived(){
>     Base.call(this);
>     this.count = 2;
> }
> Derived.prototype.say = function(){
>     console.log("Derived.say");
>     Base.prototype.say.call(this);
> }
> 
> var obj = new Derived();
> obj.say();
> //Derived.say
> //2
> ```
>
> 此时，obj.prototype === Derived.prototype。
>
> 

> 原型链中一个很关键的地方就是属性屏蔽，下层对象中的属性，会屏蔽上层对象的同名属性。
>
> 属性屏蔽有些时候会产生意想不到的问题。
>
> ```js
> var base = {
>     count: 1
> }
> var derived = Object.create(base);
> 
> derived.count++; //相当于derived.count=derived.count+1;，导致覆盖了base.count。
> 
> console.log(base.count); //1
> console.log(derived.count); //2
> ```
>
> 

## ES6中的做法

## new做了什么？

语法：`var obj = new Student()`。此时普通函数Student由于与new配合使用，常被称为构造函数。

new在工作时，一共做了4件事。

> ```js
> function Student() {
>     this.name = "zhang";
> }
> var obj = new Student();
> 
> //上面的代码，相当于执行
> function Student() {
>     var obj = Object.create(null); //1
>     Object.setPrototypeOf(obj, Student.prototype);//2
>     this = obj; //3
> 
>     this.name = "zhang";
> 
>     return obj; //4
> }
> var obj = Student();
> ```



## this指向何方

对于this，最重要的一个问题是如何判断this到底指向哪个对象。其他语言的this是在编译期做绑定的，js是在运行期做绑定的，所以会导致不同。

> ① `obj.fun();`的形式，this指向obj。

```js
function fun() {
    console.log(this.a);
}

var obj = {
    a: 2,
    fun: fun
}

obj.fun(); //2
```



> ② 通过某种绑定操作后调用，this指向绑定的对象。

```js
function fun() {
    console.log(this.a);
}

fun.call(obj); //this指向obj
fun.apply(obj); //this指向obj

var another = fun.bind(obj);
another(); //this指向obj
```



> ③ `fun();`的形式，this指向global。这种情况分三种子情况，其中第三种更特殊一点。

```javascript
function fun() {
    console.log(this.a);
}

fun(); //this指向global
```

```js
var obj = {
    fun: function(){
        console.log(this);
    }
}

var another = obj.fun;
another(); //this指向global
```

```js
var obj2 = {};
(obj2.fun = obj.fun)(); //this指向global
```



> ④ 使用new创建的对象，this会被绑定到新创建的对象上。

```js
function Fun() {
    this.name = "zhang";
}

var obj = new Fun(); //this绑定到obj
console.log(obj.name); //zhang
```



> ⑤ ②有种很特殊的情况，如果call/apply/bind中的对象为null，则this会被绑定到global。
>
> 如果fun内部会更改obj，则全局对象会被修改。
>
> 更好的实践应该是，当想传null进去的时候，改为传一个规定好的无用的{}对象。

```js
function foo() {
    this.name = "foo";
}

var fun = foo.bind(null);
fun();

console.log(name); //foo
```



> ⑥ ES6中增加了箭头函数，箭头函数的this只能被绑定一次，后面的绑定都不起作用。

```js
function foo() {
    return () => {
        console.log(this.a);
    }
}

var obj1 = {a:1};
var obj2 = {a:2};

var bar = foo.call(obj1); //this绑定到obj1
bar.call(obj2); //this已经有绑定，所以不会再次绑定。所以输出1
```

> 总结
>
> 这几种绑定形式的优先级为：④>②=⑤>③>①。⑥自成一派，会直接使用使用外层词法作用域的this。

## 如何判断父子关系

> 判断对象是否由某个类构造，使用instanceof
>
> 实际为查找Student.prototype是否在obj的原型链上出现过

```js
function Student(){

}
var obj = new Student();

console.log(obj instanceof Student); //true
```



## 最佳实践

> js中实现面向对象有各种不同的技术手段，现总结一种通用的程序结构设计方法。

# JS的类型系统

> js中共有7种语言类型：
>
> ```js
> console.log(typeof {}); //object
> console.log(typeof "zhang"); //string
> console.log(typeof 3.2); //number
> console.log(typeof false); //boolean
> console.log(typeof function(){}); //function
> console.log(typeof null); //object
> console.log(typeof undefined); //undefined
> ```
>
> 其中`typeof null`返回object，是一个实现时的bug。其实应该返回null。

> 内置函数：Object/String/Number/Boolean/Function/RegExp等，typeof会返回function。其构造出来的对象，typeof会返回object。
>
> ```js
> console.log(typeof RegExp); //function
> 
> var patt = /runoob/i
> console.log(typeof patt); //object
> ```

> 如果有需要，js会自动将字面量提升到内置对象。例如
>
> ```js
> console.log("zhang".length); //5。自动提升为String
> console.log(42.359.toFixed(2)); //42.36。自动提升为Number
> ```

> Date：只能构造，没有字面量
>
> Error：一般被自动创建，也可以`new Error()`。

## object支持的操作

## 如何复制一个对象



# 严格模式

`"use strict"`关键字可以开启严格模式。

此关键字可以加在文件开头，函数开头。

但建议加在文件开头，并且同一个工程不要混用严格模式和非严格模式。

| 函数                   | strict             | !strict                        |
| ---------------------- | ------------------ | ------------------------------ |
| eval                   | 有自己单独的作用域 | 使用运行位置的作用域           |
| 读取不存在的普通变量   | ReferenceError     | ReferenceError                 |
| 写入不存在的普通变量   | ReferenceError     | 在全局作用域创建变量           |
| with                   | 不允许使用         | 允许使用但容易出错，不建议使用 |
| 普通函数的this绑定到哪 | undefined          | global                         |
|                        |                    |                                |
|                        |                    |                                |
|                        |                    |                                |
|                        |                    |                                |

# ES6新增关键字

| 关键字 | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| let    | 可以支持将变量定义在块作用域中<br />不会像var一样将声明和赋值分开(术语叫提升)<br />在`for(let i=0;i<10;++i)`中，每次循环都会创建一个新的循环变量`i` |
| const  | 用法和含义同let，只是不可修改                                |
| import | 从模块中导入某个函数。`import fun from "somefile"`           |
| export | 从模块中导出某个函数。`export fun`                           |
| module | 导入整个模块。`module some from "somefile"`                  |
| =>     | 如果闭包函数用=>定义，则可以将真正的调用对象自动绑定到闭包函数中的this上。 |
|        |                                                              |
|        |                                                              |
|        |                                                              |



# 无法归类的主题

