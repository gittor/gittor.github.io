# 前言

本文主要来自于《你不知道的JavaScript》，分成几个角度总结了js开发中的方方面面。

这是一篇总结性质的文章，所以要求读者有一定的js基础。

总结的内容主要分为两部分：

1. 易错点
2. 最佳实践

# 变量与作用域

本节的目的在于解决一个问题：给定一段js代码，分析出它的运行过程及结果。

通用分析方法：将js代码的完整运行过程，看做编译阶段和运行阶段，分别分析。

## 编译阶段

编译阶段的主要工作是做提升。

编译器会将变量声明和函数声明，提升到作用域开头。

例如`var a=2;`会被分成`var a;`和`a=2;`两部分，而`var a;`部分会被提升到作用域开头，见自测1。

提升有几个原则：

1. 先提升函数声明，再提升变量声明。
2. 遇到同名变量/函数，则使用先声明的，后声明的会被忽略。
3. 遇到同名函数，则使用后定义的，后定义的覆盖先定义的。
4. 删除不必要的作用域。在ES5及其之前，只有全局作用域，函数级作用域，表达式作用域，with作用域，没有块级作用域。
   1. 提升后的作用域，不是函数作用域就是全局作用域。
   2. 表达式作用域的唯一应用场景是在表达式内定义函数：`foo(function some(){console.log("in some");});`，此时some只能在some内部访问，可以用于实现递归。
   3. ES6中的let，①支持将变量定义在块作用域中；②不会产生变量声明提升；③在`for(let i=0;i<10;++i)`中，每次循环都会创建一个新的循环变量`i`。
   4. ES6及其之后，还有文件作用域。也就是在文件中声明`var a=10;`，a并不属于全局对象。

## 运行阶段

模拟运行得到结果。

1. 确定是strict模式还是!strict模式。
   1. strict模式下，读取和赋值不存在的变量都会报错。
   2. !strict模式下，读取时找不到会报错，赋值时会在全局作用域创建一个变量。
2. 需要明确变量查找规则，使用的是编译时作用域还是运行时作用域。
   1. 编译时作用域的上级作用域，是写代码定义时就可以看到的，不需要分析调用栈。一般使用这种。
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

> 不同的语言实现面向对象的方式都不同，但在js中，支持三种方式。
>
> 一种是使用对象混合技术，将父类对象的数据和函数复制到子类对象。
>
> 另一种是使用原型链，只通过prototype关联父子对象的形式。
>
> 第三种是使用ES6新增的class关键字，但底层使用的其实还是原型链。

## 使用混合实现

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

> 原型链说明
>
> Function有显式的prototype属性，可以直接访问。
>
> Object只有隐式的prototype属性，必须通过Object.getPrototypeOf(obj)访问。

> 使用原型链的实现方式也有2种。

> 通过`var obj = Object.create(proto);`实现。
>
> ```js
> var Base = {
>     init: function(){
>         this.count = 1;
>     },
>     say: function(){
>         console.log(this.count);
>     }
> }
> 
> var Derived = Object.create(Base);
> Derived.greet = function(){
>     console.log("Derived.greet");
>     this.say();
> }
> Derived.init = function(){
>     Base.init.call(this);
>     this.count = 2;
> }
> 
> var obj = Object.create(Derived);
> obj.init();
> obj.say(); //2
> ```
> 这种方式的关键在于Base和Derived就是原型链上的节点。
>
> 所以代码中不会出现显式的prototype访问。
>
> 由于每个对象都是原型节点，所以如果要把属性直接定义到实例对象上，需要实现统一的init接口。



> 通过`var obj = new Student();`实现。
>
> ```js
> function Base(){
>        this.count = 1;
> }
> Base.prototype.say = function(){
>        console.log(this.count);
> }
> 
> function Derived(){
>        Base.call(this);
>        this.count = 2;
> }
> Derived.prototype = Object.create(Base.prototype);
>     Derived.prototype.greet = function(){
>        console.log("Derived.greet");
>        this.say();
> }
> 
> var obj = new Derived();
> obj.greet();
> //Derived.say
> //2
> 
> obj.say(); //2
> ```
>
> 这种形式的关键在于用js中的"构造函数"代替面向对象中的"类"。



