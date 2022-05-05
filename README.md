# pascal-s-language-compiler

> 这是一个用于将 Pascal-S 语法的代码转换为 C 语法代码的编译器

## 环境要求

- Python 3.7+
- ply 3.11
- sanic 20.12.6
- pytest 6.2.5
- pytest-cov 3.0.0

## 运行

- 安装依赖

```
$ pip install -r requirements.txt
```

- 启动项目

```
$ python main.py
```

## 单元测试

- 运行命令

```
$ pytest
```

## 请求格式

- 向 `127.0.0.1:8000/api` 发送 POST 请求，body 为 Pascal-S 语法的代码
- 返回语法树、符号表和编译生成的 C 语法代码，格式为 Json
```
{
    "ast": {},
    "symbolTable": {},
    "error": [],
    "warning": []
}
```