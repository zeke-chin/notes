```yaml
version: '3.8'  # 使用的 Docker Compose 版本

services:
  pandoc-server:
    image: pandoc/core:latest  # 使用 pandoc 官方镜像
    container_name: pandoc-server  # 容器名称
    ports:
      - "3030:3030"  # 将本地的 3030 端口映射到容器的 3030 端口
    entrypoint: /usr/local/bin/pandoc-server  # 指定入口点为 pandoc-server
    stdin_open: true  # 等价于 -it，打开 stdin 以便于交互
    tty: true  # 为容器分配伪终端
    restart: unless-stopped  # 让容器在非手动停止时自动重启

```