
# 🚀 终极跨国 SSH 加速指南：Cloudflare Tunnel (零信任隧道)

**工作原理：**
传统的 SSH 是你主动去连服务器（容易被墙、丢包、被识别特征）。
使用此方案后，你的 GCP 服务器会**主动向外**连接 Cloudflare 的骨干网建立一条隐形隧道。你的 Mac 也是连接 Cloudflare，双方在云端安全握手。**全程无视公网 IP 封锁，打字顺滑如局域网。**

---

## 🛠️ 第一阶段：云端与服务端配置 (Server-Side)

### 步骤 1：在 Cloudflare 创建隧道
1. 登录 [Cloudflare Dashboard](https://dash.cloudflare.com/)，进入 **Zero Trust** 控制台。
2. 左侧菜单依次点击 **Networks (网络)** -> **Tunnels (隧道)**。
3. 点击 **Create a tunnel (创建隧道)**，类型选择 **Cloudflared**。
4. 命名你的隧道（例如：`gcp-ssh-server`），点击 Next。

### 步骤 2：在服务器安装“连接器”
在创建页面，选择你的服务器环境（选择 `Debian` -> `64-bit`）。页面会给出一串带有 `eyJh...` 令牌的安装命令。

🔴 **【避坑警告 1：千万别把代码贴错地方！】**
> 这段代码的作用是让目标服务器向 CF 报到。**你必须通过原有方式（直连）登录到你的 GCP Ubuntu 服务器上**，把这段命令粘贴到服务器终端里执行！**绝对不能**在你的本地 Mac 电脑上执行这段带 Token 的命令！

**执行后验证：**
在 GCP 服务器上执行 `sudo systemctl status cloudflared`，看到 `active (running)` 说明服务器已成功接入云端。网页上点击 Next。

### 步骤 3：绑定域名入口（公共主机名）
这是告诉 Cloudflare：当有人访问哪个域名时，把流量送给这台服务器。

🔴 **【避坑警告 2：走错房间 & 漏填子域】**
> 1. **不要**去“专用主机名/专用网络”里配置，一定要在 **“Public Hostname (公共主机名)”** 或 **“已发布应用程序路由”** 这个标签页里配置！
> 2. **千万别忘了填子域 (Subdomain)！** 如果你留空了，它会直接覆盖你的主域名（例如 `20010215.xyz`），导致你网站打不开。一定要填个前缀，比如 `ssh` 或 `gcp`。

**正确的填写姿势：**
*   **Subdomain (子域)**：填 `gcp`
*   **Domain (域)**：下拉选择你的根域名 `20010215.xyz`
*   **Service (服务类型)**：下拉选 `SSH`
*   **URL**: 填 `localhost:22`
*   **保存！** (此时 CF 会自动在你的普通 DNS 界面生成一条记录)。

---

## ⚡ 第二阶段：消灭 5 秒登录卡顿 (Server-Side 优化)

即使隧道极速，SSH 自身的某些“老旧企业级安全机制”在跨国连接时会导致 5 秒的超时等待。

🔴 **【避坑警告 3：不要错怪网络质量】**
> 如果你发现输入密码前总是死死卡住 5 秒，这不是 Cloudflare 的锅，而是服务器开启了“反向 DNS 解析”和“GSSAPI 企业认证”。对于个人公网使用，必须关掉。

**在你的 GCP 服务器上执行这 3 行命令优化：**
```bash
sudo sed -i 's/#UseDNS yes/UseDNS no/g; s/UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
sudo sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config
sudo systemctl restart ssh
```
*优化后，你的 SSH 登录将从 5 秒瞬间变成 1 秒内秒进！*

---

## 💻 第三阶段：本地 Mac 配置 (Client-Side)

由于普通的 `ssh` 命令无法直接读懂 WebSocket 隧道里的数据，你的 Mac 也需要安装 `cloudflared` 作为一个本地“翻译官”。

### 步骤 1：安装本地工具
在你的 Mac 终端执行：
```bash
brew install cloudflared
```

🔴 **【避坑警告 4：本地执行路径写错】**
> Intel 芯片的 Mac 和 Apple Silicon (M1/M2/M3) 芯片的 Homebrew 安装路径是不一样的！
> 必须在终端执行一下 **`which cloudflared`**，把输出的绝对路径复制下来。
> (Intel 通常是 `/usr/local/bin/cloudflared`，M 系列通常是 `/opt/homebrew/bin/cloudflared`)。

### 步骤 2：配置 SSH 规则
在 Mac 终端编辑你的 SSH 配置文件：
```bash
nano ~/.ssh/config
```

将以下内容添加进去：
```ssh
Host gcp.20010215.xyz            # 换成你在第一阶段步骤 3 里配置的完整域名
    User zeke@zeke-mac           # 你的目标服务器用户名
    # 核心：调用本地 cloudflared 将 SSH 请求打包塞进隧道
    ProxyCommand /opt/homebrew/bin/cloudflared access ssh --hostname %h
    # 保持心跳，防止长时间不敲字自动断开
    ServerAliveInterval 60
    TCPKeepAlive yes
```
*(按 `Ctrl+O` 存盘，`Ctrl+X` 退出)*

---

## 🎉 第四阶段：享受丝滑连接

现在，你只需要在 Mac 终端里像往常一样敲下：

```bash
ssh gcp.20010215.xyz
```

**连接感受对比：**
*   🚫 **普通直连**：抖动巨大，打字粘手，晚高峰疯狂掉线。
*   🚀 **Cloudflare 隧道**：极其平稳，几乎零抖动，永远不掉线。你甚至可以去 GCP 后台把 22 端口的防火墙规则给删掉（禁止公网访问），进一步提升服务器安全性。



### 🧰 Cloudflare Tunnel 协议与常见服务映射表

| Cloudflare 服务类型 | 对应目标 URL 格式示例 | 常见服务场景 & 代表软件 | 客户端如何访问？ |
| :--- | :--- | :--- | :--- |
| **HTTP / HTTPS** | `localhost:8080`<br>`192.168.1.10:443` | **Web 网站、API、控制台 UI**<br>• Nginx / Apache<br>• 宝塔面板 / 1Panel<br>• Grafana / Prometheus<br>• Jupyter Notebook | **最简单**：浏览器直接输入域名即可访问。 |
| **SSH** | `localhost:22` | **Linux 远程命令行**<br>• OpenSSH | 需在 Mac 配置 `~/.ssh/config`，使用 `cloudflared access ssh`。 |
| **TCP** | `localhost:6379`<br>`localhost:3306`<br>`localhost:5432` | **所有纯 TCP 协议的服务（重点）**<br>• **Redis** (6379)<br>• **MySQL / MariaDB** (3306)<br>• **PostgreSQL** (5432)<br>• **MongoDB** (27017)<br>• Minecraft 游戏服 (25565) | **复杂**：浏览器无法直接访问！必须在本地 Mac 上开启端口转发（详见下方教程）。 |
| **RDP** | `localhost:3389` | **Windows 远程桌面**<br>• Windows Remote Desktop | 本地需运行 `cloudflared access rdp` 转发，然后用微软 RD 客户端连本地端口。 |
| **UNIX** <br> *(含 UNIX+TLS)* | `/var/run/docker.sock`<br>`/tmp/mysql.sock` | **本地 Unix 套接字（高级）**<br>• Docker 守护进程<br>• 不对外开放端口的本地数据库 | 客户端通过隧道安全地与远端套接字通信（极度安全的隔离方案）。 |

---

### 🔴 【避坑警告：如何正确连接 Redis / MySQL 等 TCP 服务？】

这里是绝大多数人会踩坑的地方！

假设你在云端把 `redis.20010215.xyz` 映射到了服务器的 `TCP` -> `localhost:6379`。
**错误做法：** 在你 Mac 上的 Redis 客户端（如 Another Redis Desktop Manager）里，直接填入 `redis.20010215.xyz` 和端口 `6379`。**这绝对连不上！** 因为 Cloudflare 的边缘节点默认只接受 HTTP/HTTPS 的握手，纯 TCP 流量直接发过去会被丢弃。

**正确做法（TCP 端口映射）：**

像 SSH 一样，你需要用你 Mac 本地的 `cloudflared` 充当“解包员”，把云端的 TCP 流量拉取到你 Mac 本地的一个端口上。

**步骤 1：在 Mac 终端运行本地转发命令**
```bash
# 格式：cloudflared access tcp --hostname <你的CF域名> --url <本地要监听的端口>
cloudflared access tcp --hostname redis.20010215.xyz --url localhost:6379
```
*(这条命令运行后终端会挂起，不要关掉它，这说明通道已经打通并保持监听)*

**步骤 2：连接本地端口**
现在，打开你 Mac 上的 Redis 客户端（或 Navicat / DataGrip 连接 MySQL）：
*   **Host (地址)**: 填 `127.0.0.1` 或 `localhost`
*   **Port (端口)**: 填 `6379` (你在上一步 `--url` 里写的端口)
*   **Password**: 填你服务器 Redis 的密码。

**原理解析：**
你连接自己 Mac 的 6379 端口 $\rightarrow$ 本地 `cloudflared` 截获 $\rightarrow$ 封装成加密 WebSocket 发给 CF $\rightarrow$ CF 发给 GCP 服务器 $\rightarrow$ GCP 服务器的 `cloudflared` 解包并丢给本机的 Redis。

---

### 🛡️ 进阶安全建议 (Zero Trust Access)

如果你把宝塔面板 (HTTP) 或者 Redis (TCP) 通过隧道暴露在公网域名上，虽然别人不知道你的服务器真实 IP，但**只要知道了域名，任何人都可以尝试爆破你的密码**。

**如何做到真正的“零信任 (Zero Trust)”？**
1. 在 Cloudflare 控制台左侧点击 **Access** -> **Applications**。
2. 点击 **Add an application**，选择 **Self-hosted**。
3. 把你的隧道域名（如 `redis.20010215.xyz` 或 `bt.20010215.xyz`）填进去。
4. 设置一个 **Policy (策略)**：比如 `Include -> Emails -> 填你自己的邮箱`。
5. **效果：** 任何人（包括你）访问这个域名之前，Cloudflare 都会拦截并弹出一个极其简洁的登录页面，只有接收并输入了你邮箱里的验证码（PIN），才能真正接触到背后的 Redis 或 Web 界面。

这相当于给你的所有服务，免费套上了一层**连黑客都无法绕过的 Google 级别身份验证防火墙**！
