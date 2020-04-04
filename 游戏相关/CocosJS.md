# 前言

本篇文章以cocos2d-x v3.16为基础，总结了开发中常用的概念及代码片段。

只涉及js-binding部分。

官方文档：https://docs.cocos2d-x.org/api-ref/js/v3x/index.html

# 项目结构介绍

以js HelloWorld项目为例

* frameworks：cocos本身的所有文件
* simulator：编译后生成的可执行文件
  * win32：windows的exe文件所在的目录
    * Resources：执行时需要的所有cocos运行时、代码、资源所在的目录
      * res：本项目的所有资源
      * src：本项目的所有源码
      * script：jsb的所有代码
* **res：所有资源所在的文件夹**
* **src：所有源码所在目录**
* .cocos-project.json：关于cocos的配置文件，没什么用
* **main.js：js的启动文件**
* manifest.webapp
* **project.json：本项目的配置**

# 主要模块介绍

## cc

单例类

| 名称        | 作用                         |
| ----------- | ---------------------------- |
| director    | 总导演                       |
| pool        |                              |
| audioEngine | 音频操作                     |
| view        | 控制游戏窗口的操作           |
| screen      | 浏览器运行时全屏显示         |
| path        | 路径操作                     |
| game        | 控制整个游戏的启动暂停和配置 |
| sys         | 获取运行环境                 |
| plistParser | 解析plist文件                |
| loader      | 负责Resources目录操作        |

| 名称                  | 作用                           |
| --------------------- | ------------------------------ |
| Point/Size/Rect/Color |                                |
| Class                 | cc为实现js面向对象提供的功能类 |
| Action/...            | 动作类                         |
| Event/...             | 事件类                         |
| GridBase/...          |                                |
| Node/...              |                                |

## ccs

CocosStudio除UI外的功能

## ccui

CocosStudio UI相关功能

| 名称            | 角色 | 作用                   |
| --------------- | ---- | ---------------------- |
| helper          | 单例 | 用于在UI树上做查找工作 |
| Widget/...      | 类   | control和layout的基类  |
| Layout/...      | 类   | 各种layout的基类       |
| RichElement/... | 类   | 富文本控件的基类       |

## jsb

| 名称          | 作用                       |
| ------------- | -------------------------- |
| fileUtils     | 控制搜索目录、访问系统目录 |
| AssetsManager |                            |
| Manifest      | 操作Android Manifest文件   |
| reflection    | 与java代码交互的中间件     |

## sp

骨骼动画相关功能。

# 启动游戏

```js
cc.game.onStart = function(){
    
    //设置分辨率
    
    //设置搜索路径
    
    //配置并运行第一个场景
};
cc.game.run();
```



# 分辨率设置

```javascript
cc.view.enableRetina(false);

//cc.ORIENTATION_PORTRAIT 相当于ORIENTATION_LANDSCAPE_LEFT
//cc.ORIENTATION_LANDSCAPE_LEFT home键在右
//cc.ORIENTATION_LANDSCAPE_RIGHT
//cc.ORIENTATION_PORTRAIT
//cc.ORIENTATION_PORTRAIT_UPSIDE_DOWN
cc.view.setOrientation(cc.ORIENTATION_LANDSCAPE);

//EXACT_FIT FIXED_HEIGHT FIXED_WIDTH NO_BORDER SHOW_ALL UNKNOWN
cc.view.setDesignResolutionSize(800, 450, cc.ResolutionPolicy.SHOW_ALL);

//当浏览器大小改变的时候，canvas的大小自动随之改变
cc.view.resizeWithBrowserSize(true);
```

# Director

| 成员       | 作用         |
| ---------- | ------------ |
| getWinSize | 取得窗口大小 |
|            |              |
|            |              |

# Action

## 属性动画类

| 方法                    | 作用 |
| ----------------------- | ---- |
| cc.moveBy/cc.moveTo     |      |
| cc.bezierBy/cc.bezierTo |      |
| cc.fadeIn/cc.fadeOut    |      |

## 直接设置属性类

| 方法                | 作用            |
| ------------------- | --------------- |
| cc.place            | 直接设置位置    |
| cc.hide/cc.show     |                 |
| cc.toggleVisibility | 切换visible属性 |
| cc.removeSelf       | 移除自身        |

## 动作组合类

| 方法        | 作用     |
| ----------- | -------- |
| cc.sequence | 依次运行 |
| cc.spawn    | 同时运行 |

## 网格动画类

| 方法       | 作用 |
| ---------- | ---- |
| cc.shaky3D |      |
| cc.waves   |      |

## 节奏控制类