> 原型链中一个很关键的地方就是属性屏蔽，下层对象中的属性，会屏蔽上层对象的同名属性。
>
> 当修改一个属性的时候，要明确想要修改的是实例对象中的属性，还是原型节点上的属性。
>
> 属性屏蔽有些时候会产生意想不到的问题。
>
> ```js
> var base = {
>  count: 1
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
>  this.name = "zhang";
> }
> var obj = new Student();
> 
> //上面的代码，相当于执行
> function Student() {
>  var obj = Object.create(null); //1
>  Object.setPrototypeOf(obj, Student.prototype);//2
>  var this = obj; //3
> 
>  Student.call(this);
> 
>  return obj; //4
> }
> var obj = Student();
> ```
>
> 关键是第二步，链接的是Student.prototype。



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

> 直接判断两个对象的原型链关系

```js
var Foo = {}
var Bar = Object.create(Foo);
var b1 = Object.create(Bar);
console.log(Foo.isPrototypeOf(Bar)); //true
console.log(Foo.isPrototypeOf(b1)); //true
console.log(Bar.isPrototypeOf(b1)); //true
```



## 最佳实践

js中实现面向对象有各种不同的技术手段：

从传统面向对象的角度思考，建议使用ES6中class的做法。

从原型链的角度思考，应该摒弃类的概念，只保留对象的概念。

# JS的类型系统

> js中共有8种语言类型(规范中是7种，function是object的一个子类型，但在此将其理解为一种独立的类型更合适，因为typeof对其特殊处理了)：
>
> ```js
> console.log(typeof {}); //object
> console.log(typeof "zhang"); //string
> console.log(typeof 3.2); //number
> console.log(typeof false); //boolean
> console.log(typeof function(){}); //function。其实是object的子类型
> console.log(typeof null); //object
> console.log(typeof undefined); //undefined
> console.log(typeof Symbol()); //symbol。ES6中新增。
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

## Object常用操作

常用操作

| 方法                                      | 说明                                       |
| ----------------------------------------- | ------------------------------------------ |
| `target = Object.assign(target, source);` | 将source中的所有可枚举属性，覆盖到target。 |
| `Object.entries(obj)`                     | 返回obj的所有直接属性的键值对。            |
| `Object.keys(obj)`                        | 返回内容同entries，但只返回键。            |
| `Object.values(obj)`                      | 返回内容同entries，但只返回值。            |
| `Object.setPrototypeOf(obj, proto)`       | 将obj的prototype设为proto。                |

循环

| 循环方式 | 循环内容        |
| -------- | --------------- |
| for...in | 同Object.keys   |
| for...of | 同Object.values |



## 如何复制一个对象

无。

## getter/setter

```js
var obj = {
  _id : 0,
  get id(){ return this._id;},
  set id(value){this._id = value;}
}
```



## 数组操作

> 基本操作

```js
var a = [1, 2, 3]

a[3] = undefined;
a[5] = 6
console.log(a.length); //6
console.log(a); //[ 1, 2, 3, undefined, <1 empty item>, 6 ]
console.log(a[4]); //undefined

delete a[2];
console.log(a.length); //6。删除元素不会导致长度变化，即使删除最后一个元素也不会导致长度变化。
console.log(a); //[ 1, 2, <1 empty item>, undefined, <1 empty item>, 6 ]

a.name = "zhang";
console.log(a.length); //6。添加属性不会导致长度变化
console.log(a); //[ 1, 2, <1 empty item>, undefined, <1 empty item>, 6, name: 'zhang' ]

a.length = 3; //可以通过设置数组长度来截断数组
console.log(a); //[ 1, 2, <1 empty item>, name: 'zhang' ]
```

> 将Array-like对象转换为真正的Array

```js
function foo()
{
    var arr = Array.prototype.slice.call(arguments); //将arguments转换为真正的数组
    console.log(arr);
}

