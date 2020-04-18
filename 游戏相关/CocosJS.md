# 前言

本篇文章以cocos2d-x v3.16为基础，总结了开发中常用的概念及代码片段。

只涉及js-binding部分。

官方文档：https://docs.cocos2d-x.org/api-ref/js/v3x/index.html

# 项目结构介绍

以js HelloWorld项目为例

* frameworks：cocos本身的所有文件
* simulator：编译后生成的可执行文件
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

类型

| 名称                  | 作用                           |
| --------------------- | ------------------------------ |
| Point/Size/Rect/Color |                                |
| Class                 | cc为实现js面向对象提供的功能类 |
| Action/...            | 动作类                         |
| Event/...             | 事件类                         |
| GridBase/...          |                                |
| Node/...              |                                |

## ccs

CocosStudio功能支持

## ccui

cocos的亲儿子UI部分

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



# 适配设置

```javascript
cc.view.enableRetina(false);

//cc.ORIENTATION_PORTRAIT 相当于ORIENTATION_LANDSCAPE_LEFT
//cc.ORIENTATION_LANDSCAPE_LEFT home键在右
//cc.ORIENTATION_LANDSCAPE_RIGHT
//cc.ORIENTATION_PORTRAIT
//cc.ORIENTATION_PORTRAIT_UPSIDE_DOWN
cc.view.setOrientation(cc.ORIENTATION_LANDSCAPE);

//设置了设计分辨率之后，相当于通知了cocos，该以什么比例缩放整个scene。
//EXACT_FIT FIXED_HEIGHT FIXED_WIDTH NO_BORDER SHOW_ALL UNKNOWN
cc.view.setDesignResolutionSize(800, 450, cc.ResolutionPolicy.SHOW_ALL);

//当浏览器大小改变的时候，canvas的大小自动随之改变
cc.view.resizeWithBrowserSize(true);
```

下面这些接口，取得的数据都是逻辑单位

```js
//取得窗口大小
cc.director.getWinSize();

//一般情况下，visibleSize和winSize是一样的，只有对当前scene做了变换操作才会导致不一样。
//当前scene的可视范围
cc.director.getVisibleSize();
//当前scene的可视原点
cc.director.getVisibleOrigin();
```

# Action

## Node属性动画类

| 方法                    | 作用 |
| ----------------------- | ---- |
| cc.moveBy/cc.moveTo     |      |
| cc.bezierBy/cc.bezierTo |      |
| cc.fadeIn/cc.fadeOut    |      |

```js
var act = cc.moveBy(2, cc.p(100,100));
node.runAction(act);
node2.runAction(act.clone());
```

## ProgressTimer属性动画类

只能作用在cc.ProgressTimer对象上

| 方法              | 作用 |
| ----------------- | ---- |
| cc.progressFromTo |      |
| cc.progressTo     |      |

```js
var action = cc.progressFromTo(2, 0, 100);
var progress = new cc.ProgressTimer(new cc.Sprite("*.png"));

//cc.ProgressTimer.TYPE_RADIAL 时钟动画
//cc.ProgressTimer.TYPE_BAR 进度条动画
progress.type = cc.ProgressTimer.TYPE_BAR;

//false: 从左向右、顺时针
progress.reverseDir = true;

//动画的起始点
progress.midPoint = cc.p(x, y);

//x,y的范围为[0,1]，0代表此方向上没有动画，1代表完全动画
progress.barChangeRate = cc.p(x, y);

progress.runAction(action);
```

## 立即设置属性类

| 方法                | 作用            |
| ------------------- | --------------- |
| cc.place            | 直接设置位置    |
| cc.hide/cc.show     |                 |
| cc.toggleVisibility | 切换visible属性 |
| cc.removeSelf       | 移除自身        |

```js
var act = cc.hide();
node.runAction(act);
```



## 动作组合类

| 方法        | 作用     |
| ----------- | -------- |
| cc.sequence | 依次运行 |
| cc.spawn    | 同时运行 |

```js
var act1 = cc.moveBy(2, 100, 100);
var act2 = cc.blink(3, 5);
var comb = cc.spawn(act1, act2);
node.runAction(comb);
```



## 网格动画类

| 方法       | 作用 |
| ---------- | ---- |
| cc.shaky3D |      |
| cc.waves   |      |

```js
var nodeGrid = new cc.NodeGrid();

nodeGrid.addChild(child);

nodeGrid.runAction(cc.shaky3D( duration, cc.size(15,10), 5, false ));
```

nodeGrid本身没有显式效果，所有效果会作用在nodeGrid的所有子节点上。

