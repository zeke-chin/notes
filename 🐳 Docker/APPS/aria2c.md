```yaml
version: "2"
services:
  Aria2-Pro:
    container_name: aria2-pro
    image: p3terx/aria2-pro
    environment:
      - PUID=0
      - PGID=0
      - UMASK_SET=022
      - RPC_SECRET=113113
      - RPC_PORT=6800
      - LISTEN_PORT=6888
      - DISK_CACHE=64M
      - IPV6_MODE=false
      - UPDATE_TRACKERS=true
      - CUSTOM_TRACKER_URL=
      - TZ=Asia/Shanghai
      #- http_proxy=http://192.155.1.10:37890
      #- https_proxy=http://192.155.1.10:37890
      #- all_proxy=http://192.155.1.10:37890
    volumes:
      - ./downloads:/downloads
    ports:
     - 6800:6800
     - 6888:6888
     - 6888:6888/udp
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: 1m

  AriaNg:
    container_name: ariang
    image: p3terx/ariang
    command: --port 6880 --ipv6
    ports:
     - 6880:6880
    restart: unless-stopped
    logging:
      driver: json-file
      options:
        max-size: 1m
```