| 方法           | 作用                 |
| -------------- | -------------------- |
| cc.ActionEase* | 控制action的运动节奏 |
| cc.delayTime   | 延时                 |

## 其他

| 方法                                                         | 作用                   |
| ------------------------------------------------------------ | ---------------------- |
| cc.targetedAction(node, action)                              | 强制在node上执行action |
| cc.callFunc(func(action, arg0, arg1, ...), node, arg0, arg1, ...) |                        |
| cc.follow(target, follow_rect)                               | 跟随target             |

## Action本身的接口

| 方法                        | 作用               |
| --------------------------- | ------------------ |
| action.clone()              | 返回克隆对象       |
| action.reverse()            | 返回反过程         |
| action.repeat(repeat_count) | 返回重复执行对象   |
| action.repeatForever()      | 返回永远重复的动作 |

## 和运行action有关的接口

| 方法                      | 作用                         |
| ------------------------- | ---------------------------- |
| cc.Node.runAction(action) |                              |
| cc.Node.pause()           | 停止所有selector和action     |
| cc.Node.resume()          | 继续运行所有selector和action |

## cc.ActionManager

cc中有一个默认的ActionManager，更新函数注册在cc.director.getScheduler()中。

---

也可以创建多个ActionManager：

```js
var actionMan = new cc.ActionManager();
scheduler.scheduleUpdateForTarget(actionMan, 0, false);

node.setActionManager(actionMan);
```

通过控制scheduler的更新速度来控制ActionManager的更新速度。

# Layer

## 纯色Layer

```javascript
//如果没有设置宽高，则为canvas大小
new cc.LayerColor(cc.color, with=undefined, height=undefined)
```

## 渐变Layer

```js
//gradient_dir
new cc.LayerGradient(startcolor, endcolor, gradient_dir=cc.p(0,-1))
```

## Layer组合

```js
var layers = new cc.LayerMultiplex(layer0, layer1, ...);
layers.switchTo(n);
```



# Menu

Menu定义了按钮的行为，与之相关的有两个接口：

| 接口                  | 作用            |
| --------------------- | --------------- |
| cc.Menu               | 管理cc.MenuItem |
| 实现了cc.MenuItem的类 | 具体的可点击项  |

## cc.Menu

| 方法                                                  | 作用                        |
| ----------------------------------------------------- | --------------------------- |
| new cc.Menu(item1, item2, ...)                        |                             |
| menu.alignItemsVertically()                           |                             |
| menu.alignItemsInColumns(col0_count, col1_count, ...) | 第0列有col0_count个item，…… |
| menu.children                                         | 所有MenuItem                |

## cc.MenuItemSprite

```js
var item1 = new cc.MenuItemSprite(normal, selected, disabled, callback, this);
```

## cc.MenuItemImage

```js
var item2 = new cc.MenuItemImage(normal, selected, disabled, callback, this);

var item2 = new cc.MenuItemImage("#normalName", "#selectedName", callback, this);
```

## cc.MenuItemLabel

```js
var item3 = new cc.MenuItemLabel(label, callback, this);
```

## cc.MenuItemFont

```js
var item = new cc.MenuItemFont("title", callback, this);
item.fontName = "Arial";
item.fontSize = 32;
item.setString("title");
```

## cc.MenuItemToggle

```js
var toggler = new cc.MenuItemToggle(menuItem1, menuItem2, ..., callback, this);
```



# Event

基本原则：自己添加的事件，必须显式移除。

## 单点触摸

```js
if( 'touches' in cc.sys.capabilities ) {
    cc.eventManager.addListener({
        event: cc.EventListener.TOUCH_ONE_BY_ONE,
        swallowTouches: true,
        onTouchBegan: this.onTouchBegan,
        onTouchMoved: this.onTouchMoved,
        onTouchEnded: this.onTouchEnded,
        onTouchCancelled: this.onTouchCancelled
    }, this);
}

onTouchBegan:function(touch, event) {
    touch.getLocation(); //世界坐标，原点在左下角
    touch.getID();
    event.getCurrentTarget();
    return true;
}
```

## 多点触摸

```js
if( 'touches' in cc.sys.capabilities ) {
    cc.eventManager.addListener({
        event: cc.EventListener.TOUCH_ALL_AT_ONCE,
        onTouchesBegan: this.onTouchesBegan,
        onTouchesMoved: this.onTouchesMoved,
        onTouchesEnded: this.onTouchesEnded,
        onTouchesCancelled: this.onTouchesCancelled
    }, this);
}

onTouchesBegan:function(touches, event) {
    for (var i=0; i < touches.length;i++ ) {
        var touch = touches[i];
    }
    //不需要返回值
},
```

## 加速器