## 节奏控制类

| 方法           | 作用                 |
| -------------- | -------------------- |
| cc.ActionEase* | 控制action的运动节奏 |
| cc.delayTime   | 延时                 |

```js
var move = cc.moveBy(2, 100, 100);
var move_ease_in = move.clone().easing(cc.easeIn(2.0));
node.runAction(move_ease_in);
```



## 其他

| 方法                                                         | 作用                   |
| ------------------------------------------------------------ | ---------------------- |
| cc.targetedAction(node, action)                              | 强制在node上执行action |
| cc.callFunc(func(action, arg0, arg1, ...), node, arg0, arg1, ...) |                        |
| cc.follow(target, follow_rect)                               | 跟随target             |

## Action本身的接口

| 方法                        | 作用                           |
| --------------------------- | ------------------------------ |
| action.clone()              | 返回克隆对象                   |
| action.reverse()            | 返回反过程                     |
| action.repeat(repeat_count) | 返回重复执行对象               |
| action.repeatForever()      | 返回永远重复的动作             |
| action.easing(eas_action)   | 返回使用了eas_action效果的动作 |

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

# MotionStreak

拖尾效果

```js
//fade_seconds=一个treak item经过多长时间消失
//minimum_segment_size=target移动多少，产生一个treak item
//texture_size=拖尾的大小，像素单位
//color=拖尾的颜色
//texture_or_texturename=拖尾使用的图
var streak = new cc.MotionStreak(fade_seconds, minimum_segment_size, texture_size, color, texture_or_texturename);

//当streak的位置改变时，会生成拖尾效果
streak.setPosition(worldLocation);
```



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
var toggler = new cc.MenuItemToggle(menuItem1, menuItem2, ..., function (){
    switch (sender.getSelectedIndex()) {
        case 0:
            break;
        case 1:
            break;
        case 2:
            break;
    }
    
    sender.getSubItems();
    sender.addSubItem(item);
}, this);
```

# ccui.Widget

## 通用接口

所有继承了ccui.Widget的类，都可以使用以下接口

```js
//进入disable状态，图像会变灰
widget.setEnabled(false);
//不进入disable状态，但图像仍变灰
widget.setBright(false);

//使用九宫格图
//capInsets: cc.rect 四个数字分别代表左侧宽，上边高，右侧宽，下边高
widget.setScale9Enabled(true);
widget.setCapInsets(capInsets);


```

## ccui.Button

```js
var button = new ccui.Button("normal.png", "pressed.png", "disabled.png");
button.loadTextures("normal.png", "pressed.png", "disabled.png");

//事件监听1
button.addTouchEventListener(function (sender, type){
    switch (type) {
        case ccui.Widget.TOUCH_BEGAN:
            break;
        case ccui.Widget.TOUCH_MOVED:
            break;
        case ccui.Widget.TOUCH_ENDED:
            break;
        case ccui.Widget.TOUCH_CANCELED:
            break;
        default:
            break;
    }
}, this);
//事件监听2
button.addClickEventListener(function (sender) {
    
});

//点击时伴随缩放效果
button.setPressedActionEnabled(true);
//负数是向小缩
button.setZoomScale(-0.05);

//设置文字
button.setTitleText("Title Button");

//默认为true，表示按钮忽略本身的大小，而使用纹理的大小来调整title位置
button.ignoreContentAdaptWithSize(false);

//返回代表title的cc.LabelTTF
var title = button.getTitleRenderer();

```

## ccui.CheckBox

```js
var checkBox = new ccui.CheckBox("normal.png", "checked.png");

checkBox.addEventListener(function(sender, type){
    switch (type) {
        case ccui.CheckBox.EVENT_UNSELECTED:
            break;
        case ccui.CheckBox.EVENT_SELECTED:
            break;
    }
}, this);

checkBox.setSelected(true);
```

## ccui.Slider

```js
var slider = new ccui.Slider();
slider.loadBarTexture("back.png");
slider.loadSlidBallTextures("ballNormal.png", "ballPressed.png", "ballDisable.png");
slider.loadProgressBarTexture("covered.png");

slider.addEventListener(function (sender, type){
    switch (type) {
        case ccui.Slider.EVENT_PERCENT_CHANGED:
            var percent = sender.getPercent();
            break;
    }
}, this);

```

## ccui.ImageView

```js
var imageView = new ccui.ImageView("image.png");
imageView.loadTexture("image.png");
```

## ccui.LoadingBar

```js
var loadingBar = new ccui.LoadingBar();
loadingBar.loadTexture("ccs-res/cocosui/sliderProgress.png");
//percent: [0,100]
loadingBar.setPercent(percent);

