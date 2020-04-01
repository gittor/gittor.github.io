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

和运行action有关的接口

| 方法                      | 作用 |
| ------------------------- | ---- |
| cc.Node.runAction(action) |      |
|                           |      |
|                           |      |

Action本身的接口

| 方法             | 作用 |
| ---------------- | ---- |
| action.clone()   |      |
| action.reverse() |      |
|                  |      |

各种不同的Action

| 方法                                | 作用       |
| ----------------------------------- | ---------- |
| cc.moveTo(seconds, pos, posY)       |            |
| cc.scaleTo(seconds, scaleX, scaleY) |            |
| cc.rotateTo(seconds, degree)        | 顺时针旋转 |
| cc.delayTime(seconds)               |            |
|                                     |            |



# Layer

纯色Layer

```javascript
//如果没有设置宽高，则为canvas大小
cc.LayerColor(cc.color, with=undefined, height=undefined)
```

渐变Layer

```js
//gradient_dir
cc.LayerGradient(startcolor, endcolor, gradient_dir=cc.p(0,-1))
```

# **cc.sys**