```js
if( 'accelerometer' in cc.sys.capabilities ) {
    var self = this;
    // call is called 30 times per second
    cc.inputManager.setAccelerometerInterval(1/30); //加速器回调的调用间隔
    cc.inputManager.setAccelerometerEnabled(true);
    cc.eventManager.addListener({
        event: cc.EventListener.ACCELERATION,
        callback: function(accelEvent, event){
            accelEvent.x;
            accelEvent.y;
            accelEvent.z;
            accelEvent.timestamp;
        }
    }, this);
}
```

## 鼠标事件

```js
if( 'mouse' in cc.sys.capabilities ) {
    cc.eventManager.addListener({
        event: cc.EventListener.MOUSE,
        onMouseDown: function(event){
            
            //原点在屏幕左下角
            var pos = event.getLocation();
            
            var target = event.getCurrentTarget();
            
            //cc.EventMouse.BUTTON_LEFT
            //cc.EventMouse.BUTTON_RIGHT
            //cc.EventMouse.BUTTON_MIDDLE
            event.getButton();
        },
        onMouseMove: function(event){
        },
        onMouseUp: function(event){
        }
    }, this);
}
```

## 键盘事件

```js
if ('keyboard' in cc.sys.capabilities) {
    cc.eventManager.addListener({
        event: cc.EventListener.KEYBOARD,
        onKeyPressed: function (keycode, event) {
            //keycode===cc.KEY
        },
        onKeyReleased: function (keycode, event) {
            
        }
    }, this);
}
```

## 自定义事件

```js
//1.定义事件唯一标识符
var MyEventName = "game_custom_event1";

//2.注册事件接收器
this._listener1 = cc.EventListener.create({
    event: cc.EventListener.CUSTOM,
    eventName: MyEventName,
    callback: function(event){
        event.getUserData();
    }
});
cc.eventManager.addListener(this._listener1, 1);

//3.发射事件
var event = new cc.EventCustom(MyEventName);
event.setUserData(data);
cc.eventManager.dispatchEvent(event);

//4.onExit时移除事件接收器
cc.eventManager.removeListener(this._listener1);
```

## Director事件

```js
//添加事件监听
//EVENT_AFTER_UPDATE
//EVENT_AFTER_VISIT
//EVENT_AFTER_DRAW
//EVENT_PROJECTION_CHANGED
this._event1 = cc.eventManager.addCustomListener(cc.Director.EVENT_AFTER_UPDATE, function(event){
    
});

cc.eventManager.removeListener(this._event1);
```



## 其他接口

```js
//priority越小，优先级越高
cc.eventManager.addListener(listener, nodeOrPriority);

cc.eventManager.removeListener(listener1);

//移除游戏中所有的事件，会导致所有按钮不可用，一般用不到这个方法
cc.eventManager.removeAllListeners();

//暂停node的所有事件监听
cc.eventManager.pauseTarget(node, recursive);

//停止事件继续传播
event.stopPropagation();

//关闭监听或打开继续监听
listener.setEnabled(enabled);
```

# Scene

运行场景

```js
//替换当前正运行的scene
director.runScene(scene);
director.runScene(new cc.TransitionSlideInT(seconds, scene));

//scene入栈
director.pushScene(scene);
director.pushScene(new cc.TransitionSlideInT(seconds, scene));

//scene出栈
director.popScene();
```

添加常驻节点

```js
//场景切换时，所有的内容都会被删除
//如果希望有常驻的节点，例如悬浮窗，可以通过此接口设置。
cc.director.setNotificationNode(node);
cc.director.setNotificationNode(null);
```

事件回调

```js
//当场景切换动画完成时被调用
cc.Node.onEnterTransitionDidFinish();
```

# Label

## cc.LabelAtlas

```js
var label1 = new cc.LabelAtlas("title", "fonts/tuffy_bold_italic-charmap.plist");

label1.setString("title");
```

## cc.LabelBMFont

```js
var label1 = new cc.LabelBMFont("title", "fonts/bitmapFontTest2.fnt");

//可以针对每个字符做操作，只有LabelBMFont支持
var char0 = label1.getChildByTag(0);

//水平对齐方式：cc.TEXT_ALIGNMENT_LEFT|cc.TEXT_ALIGNMENT_CENTER|cc.TEXT_ALIGNMENT_RIGHT
//LabelBMFont没有垂直对齐
label1.textAlign;

//整个label的宽度
label1.boundingWidth;

//文字部分的宽高
label1.width;
label1.height;
```

## cc.LabelTTF