foo("apple", "banana"); //[ 'apple', 'banana' ]
```

> 查找

```js
var a = ["apple", "banana", "orange"]

console.log(a.indexOf("banana")); //1
console.log(a.indexOf("none")); //-1

//根据规则查找
console.log(a.findIndex((item)=>{
    return item[0] === 'o';
})); //2
```

> 连接两个数组

```js
var a = ["apple", "banana", "orange"]
var b = a.concat("black");
var c = a.concat(["black"]);

console.log(a); //[ 'apple', 'banana', 'orange' ]
console.log(b); //[ 'apple', 'banana', 'orange', 'black' ]
console.log(c); //[ 'apple', 'banana', 'orange', 'black' ]
```

> 创建一个固定大小的数组
>
> ```js
> var a = new Array(3);
> console.log(a); //[ <3 empty items> ]
> 
> var b = [];
> b.length = 3;
> console.log(b); //[ <3 empty items> ]
> 
> var c = Array.apply(null, { length : 3 });
> console.log(c); //[ undefined, undefined, undefined ]
> ```
>
> 

## 字符串操作

> 不可修改性
>
> ```js
> var name = "zhang";
> 
> name[2] = 'x';
> console.log(name); //zhang。字符串是不可修改的
> ```

> 借用数组的方法来处理字符串
>
> ```js
> var name = "zhang";
> 
> console.log(Array.prototype.join.call(name, '-')); //z-h-a-n-g
> 
> var b = Array.prototype.map.call(name, (c)=>{
>     return c.toUpperCase()+"*";
> });
> console.log(b); //[ 'Z*', 'H*', 'A*', 'N*', 'G*' ]
> ```

> 其他操作
>
> 假设`var name = "zhang";`。
>
> | 操作         | 调用                                   | 说明                                      |
> | ------------ | -------------------------------------- | ----------------------------------------- |
> | 全部转为大写 | `var b = name.toUpperCase();`          | ZHANG                                     |
> | 全部转为小写 | `var b = name.toLowerCase();`          | zhang                                     |
> | 截取子串1    | `var b=name.substr(start, length)`     | start为-1时代表最后一个字符。             |
> | 截取子串2    | `var b=name.substring(start, end)`     | 得到**[start,end)**的子串，参数不能为负。 |
> | 截取子串3    | `var b=name.slice(start, end)`         | 得到**[start,end)**的子串。参数可以为负。 |
> | 去掉前后空格 | `var b=name.trim()`                    |                                           |
> | 格式化       | ``console.log(`my name is ${name}`);`` | ES6首次提供。ES5中用原始的+。             |
> | 反格式化     |                                        |                                           |
> | 规范化       | `name.normalize();`                    | 进行unicode规范化。                       |
> | 查找内容     | `name.match(/an/)`                     | 返回值是所有匹配内容的数组                |
>

> 处理unicode字符串
>
> ```js
> //计算长度
> [...name.normalize()].length;
> ```
>
> ```js
> //读取字符
> name.codePointAt(index);
> ```
>
> 

## 数字操作

> js中只有浮点数，没有整数。

> 基本操作
>
> ```js
> var a = 5E10;
> console.log(a); //50000000000
> console.log(a.toExponential()); //5e+10
> 
> var b = 42.59;
> 
> //保留小数点后n位后转换成字符串，必要时进行四舍五入
> console.log(b.toFixed(0)); //"43"
> console.log(b.toFixed(1)); //"42.6"
> console.log(b.toFixed(2)); //"42.59"
> console.log(b.toFixed(3)); //"42.590"
> console.log(b.toFixed(4)); //"42.5900"
> 
> //从最高位算起，保留n位有效数字后转换成字符串，必要时进行四舍五入
> console.log(b.toPrecision(1)); //"4e+1"
> console.log(b.toPrecision(2)); //"43"
> console.log(b.toPrecision(3)); //"42.6"
> console.log(b.toPrecision(4)); //"42.59"
> console.log(b.toPrecision(5)); //"42.590"
> ```

> | 含义                   | 表示法                                                |
> | ---------------------- | ----------------------------------------------------- |
> | 十六进制/八进制/二进制 | 0xff/0o7/0b1                                          |
> | 最小/最大的浮点数      | Number.MIN_VALUE、Number.MAX_VALUE                    |
> | 浮点数判等的阈值       | Number.EPSILON                                        |
> | 安全整数的范围         | Number.MIN_SAFE_INTEGER、Number.MAX_SAFE_INTEGER      |
> | 检测是否整数           | `Number.isInteger(42.0); //true`                      |
> | 检测是否安全整数       | `Number.isSafeInteger(42.0); //true`                  |
> | 转换为32位整数值       | `var n = 42.3|0;`忽略其他位数，只保留有效的32位整数。 |
> | 转换为任意进制的字符串 | `n.toString(8);`                                      |

