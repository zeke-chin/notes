1. 安装`curlftpfs`

```bash
sudo apt-get install curlftpfs
```

2. 创建挂载点

```bash
sudo mkdir -p /mnt/184
```

3. 配置`allow_other`

在`sudo vim/etc/fuse.conf`中 写入

- `user_allow_other `

4. 挂载

```bash
sudo curlftpfs quan.gao:Niren1015@192.155.1.184 /mnt/184 -o allow_other
```

5. 卸载

```bash
sudo fusermount -u /mnt/184
```

