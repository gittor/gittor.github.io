# 前言

总结Unity开发中常用的概念、做法、代码片段等。

以Unity 2019.03版本为研究对象。

# 2D项目

1. 设置Game面板的预览窗口大小(1136x768)。
2. 相机投影模式(Projection)：Orthographic。
3. 相机Size(1136/2=568)。
4. 在Scene里添加Canvas，设置渲染模式为World Space，修改Canvas大小(1136x768)。



1. 原点在左下角

# vs项目

* 生成sln：Edit->Preference->External Tool->Regenerate project files。
* 调试：
  * 下载vs2017 for unity：工具->获取工具和功能->安装unity支持包。
  * 调试->附加unity调试程序。

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
//屏幕坐标，原点为游戏窗口的左下角，最大值为游戏窗口的右上角(Screen.width,Screen.height)
//使用时需要转换成世界坐标
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
//屏幕坐标，左下角为原点，最小单位为像素
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

# GameObject操作

```c#
obj.localPosition; //局部坐标
obj.position; //全局坐标
```

# 坐标转换

世界坐标vs局部坐标

```c#
obj.transform.TransformPoint(localPoint); //局部坐标转成世界坐标
obj.transform.InverseTransformPoint(worldPoint); //世界坐标转成局部坐标
```

屏幕坐标vs世界坐标

```c#
Camera.main.ScreenToWorldPoint(Input.mousePosition); //屏幕坐标转成世界坐标
Camera.main.WorldToScreenPoint(worldPosition); //世界坐标转成屏幕坐标
```

# 屏幕适配

# 动画

## 添加动画

1. 选中要添加动画的物体，按ctrl+6。
2. 添加动画并保存，会生成.anim和.controller两个文件。