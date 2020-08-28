# 前言

总结Unity开发中常用的概念、做法、代码片段等。

以Unity 2019.03版本为研究对象。

# 用户输入

Unity中有两套输入系统：

* Input Manager：Unity原生的输入系统，比较原始。
* Input System：提供了更高级的接口。一个功能包，使用前需要先下载。需要.Net 4以上的环境。

## Input Manager

Input Manager的所有API都在Input类中。

### 鼠标事件

鼠标事件在移动设备上也可以使用，可以用来模拟单指触摸。

```c#
//buttonIndex：0==鼠标左键；1==鼠标滚轮；2==鼠标右键
bool Input.GetMouseButton(buttonIndex);
bool Input.GetMouseButtonDown(buttonIndex);
bool Input.GetMouseButtonUp(buttonIndex);

//取得鼠标的当前位置
//原点为游戏窗口的左下角，最大值为游戏窗口的右上角(Screen.width,Screen.height)
Vector3 Input.mousePosition;

//设置鼠标显示模式
//CursorLockMode.Locked 鼠标不可见，位置一直居中于游戏窗口
//CursorLockMode.Confined 鼠标不能移出游戏窗口
//CursorLockMode.None 鼠标可以移出游戏窗口
CursorLockMode Cursor.lockState;
```

### 触摸事件

```c#
//取得当前所有的触摸信息
Touch[] Input.touches;

//开启或禁用多点触摸
bool Input.multiTouchEnabled;
```

#### Touch

```c#
//TouchPhase.Begin 按下时触发
//TouchPhase.Moved 移动手指时触发
//TouchPhase.Stationary 在触摸屏幕但没有移动
//TouchPhase.Ended 触摸完成
//TouchPhase.Canceled 取消触摸
touch.phase;

//Vector2
//屏幕左下角为原点，最小单位为像素
touch.position;

//自上次更新到本次更新的差值
touch.deltaTime;
touch.deltaPosition;

//可以用来检测双击，双击时值为2
int touch.tapCount;

//触摸信息的唯一标识
int touch.fingerId;
```

### 键盘事件

### 轴事件

轴事件的处理分为2部分：

1. 在**Edit > Project Settings**中设置虚拟轴
2. 使用**Input**接口处理事件

轴接口一共分两种：

用于处理平滑移动类输入的接口

```c#
//返回值在[-1,1]之间
float Input.GetAxis(string axisName);
```

用于处理即时事件类输入的接口，例如开火按钮等。

```c#
bool Input.GetButton(string buttonName); //当buttonName按下时每次调用都返回true
bool Input.GetButtonDown(string buttonName); //按下时触发一次
bool Input.GetButtonUp(string buttonName); //松开时触发一次
```

