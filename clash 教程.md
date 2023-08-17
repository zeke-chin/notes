docker-compose.yml
```yaml
version: '2'
services:
  zeke_clash:
    hostname: zeke_clash
    container_name: zeke_clash
    restart: always
    image: registry.cn-shanghai.aliyuncs.com/zekechin/clash
    volumes:
      - ./config.yaml:/opt/clash/config.yaml
    privileged: true
    ipc: host
    tty: true
    ports:
      - '37890:7890' # http代理端口
      - '37891:7891' # socks代理端口
      - '39090:9090' # web端口
# alias onc="export https_proxy=http://127.0.0.1:37890 http_proxy=http://127.0.0.1:37890 all_proxy=socks5://127.0.0.1:37890"
# alias offc"unset https_proxy http_proxy all_proxy"

```



1. 通过clash链接下载clash配置文件，并命名为`config.yaml` 移动至`docker-compose.yml`同级目录
2. 在`config.yaml`中加一行

`external-ui: /opt/clash/ui`

```yaml
port: 7890
socks-port: 7891
redir-port: 7892
mixed-port: 7893
allow-lan: false
mode: rule
log-level: info
ipv6: false
external-controller: 0.0.0.0:9090
##############
external-ui: /opt/clash/ui
##############
clash-for-android:
  append-system-dns: false
profile:
  tracing: true
experimental:
  sniff-tls-sni: true
dns:
```

3. 启动服务
![image-20230817174358407](clash%20%E6%95%99%E7%A8%8B.assets/image-20230817174358407.png)

4. 
