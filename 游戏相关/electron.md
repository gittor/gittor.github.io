# 前言

总结electron使用中的方方面面。

官方文档：https://www.electronjs.org/docs

electron版本：8.11

Node版本：v12.16.1

## 安装electron-forge

electron项目的创建和打包都需要执行较多命令，使用electron-forge可以简化这个过程。

```bash
npm install -g electron-forge
```

---

| 目的     | 命令                        | 说明                                 |
| -------- | --------------------------- | ------------------------------------ |
| 新建项目 | `electron-forge init myapp` | 新建项目时会安装较多依赖，时间较长。 |
| 运行项目 | `npm start`                 |                                      |
| 打包分发 | `electron-forge make`       | 生成结果在out目录下。                |