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


 lan-clip:
    hostname: clip
    container_name: clip
    restart: always
    image: registry.cn-shanghai.aliyuncs.com/zekechin/lan-clip:latest
    privileged: true
    ipc: host
    tty: true
    ports:
      - '9501:9501'
    volumes:
      - './clip-cfg.json:/app/server/config.json'

```

clip-config
```

```


Github: `https://github.com/Zeke-chin/clash_config_manager`
```dockerfile
FROM golang:latest as clash

  

RUN go env -w GOPROXY=https://goproxy.cn,direct

  

WORKDIR /workspace

RUN git clone https://github.com/Zeke-chin/clash.2023.08.06.git

  

ARG TARGETPLATFORM

ENV WORKDIR=/workspace/clash.2023.08.06

  

RUN case "$TARGETPLATFORM" in \

"linux/amd64") ARCH="linux-amd64" ;; \

"linux/arm64") ARCH="linux-arm64" ;; \

"darwin/amd64") ARCH="darwin-amd64" ;; \

"darwin.arm64") ARCH="darwin-arm64" ;; \

*) echo "Unsupported platform: $TARGETPLATFORM" >&2; \

exit 1 ;; \

esac && \

cd $WORKDIR && \

make $ARCH

  

# cp /workspace/clash.2023.08.06/bin/clash-* clash

  
  

FROM rust:latest as ccm

  

# RUN cargo install crm && crm use bfsu-sparse

RUN apt update && apt install musl-tools libssl-dev -y

WORKDIR /workspace

RUN git clone https://github.com/Zeke-chin/clash_config_manager.git

  

ARG TARGETPLATFORM

ENV WORKDIR=/workspace/clash_config_manager

  

RUN case "$TARGETPLATFORM" in \

"linux/amd64") ARCH="x86_64-unknown-linux-musl" ;; \

"linux/arm64") ARCH="aarch64-unknown-linux-gnu" ;; \

"darwin/amd64") ARCH="x86_64-apple-darwin" ;; \

"darwin/arm64") ARCH="aarch64-apple-darwin" ;; \

*) echo "Unsupported platform: $TARGETPLATFORM" >&2; \

exit 1 ;; \

esac && \

cd $WORKDIR && \

make $ARCH

  

# cp /workspace/clash_config_manager/target/bin/*-clash_config_manager CCM

  

FROM debian:latest as base

  

# RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list \

# && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list

RUN printf "\

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释 \n\

deb http://mirrors.cernet.edu.cn/debian/ bookworm main contrib non-free non-free-firmware \n\

deb-src http://mirrors.cernet.edu.cn/debian/ bookworm main contrib non-free non-free-firmware \n\

\n\

deb http://mirrors.cernet.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware \n\

deb-src http://mirrors.cernet.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware \n\

\n\

deb http://mirrors.cernet.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware \n\

deb-src http://mirrors.cernet.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware \n\

\n\

# deb http://mirrors.cernet.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware \n\

# deb-src http://mirrors.cernet.edu.cn/debian-security bookworm-security main contrib non-free non-free-firmware \n\

\n\

deb http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware \n\

deb-src http://security.debian.org/debian-security bookworm-security main contrib non-free non-free-firmware \n\

" > /etc/apt/sources.list

ENV LANG=zh_CN.UTF-8 LANGUAGE=zh_CN:zh LC_ALL=zh_CN.UTF-8 DEBIAN_FRONTEND=noninteractive

  

RUN apt update && apt install -y \

apt-transport-https \

ca-certificates \

supervisor \

wget \

curl \

vim \

unzip \

locales \

fonts-wqy-zenhei

  

RUN locale-gen zh_CN.UTF-8 && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

  

FROM base as Runtime

CMD ["supervisord", "-n"]

WORKDIR /opt/clash

  

RUN mkdir -p /root/.config/clash && \

wget -O /root/.config/clash/Country.mmdb https://github.com/Dreamacro/maxmind-geoip/releases/latest/download/Country.mmdb

RUN wget https://github.com/haishanh/yacd/archive/refs/heads/gh-pages.zip && \

unzip gh-pages.zip && \

mv yacd-gh-pages ui && \

rm gh-pages.zip

  

COPY --from=clash /workspace/clash.2023.08.06/bin/clash-* /opt/clash/clash

RUN echo "\

[program:clash] \n\

command=/opt/clash/clash -f /opt/clash/config.yaml \n\

autorestart=True \n\

autostart=True \n\

redirect_stderr = true \n\

priority=999 \n\

" > /etc/supervisor/conf.d/clash.conf

  

COPY --from=ccm /workspace/clash_config_manager/target/bin/*-clash_config_manager /opt/clash/CM

RUN echo "\

[program:CM] \n\

command=/opt/clash/CM --clash-url %(ENV_clash-url)s --file-path /opt/clash/config.yml \n\

autorestart=True \n\

autostart=True \n\

redirect_stderr = true \n\

priority=1 \n\

" > /etc/supervisor/conf.d/CM.conf

  

EXPOSE 7890 7891 9090
```