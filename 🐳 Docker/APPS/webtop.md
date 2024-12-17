```yaml

services:
  webtop:
    image: linuxserver/webtop:ubuntu-xfce
    container_name: webtop
    privileged: true
    security_opt:
      - seccomp:unconfined #optional
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      # - DOCKER_MODS=linuxserver/mods:universal-internationalization
      - DOCKER_MODS=linuxserver/mods:universal-package-install
      - INSTALL_PACKAGES=fonts-wqy-zenhei
      - LC_ALL=zh_CN.UTF-8
      - LANGUAGE=zh_CN:zh:en_US:en
      - SUBFOLDER=/ #optional
      - TITLE=Webtop #optional
      - http_proxy=http://192.155.1.10:37890
      - https_proxy=http://192.155.1.10:37890
      - all_proxy=http://192.155.1.10:37890
    volumes:
      - ./datas:/config
      # - ./datas:/config
      # - /var/run/docker.sock:/var/run/docker.sock #optional
    ports:
      - 33000:3000
      - 33001:3001
    devices:
      - /dev/dri:/dev/dri #optional
    shm_size: "10gb" #optional
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]#
```