> 无效数值NaN
>
> ```js
> console.log(NaN===NaN); //false。js中唯一一个不等于自身的值。
> 
> console.log(isNaN(42)); //false
> console.log(isNaN("apple")); //true。这是isNaN的一个bug。
> 
> //Number.isNaN只能在ES6及其之后使用
> console.log(Number.isNaN(42)); //false
> console.log(Number.isNaN("42")); //false
> ```

> 代表无穷的数字
>
> ```js
> console.log(1/0); //Infinity。用Number.POSITIVE_INFINITY表示
> console.log(-1/0); //-Infinity。用Number.NEGATIVE_INFINITY表示
> ```
>
> 当运算结果溢出时，也会导致出现无穷数。
>
> 应该避免对无穷数做运算。
>
> ```js
> console.log(Number.POSITIVE_INFINITY/Number.POSITIVE_INFINITY); //NaN
> console.log(Number.POSITIVE_INFINITY*Number.POSITIVE_INFINITY); //Infinity
> ```

> 正负0
>
> 正负0都是相等的，运算时也是可以相互替换的。只有一个方法可以区分0的符号。
>
> ```js
> //此方法属于ES6新增方法
> console.log(Object.is(-1*0, -0)); //true
> console.log(Object.is(-1*0, 0)); //false
> ```
>
> 保留-0是为了，防止一个负数逐渐变成0的时候，丢失了它的符号位，导致需要符号位的运算过程失效。

## 布尔操作

> ```js
> var b = new Boolean(false); //手动装箱
> 
> if(b)
> {
>     console.log("b is true"); //会执行到这里，因为b现在有值
> }
> 
> if(b.valueOf()) //手动拆箱
> {
>     console.log("b is true"); //执行不到这里
> }
> ```

| 表达式    | 结果  |
| --------- | ----- |
| "0"       | true  |
| []        | true  |
| {}        | true  |
| ""        | false |
| 0         | false |
| null      | false |
| undefined | false |

## 正则表达式

```js
var a = /pattern/attributes;
var b = new RegExp(pattern, attributes);
```

attributes的可选值:

| 修饰符 | 描述                                  |
| ------ | ------------------------------------- |
| i      | 大小写不敏感                          |
| g      | 直到找到所有匹配                      |
| m      | 多行匹配                              |
| u      | 标明pattern是unicode字符串。ES6新增   |
| y      | 打开定点模式，与r.lastIndex配合使用。 |

成员变量

| 变量名       | 含义                                                |
| ------------ | --------------------------------------------------- |
| r.ignoreCase | attributes是否具有i属性                             |
| r.global     | attributes是否具有g属性                             |
| r.mutiline   | attributes是否具有m属性                             |
| r.flags      | 列出所有attributes属性，以"gimuy"的顺序             |
| r.source     | 得到pattern                                         |
| r.lastIndex  | 整数。开始下一次匹配的字符位置。与修饰符y配合使用。 |

成员函数

| 方法                       | 说明                                                         |
| -------------------------- | ------------------------------------------------------------ |
| compile                    |                                                              |
| `var res = r.exec(string)` | 找到时返回结果数组，找不到时返回null。<br />结果数组中第0个元素是匹配结果，第1个元素是`()`的子串匹配结果。 |
| `var res = r.test(string)` | 同exec，但只返回匹配(true)或不匹配(false)。                  |

