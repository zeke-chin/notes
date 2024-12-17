```yml
services:
  hbbs:
    container_name: hbbs
    image: rustdesk/rustdesk-server:latest
    command: hbbs
    environment:
      - "RELAY=hbbr:21117"
      - "ENCRYPTED_ONLY=1"
    ports:
      - 21115:21115
      - 21116:21116
      - 21116:21116/udp
      - 21118:21118
    volumes:
      - ./data:/root
    networks:
      - rustdesk-net
    depends_on:
      - hbbr
    restart: unless-stopped

  hbbr:
    container_name: hbbr
    image: rustdesk/rustdesk-server:latest
    command: hbbr
    ports:
      - 21117:21117
      - 21119:21119
    volumes:
      - ./data:/root
    networks:
      - rustdesk-net
    restart: unless-stopped

networks:
  rustdesk-net:
    external: false

```