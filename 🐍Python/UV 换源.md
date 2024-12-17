### uv
```toml

[pip]
index-url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# uv add xxx
[tool.uv]
index-url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"

# uv pip install xxx
[tool.uv.pip]
index-url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
```

### uvx 
`uvx`是`uv tool run`的别名
需要配置`~/.config/uv/uv.toml`
```toml
index-url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple"
```