## 日期类型

```js
var date = new Date(); //得到当前时间
var nowstamp = Date.now(); //取得当前时间戳
```

参考链接：https://www.w3school.com.cn/jsref/jsref_obj_date.asp

## 异常类型

可以手动构造一个Error来获得当前调用堆栈信息，作为调试手段之一。

```js
function say()
{
    var e = new Error();
    console.log(e); //会打印当前调用堆栈
}
function walkAndSay()
{
    say();
}

walkAndSay();
```

## JSON操作

| 方法                              | 说明                   |
| --------------------------------- | ---------------------- |
| `var obj = JSON.parse(text);`     | 将字符串解析为对象     |
| `var text = JSON.stringify(obj);` | 将对象转换为json字符串 |



## 类型转换

字符串与数字

| 转换类型       | 操作                                                         |
| -------------- | ------------------------------------------------------------ |
| 数字转字符串   | `var a = String(3.14);`                                      |
| 字符串转数字   | `var b = Number("3.14");`参数只能是合法数字，不能有任何非数字字符。 |
| 字符串转整数   | `var b = parseInt("3.14px");`返回3<br />**注意**：ES5中使用parseInt时，不指定第二个参数，"077"会被当做八进制解析。<br />ES6会将其当做10进制解析。 |
| 字符串转浮点数 | `var b = parseFloat("3.14px");`返回3.14                      |

bool与数字

| 转换类型   | 操作                                                         |
| ---------- | ------------------------------------------------------------ |
| bool转数字 | `var b = Boolean(true);`返回1。<br />`var b = Boolean(false);`返回0。 |

## &&和||

和其他语言不同，js中的&&和||返回的是操作数中的一个，而不是bool。

| 操作          | 结果  |
| ------------- | ----- |
| 42\|\|"abc"   | 42    |
| a&&"abc"      | "abc" |
| null\|\|"abc" | "abc" |
| null&&"abc"   | null  |

## ==和===

当操作数的类型不同时，===直接返回false，==会统一两个操作数的类型再比较。

| 操作数类型      | 结果             |
| --------------- | ---------------- |
| 数字==字符串    | 字符串转换为数字 |
| bool==其他      | bool转换为数字   |
| null==undefined | true             |
| 对象==字符串    | 对象转换为字符串 |
| 对象==数字      | 对象转换为数字   |
| 对象==对象      | 比较内存地址     |

## 小于<和大于>

大于和小于可以用来比较两个字符串，以字典顺序。

## Symbol类型

> 符号类型一般用于防止出现重复名字的属性。

# ES6新增关键字(常用)

| 关键字       | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| let          | 可以支持将变量定义在块作用域中<br />不会像var一样将声明和赋值分开(术语叫提升)<br />在`for(let i=0;i<10;++i)`中，每次循环都会创建一个新的循环变量`i` |
| const        | 用法和含义同let，只是不可修改。这种不可修改是说指针不可修改而不是值不可修改。 |
| import       | 从模块中导入某个函数。`import fun from "somefile"`           |
| export       | 从模块中导出某个函数。`export fun`                           |
| module       | 导入整个模块。`module some from "somefile"`                  |
| =>           | 如果闭包函数用=>定义，则可以将真正的调用对象自动绑定到闭包函数中的this上。 |
| Number.isNaN |                                                              |
| Symbol       |                                                              |
| ...[1,2,3]   | 会把[1,2,3]展开为三个独立的变量。可以用在函数形参、数组字面量等任意地方。 |
| ...rest      | 将几个独立的变量，包装为一个数组，数组名为rest。             |
| 形参加默认值 |                                                              |
| 解构         | 包括数组解构、对象解构。解构是一个很庞大的话题，有超级多的应用。 |
| super        | 当super.xxx()出现在某个对象的方法中时，它代表访问this.prototype.xxx()。 |



# 生成器

## 生成器理论

