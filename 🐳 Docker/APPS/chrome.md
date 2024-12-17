```yaml
services:
  chromium:
    image: linuxserver/chromium:latest
    container_name: chromium
    security_opt:
      - seccomp:unconfined #optional
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Asia/Shanghai
      - CHROME_CLI=https://www.baidu.com/ #optional
      - DOCKER_MODS=linuxserver/mods:universal-internationalization
      - LC_ALL=zh_CN.UTF-8
      - http_proxy=http://192.155.1.10:37890
      - https_proxy=http://192.155.1.10:37890
      - all_proxy=http://192.155.1.10:37890
    volumes:
      - ./datas/1:/config
    ports:
      - 3100:3000
      - 3101:3001
    shm_size: "10gb"
    restart: unless-stopped

```