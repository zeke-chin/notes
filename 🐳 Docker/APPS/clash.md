```yaml
version: '3'
services:
  clash:
    hostname: clash
    container_name: clash
    restart: always
    image: registry.cn-shanghai.aliyuncs.com/zekechin/clash
    privileged: true
    ipc: host
    tty: true
    ports:
      - '37890:7890'
      - '37891:7891'
      - '39090:9090'
    environment:
      - clash-url=
```