//ccui.LoadingBar.TYPE_LEFT: 从左到右 默认
//ccui.LoadingBar.TYPE_RIGHT: 从右到左
loadingBar.setDirection(ccui.LoadingBar.TYPE_RIGHT);
```

## ccui.ScrollView

```js
var scrollView = new ccui.ScrollView();
//ccui.ScrollView.DIR_HORIZONTAL
//ccui.ScrollView.DIR_VERTICAL
//ccui.ScrollView.DIR_BOTH
//ccui.ScrollView.DIR_NONE
scrollView.setDirection(ccui.ScrollView.DIR_VERTICAL);
scrollView.setTouchEnabled(true);
scrollView.setContentSize(cc.size());

//设置所有子节点的大小
scrollView.setInnerContainerSize(cc.size());

//添加子节点
scrollView.addChild(node);
```



## box布局

```js
var layout = new ccui.HBox();
var layout = new ccui.VBox();

layout.setFocused(true); //当用户点击键盘方向键时，会发送cc.EventListener.FOCUS
layout.setLoopFocus(true);

//如果要让layout的setFocused起作用，node必须调用node.setFocusEnabled(true);
layout.addChild(node);

//注册事件监听
cc.eventManager.addListener({
    event: cc.EventListener.FOCUS,
    onFocusChanged: function(widgetLostFocus, widgetGetFocus){
        widgetLostFocus.isFocusEnabled();
        widgetGetFocus.isFocusEnabled();
    }
}, this);
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
            
            event.getDeltaX();
            event.getDeltaY();
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

## 图片浏览事件

```js
cc.eventManager.addListener({
    event: cc.EventListener.FOCUS,
    onFocusChanged: function(widgetLostFocus, widgetGetFocus){
        widgetLostFocus.isFocusEnabled();
        widgetGetFocus.isFocusEnabled();
    }
}, this);
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
cc.eventManager.addListener(this._listener1, nodeOrPriority);

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
//EVENT_AFTER_UPDATE update后发送
//EVENT_AFTER_VISIT visit后发送
//EVENT_AFTER_DRAW draw后发送
//EVENT_PROJECTION_CHANGED 投影矩阵改变后发送
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

## 运行场景

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

## 添加常驻节点

```js
//场景切换时，所有的内容都会被删除
//如果希望有常驻的节点，例如悬浮窗，可以通过此接口设置。
cc.director.setNotificationNode(node);
cc.director.setNotificationNode(null);
```

## 场景切换事件

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
var label = new cc.LabelTTF("title", fontDef);
//offset: cc.p
//blurSize: [0,1]
label.enableShadow(shadowColor, offset, blurSize);
```

# cc.TextField

```js
var textField = new cc.TextFieldTTF(placeholder, fontName, fontSize);

textField.setDelegate(this);

textField.setString("text");
textField.getString("text");
```

# Node

## cc.Node

```js
//rect.origin是node左下角的坐标
var rect = node.getBoundingBox();

//重排子节点的zOrder
node.reorderChild(child, newZOrder);
```

## cc.ClippingNode

```js
var clipper = new cc.ClippingNode();
//默认是false，只显示模板以内的部分。如果是true，只显示模板外的部分
clipper.setInverted(true);
//
clipper.alphaThreshold = 1;
this.addChild(clipper);

var stencil = new cc.DrawNode();
clipper.stencil = stencil;

var content = new cc.Sprite("sprite.png");
clipper.addChild(content);
```

## cc.DrawNode

```js
var draw = new cc.DrawNode();
this.addChild(draw);

draw.drawDot(pos, radius, color);
draw.drawRect(origin, destination, fillColor, lineWidth, lineColor);
draw.drawSegment(from, to, lineWidth, color);
draw.drawCircle(center, radius, angle, segments, drawLineToCenter, lineWidth, color);
```

## cc.ParallaxNode

景深效果

```js
var voidNode = new cc.ParallaxNode();

//ratio: cc.p 当voidNode移动(x,y)时，node只移动(ratio.x*x, ratio.y*y)
//offset: cc.p(0,0)
voidNode.addChild(node, zOrder, ratio, offset);

```



# Sprite

## cc.Sprite

