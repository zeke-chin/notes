```yaml
version: "3"
services:
  windows:
    image: dockurr/windows
    container_name: windows
    environment:
      VERSION: "tiny10"	# 镜像版本
      DISK_SIZE: "600G"		# 磁盘大小
      RAM_SIZE: "8G"
      CPU_CORES: "4"
    devices:
      - /dev/kvm
    cap_add:
      - NET_ADMIN
    ports:
      - 3006:8006. # web端口
      - 3389:3389/tcp
      - 3389:3389/udp
		volumes:
		  - ./data:/storage
		  - ./shared:/shared	# 网络共享
    stop_grace_period: 2m
    restart: on-failure
```


```yaml
environment:
  VERSION: "win11"
```

| **Value** | **Version**                                     | **Size**     |
| --------- | ----------------------------------------------- | ------------ |
| `win11`   | Windows 11 Pro Windows 11 专业版                   | 6.4 GB 6.4GB |
| `win11e`  | Windows 11 Enterprise Windows 11 企业版            | 5.8 GB 5.8GB |
| `win10`   | Windows 10 Pro Windows 10 专业版                   | 5.8 GB 5.8GB |
| `ltsc10`  | Windows 10 LTSC Windows 10 长期支持中心               | 4.6 GB 4.6GB |
| `win10e`  | Windows 10 Enterprise Windows 10 企业版            | 5.2 GB 5.2GB |
| `win81`   | Windows 8.1 Pro Windows 8.1 专业版                 | 4.2 GB 4.2GB |
| `win81e`  | Windows 8.1 Enterprise Windows 8.1 企业版          | 3.8 GB 3.8GB |
| `win7`    | Windows 7 Enterprise Windows 7 企业版              | 3.0 GB 3.0GB |
| `vista`   | Windows Vista Enterprise  <br>Windows Vista 企业版 | 3.0 GB 3.0GB |
| `winxp`   | Windows XP Professional Windows XP 专业版          | 0.6 GB 0.6GB |
|           |                                                 |              |
| `2022`    | Windows Server 2022                             | 4.7 GB 4.7GB |
| `2019`    | Windows Server 2019 Windows 服务器 2019            | 5.3 GB 5.3GB |
| `2016`    | Windows Server 2016 Windows 服务器 2016            | 6.5 GB 6.5GB |
| `2012`    | Windows Server 2012 Windows 服务器 2012            | 4.3 GB 4.3GB |
| `2008`    | Windows Server 2008                             | 3.0 GB 3.0GB |
|           |                                                 |              |
| `core11`  | Tiny 11 Core 微型 11 核                            | 2.1 GB 2.1GB |
| `tiny11`  | Tiny 11 小11                                     | 3.8 GB 3.8GB |
| `tiny10`  | Tiny 10 小10                                     | 3.6 GB 3.6GB |

- ### How do I pass-through a disk? 如何传递磁盘？

  

  It is possible to pass-through disk devices directly by adding them to your compose file in this way:
  通过将磁盘设备添加到您的撰写文件中，可以直接传递磁盘设备：

  ```
  devices:
    - /dev/sdb:/disk1
    - /dev/sdc:/disk2
  ```

  

  Use `/disk1` if you want it to become your main drive, and use `/disk2` and higher to add them as secondary drives.
  如果您希望它成为主驱动器，请使用 `/disk1` ，并使用 `/disk2` 及更高版本将它们添加为辅助驱动器。



https://github.com/dockur/windows