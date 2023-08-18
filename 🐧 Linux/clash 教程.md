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
4. 验证服务打开`ip:port(39090)/ui`
![[Pasted image 20230818100341.png]]
5. 建议将所以协议代理都从7890走
![[Pasted image 20230818100420.png]]
6. 修改节点
	1. 修改规则模式节点
		1. ![[Pasted image 20230818100538.png]]
	2. 修改全局节点
		1. ![[Pasted image 20230818100602.png]]
7. 测试服务
	1. linux命令行走代理
		`export https_proxy=http://127.0.0.1:37890 http_proxy=http://127.0.0.1:37890 all_proxy=socks5://127.0.0.1:37890`
		自行修改ip及端口
	2. 使用技巧
	  如果你使用bash就在bash中加入
```
	  alias onc="export https_proxy=http://127.0.0.1:37890 http_proxy=http://127.0.0.1:37890 all_proxy=socks5://127.0.0.1:37890"

	  alias offc"unset https_proxy http_proxy all_proxy"
```
		3. 验证
```

❯ curl -i google.com
^C
❯ onc
❯ curl -i google.com
HTTP/1.1 301 Moved Permanently
Content-Length: 219
Cache-Control: public, max-age=2592000
Connection: keep-alive
Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-JWEwiGpdUYFYi-LBrDGC3w' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
Content-Type: text/html; charset=UTF-8
Date: Fri, 18 Aug 2023 02:08:55 GMT
Expires: Sun, 17 Sep 2023 02:08:55 GMT
Keep-Alive: timeout=4
Location: http://www.google.com/
Proxy-Connection: keep-alive
Server: gws
X-Frame-Options: SAMEORIGIN
X-Xss-Protection: 0

<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>


❯ offc
❯ curl -i google.com
