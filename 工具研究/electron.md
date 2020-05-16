# 前言

总结使用electron开发桌面应用的方方面面。

## 工具链说明

| 工具      | 文档                             | 版本    | 安装方式         |
| --------- | -------------------------------- | ------- | ---------------- |
| Node      | https://nodejs.org/zh-cn/docs/   | 12.16.1 | 下载二进制包安装 |
| electron  | https://www.electronjs.org/docs  | 8.11    | 不需要手动操作   |
| vue       | https://cn.vuejs.org/v2/guide/   | 2.6     | cdn引入          |
| ElementUI | https://element.eleme.cn/#/zh-CN |         | cdn引入          |

## 为什么使用electron
* 优点：跨平台，技术有前景，轻量。
* 缺点：
  * 发布包很大：由于是桌面应用，所以对发布包大小不是特别敏感
  * UI响应不如native应用迅速：在可接受范围内
  * 需要有前端开发经验：这就是需要阅读本教程的原因

## 前端框架的选择
前端开发有两种方式：

* 一种是不使用任何框架，纯html+css+js开发。这种方式方式太原始，并且较少社区资源支持。
* 另一种是选择一种前端框架，如react、vue等。我们选择的是vue。

vue的优点
* 响应式：数据值改变，自动同步到界面元素。
* html逻辑：在html里直接写简单的显示逻辑，不用再拼html字符串。

## ElementUI是什么
ElementUI是基于vue开发的一套桌面风格的UI库。
优点：使用简单，界面美观。

## 项目概观

开发electron项目，就像是开发浏览器，有两部分：

* html展示：通过编写html页面实现功能。
  * 每个html页面都运行在一个独立的渲染进程里。
  * 工作内容为操作vue相关的API。
* 其他部分：
  * 桌面应用UI部分：包括标题栏、菜单栏，工具栏，文件拖放等。通过操作electron的API实现。
  * 与html页面进行数据交换等操作。通过electron中的ipc接口实现。
  * 运行在唯一的主进程里。

# 新建项目

1. 下载模板文件：<a href="/工具研究/electron/myapp.zip" download="myapp.zip">myapp</a>
2. 修改文件夹名字`myapp`、`package.json`中的`name`字段为新项目的名字
3. 执行`npm install`或`cnpm install`下载依赖文件
4. 执行`npm start`运行项目