```js
var sprite = new cc.Sprite("image.png");
var sprite = new cc.Sprite(texture);
var sprite = new cc.Sprite("#grossini_dance_01.png"); //从cc.spriteFrameCache中选取一张图片

//设置混合函数
//src:cc.ZERO, cc.ONE, cc.DST_COLOR, cc.ONE_MINUS_DST_COLOR, cc.DST_ALPHA, cc.ONE_MINUS_DST_ALPHA
//dst:cc.ZERO, cc.ONE, cc.SRC_COLOR, cc.ONE_MINUS_SRC_COLOR, cc.SRC_ALPHA, cc.ONE_MINUS_SRC_ALPHA
sprite.setBlendFunc(src, dst);
```

## cc.Scale9Sprite

```js
//会优先从cc.spriteFrameCache中提取文件
var blocks = new cc.Scale9Sprite('blocks9.png');

//capInsets:cc.rect 四个数字分别代表左侧宽，上边高，右侧宽，下边高
var blocks = new cc.Scale9Sprite();
blocks.updateWithBatchNode(cc.SpriteBatchNode, originalRect, rotated, capInsets);
```

## cc.SpriteBatchNode

```js
var batch = new cc.SpriteBatchNode("sprite.png");
var sprite = new cc.Sprite(batch.texture);
batch.addChild(sprite);
```

# Particle

```js
var particleSystem = new cc.ParticleSystem("particle.plist");
particleSystem.setAutoRemoveOnFinish(true);
this.addChild(particleSystem);
```

# RenderTexture

RenderTexture在每帧开始不会自动clear，所以画在上面的内容会一直保留。

```js
var renderTexture = new cc.RenderTexture(winSize.width, winSize.height);
this.addChild(renderTexture); //也可以没有这一步

renderTexture.begin();
sprite.visit(); //sprite只渲染到target上
renderTexture.end();

//
renderTexture.clear(r, g, b, a);

//format: cc.IMAGE_FORMAT_PNG cc.IMAGE_FORMAT_JPEG
renderTexture.saveToFile(filename, format);
```

# Scheduler

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

//key: [string] 唯一标识符，可以不填
node.scheduleOnce(callback, delay, key);

node.scheduleUpdate();
node.scheduleUpdateWithPriority(priority);

node.unscheduleAllCallbacks();

```

# AudioEngine

## 播放背景音乐

```js
//播放/停止
cc.audioEngine.playMusic("music.mp3", loop);
cc.audioEngine.stopMusic();

//暂停/继续
cc.audioEngine.pauseMusic();
cc.audioEngine.resumeMusic();

//重新从头播放音乐
cc.audioEngine.rewindMusic();

//
cc.audioEngine.isMusicPlaying();

//设置音效声音，范围[0,1]
cc.audioEngine.setMusicVolume(cc.audioEngine.getMusicVolume() + 0.1);
```

## 播放音效

```js
//播放/停止
var soundId = cc.audioEngine.playEffect(EFFECT_FILE, loop);
cc.audioEngine.stopEffect(soundId);
cc.audioEngine.stopAllEffects();

//暂停/继续
cc.audioEngine.pauseEffect(soundId);
cc.audioEngine.resumeEffect(soundId);

//暂停所有音效
cc.audioEngine.pauseAllEffects();
cc.audioEngine.resumeAllEffects();

//
cc.audioEngine.unloadEffect(EFFECT_FILE);

//设置音效声音，范围[0,1]
cc.audioEngine.setEffectsVolume(cc.audioEngine.getEffectsVolume() + 0.1);
```

# Loader

## 直接加载资源

results存储了资源对应的cocos对象。

```js
var res = ["a.png", "b.png"];
cc.loader.load(res, function(err, results){
    if(err){
        cc.log("Failed to load %s.", res);
        return;
    }
});

//加载完成后，可以通过getRes得到
cc.loader.getRes(name);

//如果不想要，可以通过release释放
cc.loader.release(name);
```

## 加载图集

加载到cc.spriteFramesCache

```js
cc.loader.loadAliases("name.plist", function(){
    var sprite = new cc.Sprite("grossini.bmp");
    self.addChild( sprite, 100);
    sprite.x = winSize.width/2;
    sprite.y = winSize.height/2;
});
```

## 加载自定义文件

```js
cc.loader.register(["mpx"], {
    load: function(realUrl, url, res, cb){
        
        //此函数只负责一个url的加载
        //如果调用者用数组调用load方法，则cocos会合并每个资源的加载结果并返回给调用者
        
        //调用者-->cocos-->load
        
        //realUrl: 可以传递给文件系统使用的文件名
        //url: 调用者传递的参数
        //res: 
        //cb(error, results): 当所有内容加载完成后，用此函数通知cocos已经加载完成，cocos会处理接下来的步骤。
    }
});