```js
var label = new cc.LabelTTF("title", fontName="Arial", fontSize=16, blockSize= cc.size(0,0), horizAlign=cc.TEXT_ALIGNMENT_LEFT, vertAlign=cc.VERTICAL_TEXT_ALIGNMENT_TOP);

//文字部分的大小
label.boundingWidth;
label.boundingHeight;

//设置整体框大小
label.setDimensions(width, height);

//cc.TEXT_ALIGNMENT_LEFT|cc.TEXT_ALIGNMENT_CENTER|cc.TEXT_ALIGNMENT_RIGHT
label.setHorizontalAlignment(halign);
//cc.VERTICAL_TEXT_ALIGNMENT_TOP|cc.VERTICAL_TEXT_ALIGNMENT_CENTER|cc.VERTICAL_TEXT_ALIGNMENT_BOTTOM
label.setVerticalAlignment(valign);

```

字体阴影

```js
// font definition
var fontDef = new cc.FontDefinition();
fontDef.fontName = "Arial";
fontDef.fontSize = 32;
fontDef.textAlign = cc.TEXT_ALIGNMENT_LEFT;
fontDef.verticalAlign = cc.VERTICAL_TEXT_ALIGNMENT_TOP;
fontDef.fillStyle = cc.color(255,255,233);
fontDef.boundingWidth = 300;
fontDef.boundingHeight = 200;
// shadow
fontDef.shadowEnabled = true;
fontDef.shadowOffsetX = 6;
fontDef.shadowOffsetY = -3;
// stroke，只在移动设备上支持
fontDef.strokeEnabled = true;
fontDef.strokeStyle = cc.color(0,0,0);

var label = new cc.LabelTTF("title", fontDef);
```

# Node

```js
//rect.origin是node左下角的坐标
var rect = node.getBoundingBox();

//重排子节点的zOrder
node.reorderChild(child, newZOrder);
```

# Sprite

```js
var sprite = new cc.Sprite("image.png");
var sprite = new cc.Sprite(texture);
var sprite = new cc.Sprite("#grossini_dance_01.png"); //从cc.spriteFrameCache中选取一张图片

//设置混合函数
//src:cc.ZERO, cc.ONE, cc.DST_COLOR, cc.ONE_MINUS_DST_COLOR, cc.DST_ALPHA, cc.ONE_MINUS_DST_ALPHA
//dst:cc.ZERO, cc.ONE, cc.SRC_COLOR, cc.ONE_MINUS_SRC_COLOR, cc.SRC_ALPHA, cc.ONE_MINUS_SRC_ALPHA
sprite.setBlendFunc(src, dst);
```



# scheduler

## 内置的定时类

* cc.Scheduler：
  * 定时器管理类，可以new出多个对象，cc.director有一个总定时器对象
* cc.ActionManager：
  * Action管理类，可以new出多个对象，cc.director.scheduler有一个总Action管理类

## 主要接口

如果对一个函数多次注册，则只有最后一次注册的会有效。

```js
var scheduler = cc.director.getScheduler();

//注册自定义的回调函数
scheduler.schedule(this.callback, this, interval, paused);

//注册update回调，每帧回调一次
scheduler.scheduleUpdateForTarget(target, priority, paused);
scheduler.unscheduleUpdateForTarget(target);

//暂停/开始所有的更新事件，包括update、selector等
scheduler.pauseTarget(target);
scheduler.resumeTargets(target);

//取消所有回调，包括update和自定义回调
scheduler.unscheduleAllCallbacks();
scheduler.unscheduleAllCallbacksForTarget(target);
//只取消update回调
scheduler.unscheduleUpdate();
scheduler.unscheduleUpdateForTarget(target);

//数值越小，更新越慢
scheduler.setTimeScale(1.0);
```

## 创建多个scheduler

```js
this._newScheduler = new cc.Scheduler();
this._newActionManager = new cc.ActionManager();

node.setActionManager(this._newActionManager);
node.setScheduler(this._newScheduler);

cc.director.getScheduler().scheduleUpdateForTarget(this._newScheduler, 0, false);
this._newScheduler.scheduleUpdateForTarget(this._newActionManager, 0, false);
```

## cc.Node提供的接口

```js
//将node绑定到callback的this上
//内部调用了cc.director.getScheduler().scheduleUpdateForTarget(this, 0, false);
node.schedule(callback, tick_seconds=0, tick_count=4294967294);

node.scheduleUpdate();
node.scheduleUpdateWithPriority(priority);

node.unscheduleAllCallbacks();

```

# 坐标转换

* 世界坐标
* 屏幕坐标
* 局部坐标

```js
//返回的localpos为相对于(0,0)点的坐标
var localpos = node.convertToNodeSpace(worldpos);

//anchor relative，返回的localpos为相对于anchor的坐标
var localpos = node.convertToNodeSpaceAR(worldpos);
```

