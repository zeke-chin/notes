1. 安装包
```
apt install musl-tools libssl-dev -y
```
2. 添加依赖
```
openssl = { version = "0.10", features = ["vendored"] }
```