cc.loader.load(["data.mpx"], function(error, results){
    if(err){
        cc.log("Failed to load data.mpx");
        return;
    }
});
```

# cc.sys.localStorage

```js
cc.sys.localStorage.setItem(key, value);

var value = cc.sys.localStorage.getItem(key);

cc.sys.localStorage.removeItem(key);

cc.sys.localStorage.clear();
```



# Component

创建组件

```js
var Player = cc.ComponentJS.extend({
    onEnter: function() {
        var owner = this.getOwner();
    }
});
```

使用组件

```js
var playerComponent = new cc.ComponentJS("src/ComponentTest/player.js");
node.addComponent(playerComponent);
```

# jsb.fileUtils

```js
jsb.fileUtils.addSearchPath(path);
jsb.fileUtils.setSearchPath(paths);

jsb.fileUtils.getWritablePath();
```

# 骨骼动画

```js
var spineBoy = new sp.SkeletonAnimation('spineboy.json', 'spineboy.atlas');

spineBoy.setMix(from_name, to_name, duration_seconds);
spineBoy.setMix('jump', 'run', duration_seconds);

//在trackIndex轨上播放animation_name动画
spineBoy.setAnimation(trackIndex, animation_name, loop);

var trackEntry = spineBoy.getCurrent();

//改变动画播放速度
spineBoy.setTimeScale(1.0);

//设置蒙皮，可以不设置，直接使用默认蒙皮
spineBoy.setSkin("goblin");

spineBoy.setStartListener(function(trackEntry){
});
spineBoy.setEndListener(function(trackEntry){
});
spineBoy.setCompleteListener(function(trackEntry){
});
spineBoy.setEventListener(function(trackEntry, event){
});
```

## TrackEntry的接口

```js
trackEntry.animation;
trackEntry.animation.name;

trackEntry.trackIndex;

//这一轨已经播放了多长时间
trackEntry.trackTime;

//这一轨的动画时长
trackEntry.animationEnd;
```



# cc.sys

## cc.sys.language

```js
switch(cc.sys.language)
{
    case cc.sys.LANGUAGE_ENGLISH:
        break;
    case cc.sys.LANGUAGE_CHINESE:
        break;
}
```

## cc.sys.capabilities

cc.sys.capabilities是一个字符串列表

* canvas: 是否web环境
* opengl: 是否使用opengl环境
* keyboard: 是否支持键盘
* touch: 是否支持触摸
* mouse: 是否支持鼠标

## cc.sys.openURL

在系统浏览器中打开网址

```js
cc.sys.openURL("http://www.cocos2d-x.org/");
```



# 坐标转换

```js
//返回的localpos为相对于(0,0)点的坐标
var localpos = node.convertToNodeSpace(worldpos);

//anchor relative，返回的localpos为相对于anchor的坐标
var localpos = node.convertToNodeSpaceAR(worldpos);
```

# 图像格式

* Image: 存在硬盘上的图片
* Texture: 加载Image后，存在GPU中的纹理
* SpriteFrame: Texture中的一部分 = Texture+Rect

# 内置缓存

## cc.textureCache

```js
cc.textureCache.addImageAsync(url, function(texture){
}, this);
```

## cc.spriteFrame

```js
cc.spriteFrame.addSpriteFrame(SpriteFrame, name);

cc.spriteFrame.addSpriteFrame(plist);
```

# 网络

## XMLHttpRequest

完整API参考: https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest

```js
var xhr = cc.loader.getXMLHttpRequest();

xhr.timeout = 5000;

//set arguments with <URL>?xxx=xxx&yyy=yyy
xhr.open("GET", "http://httpbin.org/gzip", async_bool);
xhr.setRequestHeader("Accept-Encoding","gzip,deflate");

xhr.onloadstart = function(){
}
xhr.onabort = function(){
}
xhr.onerror = function(){
}
xhr.onload = function(){
}
xhr.onloadend = function(){
}
xhr.ontimeout = function(){
}
xhr.onreadystatechange = function(){
    //4==下载操作已经完成
    if (xhr.readyState == 4 && (xhr.status >= 200 && xhr.status <= 207)) {
        xhr.responseText;
    }
}

xhr.send();
xhr.send(new Uint8Array([1,2,3,4,5])); //用于post方式
```

## SocketIO

```js
var sioclient = SocketIO.connect("ws://tools.itharbors.com:4000");

sioclient.on("connect", function() {
});
sioclient.on("message", function(data) {
});
sioclient.on("disconnect", function() {
});

sioclient.send("Hello Socket.IO!");
```

