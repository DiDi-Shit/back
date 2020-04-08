# ks
课设

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
