# 文件结构与各分支定义

## 文件目录结构

module： 每个人编写的模块放置的位置。

start.py：主程序

requirments.txt：依赖文件

utils.py：放置全局工具，如配置文件读取等函数

config.yml：配置文件。已被git ignore。

因此，本项目的目录应该长得像这样。

```
.
|-- root
    |-- .gitignore
    |-- README.md
    |-- config.yml
    |-- start.py
    |-- utils.py
    |-- module
        |-- __init__.py
        |-- getToilet.py
        |-- login.py
        |-- sample.py
```

## 分支规范

### 分支定义

| 分支名     | 期限 | 备注                                                         |
| ---------- | :--: | ------------------------------------------------------------ |
| master     | 长期 | 上线的版本，与线上同步                                       |
| develop    | 长期 | 开发中的版本，开发完成后与merge到master中                    |
| feature/\* | 短期 | 从develop分出，用于开发新功能。*表示你开发的功能名称。开始开发的时候从develop签出。 |
| bugfix/\*  | 短期 | 从develop分出，用于修复bug。*表示你要修复的bug名称。开始修复的时候从develop签出。 |

