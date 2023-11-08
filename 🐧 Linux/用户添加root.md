1. 添加用户
``` bash
sudo useradd -m -d /data/cgl cgl
```
2. 添加root权限
`/etc/sudoers`
```
# Cmnd alias specification

# User privilege specification
root    ALL=(ALL:ALL) ALL
cgl     ALL=(ALL:ALL) ALL
```