> 生成器是ES6引进的一个规范，它在工作函数内部，提供了一种特殊的回调机制，对"生产者-消费者"问题提供了一套定义良好的接口。
> 应用一：预知即将得到一大批数据，总体时间较长，工作函数希望在得到一部分数据后，通知调用者完成了部分工作。此时调用者可以先处理这部分数据。
> 应用二：工作函数的作用是根据一定的算法，生成一串值。此时可以每生成一个值，向外通知一次。

> 在ES5中，不使用生成器，而是在工作函数的参数列表中加一个回调也可以完成相同的事。
>
> 但生成器提供了更多的功能：
>
> * for...of支持
> * 与Promise配合可以以同步方式写异步代码。但在ES6中没有得到很好支持，需要第三方库的支持。

## 生成器原理

```js
function* generator(){
  let last = yield 10;
  yield last+1;
}

let gen = generator();

console.log(gen.next()); //{ value: 10, done: false }
console.log(gen.next(100)); //{ value: 101, done: false }
console.log(gen.next()); //{ value: undefined, done: true }
```

应该这样理解生成器的工作原理：生成器本身没有挂起、阻塞的说法，应该把yield理解为保存生成器的当前状态。next(value)理解为为生成器提供一个新状态并继续运行。

所以生成器可以运行在事件循环的任意一个时间片内。

## 使用生成器

```js
function* Fabnaci(maxnum) //定义了一个斐波那契生成器
{
    var arg1, arg2;

    while (true) {
        if (arg1 == undefined) {
            arg1 = 1;
            yield 1;
        }
        else if (arg2 == undefined) {
            arg2 = 1;
            yield 1;
        }
        else {
            let result = arg1+arg2;
            arg1 = arg2;
            arg2 = result;
            yield result;
        }

        if (arg1 + arg2 >= maxnum) {
            break;
        }
    }
}

let fab = Fabnaci(500); //定义了一个迭代器
for(let n of fab)
{
    console.log(n);
}
```

## 枚举一个生成器

```js
function* fruit(){
  yield "apple";
  yield "banana";
}

function* vegetable(){
  yield "tomato";
  yield "potato";
}

function* shop(){ //shop依次枚举了其他两个生成器
  yield* fruit();
  yield* vegetable();
}

for(let x of shop()) //结果为输出商店内所有的水果和蔬菜
{
  console.log(x);
}
```



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
| 八进制使用"07"的写法   | 不支持             | 支持                           |
| 为undefined赋值        | TypeError          | 可以                           |
|                        |                    |                                |
|                        |                    |                                |

# 异步机制

> js中的异步分为两部分，ES5中使用回调的方式完成异步通知，ES6中使用Promise完成异步通知。ES6同时提供了生成器，使程序员可以以同步的方式写异步代码。
>
> 1. ES5中也有Promise库，但都是第三方的，底层还是回调，所以还是有回调的问题。
> 2. ES6中的Promise，是由ES委员会定义的一套标准，从原理本身对错误进行了规避。

>使用回调的方式有几个缺点：
>
>1. 大量的回调可能会嵌套，造成回调地狱。这部分可以通过重构代码解决。
>2. 没有统一的接口来处理异步链需求，通常会写成函数嵌套的样式，使代码不太清晰。
>   1. 某些异步任务有先后关系：ABC是三个独立的异步任务，但需要以A->B->C的顺序依次完成。
>3. 如果某工作函数提供了一个回调参数，当不能确定回调函数的调用时机(同步/异步)时，回调内的代码和工作函数后面的代码，先执行哪部分是不知道的。
>4. 由于回调时机掌握在工作函数手里，所以回调函数可能被意外地多次执行或不执行。
>5. 回调方式往往伴随着setTimeout的使用，如果在工作函数中抛出异常，setTimeout是不会把这个异常通知给调用代码的。
>
>上面缺点1、2，出错的代码掌握在自己手里，是可以通过重构解决的，这不是核心问题。缺点3、4、5，是由于工作函数可能出错导致的。如果所有的工作函数都是完全正确的，或程序员只使用了其中正确的部分，那回调的方式完全没问题。但一旦工作函数出了问题，我们是没办法直接解决的。
>
>所以，如何避免工作函数出错，就成了核心问题。有鉴于此，ES提供了Promise标准，从语言本身解决了上面的问题。

