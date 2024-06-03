
```yml
services:
  derper:
    image: pvapor/derper
    container_name: derper
    restart: always
    ports:
      - "4433:443"      # 填在web 及 https://ip:port 测试用
      - "3478:3478/udp" # 不能变
```