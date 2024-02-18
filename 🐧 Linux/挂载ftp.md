1. 安装`curlftpfs`

```
sudo apt-get install curlftpfs
```

1. 创建挂载点

```
sudo mkdir -p /mnt/184
```

1. 配置`allow_other`

在``/etc/fuse.conf`中 写入

- `user_allow_other `

1. 挂载

```bash
sudo curlftpfs quan.gao:Niren1015@192.155.1.184 /mnt/184 -o allow_other
```