## 基于回调的异步

```js
//异步任务工作函数
function getFruit(name, callback) {
  setTimeout(() => {
    switch(name)
    {
      case "apple": callback({"name": "apple", "price": 100}); break;
      case "banana": callback({"name": "banana", "price": 200}); break;
      case "orange": callback({"name": "orange", "price": 300}); break;
    }
  }, 2000);
}

//针对异步结果要做的操作
function outputFruit(fruitobj)
{
  console.log(fruitobj);
}

//启动异步任务
getFruit("banana", outputFruit);
```



## Promise接口

### 理论

可以把Promise当做回传统回调函数的封装。当`new Promise`时，相当于注册了一个回调，resolve和reject就是调用这个回调。

### 基础用法

```js
//将基于回调的异步任务工作函数改写为基于Promise
function getFruit(name) {
    return new Promise(function(resolve, reject){
        setTimeout(() => {
            switch(name)
            {
            case "apple": resolve({"name": "apple", "price": 100}); break;
            case "banana": resolve({"name": "banana", "price": 200}); break;
            case "orange": resolve({"name": "orange", "price": 300}); break;
            }
        }, 2000);
    });
}

//针对异步结果要做的操作
function outputFruit(fruitobj)
{
  console.log(fruitobj);
}

getFruit("banana").then(
    function onfulfill(result){
        outputFruit(result);
    }
    ,function onreject(error) {
        console.log(error);
    }
).catch(function(error){
    console.log(error.message);
});
```

有以下几个特点：

1. 通过Promse构造函数传进去的函数会立即执行，通过then传进去的回调函数本轮事件循环内一定不会执行。解决了问题3。
2. 一个then最多只会被调用一次。如果then在异步函数执行完才添加，也会被调用。解决了回调多次被调用的问题。
3. then可以链式调用，并且回调顺序和调用顺序一致。解决了问题2。
4. then内的onfulfill可以传回另一个值，这个过程可以用来实现数据管道。
5. 如果整个异步链的某一步出现了异常，异常会被传递到第一个onreject或catch。解决了问题5。

调用时机(只总结了最有用的几种情况)

| 函数      | 调用时机                                  |
| --------- | ----------------------------------------- |
| 工作函数  | 同步立即调用                              |
| onfulfill | resolve被调用并且结果正确                 |
| onreject  | 发生异常或者reject被调用                  |
| catch     | 发生异常并且catch前没有设置任何onreject。 |

遗留的问题：如果工作函数既没有出错，也没有resolve和reject，则then就一直不被回调。参考下面的解决方案。

### 超时机制

```js
function timeoutPromise(delay_ms) {
    return new Promise(function(resolve, reject){
        setTimeout(() => {
            reject("timeout");
        }, delay_ms);
    });
}

Promise.race([foo(), timeoutPromise(1000)])
.then(function onfulfill(val){
    //foo完成
}, function onreject(err){
    //foo拒绝或超时
});
```

### 使用建议

* 避免嵌套使用Promise。
* 总是在onfulfill和onreject内返回正确的数据或抛出正确的异常。
* 尽量使用catch块。

### 常用API

| 接口                               | 说明                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| `val p = Promise.resolve(result);` | 返回一个决议的result Promise对象。                           |
| `val p = Promise.reject(result);`  | 返回一个拒绝的result Promise对象。                           |
| `val p = Promise.all([p1, p2]);`   | 数组中所有Promise对象都resolve，结果才resolove。<br />并且onfulfill接收results数组，顺序为[p1.result,p2.result]。<br />如果数组为空，表示成功完成。 |
| `val p = Promise.race([p1,p2])`    | 只取数组中第一个Promise的决议结果。<br />如果数组为空，则会挂起并且永远不会调用then。所以应该禁止传空数组。 |

## 生成器与Promise配合

> 基本原理：yield一个Promise，在外部决定调用it.next(...)还是it.throw(...)。

手工改写例子太复杂了，不建议在工程中使用。事实上很多库都提供了实现。

最好的方式是使用ES7新增的async和await关键字。

