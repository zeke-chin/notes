```yaml
version: '3'
services:
  umami:
    image: docker.umami.dev/umami-software/umami:mysql-latest
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 500M
        reservations:
          cpus: '0.25'
          memory: 200M
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: mysql://umami:xxx@127.0.0.1:3306/umami
      DATABASE_TYPE: mysql
      HASH_SALT: replace-me-with-a-random-string
    restart: always
    network_mode: "host"
```

Umami服务的CPU使用被限制在最多50%的CPU能力，内存使用被限制在最多500MB。同时，这个服务至少需要25%的CPU和200MB的内存。

```
# 原本的启动命令为 
docker-compse up -d 
# 需要添加一个参数--compatibility表示以兼容模式来运行 
docker-compose --compatibility up -d
```