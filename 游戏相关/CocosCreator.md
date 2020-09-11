# 前言

本文会总结CocosCreator使用中的方方面面。

官方文档：http://docs.cocos.com/creator/manual/zh/

CocosCreator版本：v2.3

# 目录结构

* assets：保存项目所有的代码和资源，会被打包
  * Scene：所有场景
  * Script：所有脚本
  * Texture：所有纹理及图片
* library：
* local：
* packages：
* settings：
* temp：

# 资源加载

从生命周期管理的角度看，creator里的资源分为两种。

* 一种是所有存放于assets目录下的资源。
  * 这种资源的生命周期由creator管理，只能在creator编辑器中预设，不能动态切换。

* 另一种是存放在assets/resources目录下的资源。
  * 需要由开发者管理生命周期。
  * 所有的resources资源都会被导出。

* 不论是resources资源，还是普通资源，都可以相互引用，并正确导出。所以只应该在resouces目录下，存放需要直接用代码加载的资源；间接加载的资源，应该由creator自动管理。

**加载单个资源**

```js
//加载普通资源
//resname: 相对于assets/resources目录，并且不能加后缀名
cc.loader.loadRes(resname, function (err, res) {
});

//加载SpriteFrame
//必须指明资源类型，否则加载到的是cc.Texture2D
cc.loader.loadRes(resname, cc.SpriteFrame, function (err, spriteFrame) {
});

//先加载图集，再获得其中的SpriteFrame
cc.loader.loadRes(atlasname, cc.SpriteAtlas, function (err, atlas) {
    var frame = atlas.getSpriteFrame('sheep_down_0');
    sprite.spriteFrame = frame;
});
```

**加载目录下所有资源**

```js
// 加载dirname目录下所有资源
cc.loader.loadResDir(dirname, function (err, assets) {
    // ...
});

// 加载dirname目录下所有 SpriteFrame，并且获取它们的路径
cc.loader.loadResDir(dirname, cc.SpriteFrame, function (err, assets, urls) {
    // ...
});
```

**加载远程资源**

```js
// 远程 url 带图片后缀名
var remoteUrl = "http://unknown.org/someres.png";
cc.loader.load(remoteUrl, function (err, texture) {
    // Use texture to create sprite frame
});

// 远程 url 不带图片后缀名，此时必须指定远程图片文件的类型
remoteUrl = "http://unknown.org/emoji?id=124982374";
cc.loader.load({url: remoteUrl, type: 'png'}, function () {
    // Use texture to create sprite frame
});

// 用绝对路径加载设备存储内的资源，比如相册
var absolutePath = "/dara/data/some/path/to/image.png"
cc.loader.load(absolutePath, function () {
    // Use texture to create sprite frame
});
```

**释放资源**

```js
// 直接释放某个贴图
cc.loader.release(texture);

// 释放一个 prefab 以及所有它依赖的资源
var deps = cc.loader.getDependsRecursively('prefabs/sample');
cc.loader.release(deps);

// 如果在这个 prefab 中有一些和场景其他部分共享的资源，你不希望它们被释放，可以将这个资源从依赖列表中删除
var deps = cc.loader.getDependsRecursively('prefabs/sample');
var index = deps.indexOf(texture2d._uuid);
if (index !== -1)
    deps.splice(index, 1);
cc.loader.release(deps);
```