## async和await

### 原理

| 关键字 | 实际作用                                                     |
| ------ | ------------------------------------------------------------ |
| async  | 当对一个同步方法加上async关键字后，这个方法的返回值会被包装为一个Promise。<br />但最好不要依赖这个机制，不是一个好习惯，而是应该直接返回一个Promise。 |
| await  | 得到异步方法返回的Promise，并把await所在行及后面的代码，都封装在这个Promise的then里面执行。<br />由于此原理，所以await必须被封装在async函数中运行。 |

### 使用方式

```js
async function getFruit(name) {
  return new Promise(function(resolve, reject){
    setTimeout(() => {
      switch(name)
      {
      case "apple": resolve({"name": "apple", "price": 100});
      case "banana": resolve({"name": "banana", "price": 200});
      case "orange": resolve({"name": "orange", "price": 300});
      }
  }, 2000);
  });
}

async function outputFruit(name)
{
  let fruitobj = await getFruit(name);
  console.log("fruitobj:", fruitobj);
}

outputFruit("banana");
```

## 总结

| 版本 | 异步方式                                                     |
| ---- | ------------------------------------------------------------ |
| ES5  | 语言只支持异步回调，有第三方的Promise库。                    |
| ES6  | 语言本身提供了Promise机制，其实质是异步回调的封装。<br />由第三方提供"生成器+异步"形式的库。 |
| ES7  | 语言本身提供了async和await关键字，进一步封装了"生成器+异步"的方式。 |

# 数学库

| 方法          | 含义                  |
| ------------- | --------------------- |
| `random();`   | 生成[0,1]之间的随机数 |
| `ceil(num);`  | 对num进行向上舍入     |
| `floor(num);` | 对num进行向下舍入     |

## 线性同余随机数

```js
if(!Math.seed && !Math.seedRandom)
{
    Math.seed = 0;
    Math.seedRandom = function() {
        Math.seed = (Math.seed * 9301 + 49297) % 233280;
        var rnd = Math.seed / 233280.0;
        return rnd;
    };    
}
```



# 模块管理

| 名称     | 说明                                            | 典型API |
| -------- | ----------------------------------------------- | ------- |
| AMD      | RequireJS使用的方式。异步加载。                 |         |
| CMD      | SeaJS使用的方式。                               |         |
| CommonJS | Node.js使用的方式。同步加载。以文件为模块单元。 |         |
| UMD      | 结合了AMD和CommonJS的方式。                     |         |
| ES6模式  | 类似于CommonJS。以文件为模块单元。              |         |

# Babel

Babel是这样一个工具，使用它可以把ES6+的代码，转换成ES5的对应形式。

# 总结

> js给我的感觉像是一锅大杂烩一样。
>
> 虽然c++也是一锅烩，但起码可以被分成不同的技术主题，主题之间往往有比较明确的界限，不会难以记忆。js中的杂烩，是所有细节内容都掺杂在一起，导致根本没办法根据一套特定的规则来记忆。比如同样是面向对象的语义，this使用的是动态绑定，super却使用的是静态绑定。

> 如果把语言看成工具，类型系统看做积木。
>
> 越是静态的语言，提供的工具越有限，搭积木越方便，而修改积木本身变得越困难。比如Array是一个数组，C++中只能通过整数下标来访问，只能存储固定的值。
>
> 越是动态的语言，提供的工具能力越来越强，有时候甚至可以修改积木本身。比如js中的数组可以表现得像一个对象，通过属性来访问数据。
>
> 这是两个极端，左面是C++，虽然能完成任务，但需要更精巧的设计，用时可能会更长；右面是JS，能按照程序员的想法随意存储访问任何数据，虽然简单任务会变得更容易实现，但大型项目会造成流程上的混乱。
>
> 这种情况下，在写JS代码时，要求我们做更细化的数据流设计，避免出现数据流混乱的问题。这是写js代码最容易忽略的地方。

> ES6及其之后介绍的新语法，很大一部分是为了更好地解决某一类问题而出现的。ES5中也可以解决，但新语法更好。例如迭代器，Promise等。