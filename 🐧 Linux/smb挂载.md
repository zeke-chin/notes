1. 检查smb服务
`smbclient -L //192.168.221.129/`

这种smb的 `Sharename` 就是 `share`
```
[root@samba-client /]# smbclient -L  //192.168.221.129/
Enter root's password: 
Anonymous login successful
Domain=[MYGROUP] OS=[Unix] Server=[Samba 3.6.9-164.el6]

	    Sharename       Type      Comment
    ---------       ----      -------
    devops          Printer   samba-server test
    share           Printer   share
    IPC$            IPC       IPC Service (Samba Server Version 3.6.9-164.el6)
Anonymous login successful
Domain=[MYGROUP] OS=[Unix] Server=[Samba 3.6.9-164.el6]

    Server               Comment
    ---------            -------
    SAMBA-SERVER         Samba Server Version 3.6.9-164.el6

    Workgroup            Master
    ---------            -------
    MYGROUP              SAMBA-SERVER

```

这种smb的 `Sharename` 就是 `zeke
```
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\cgl's password:

	Sharename       Type      Comment
	---------       ----      -------
	zeke            Disk
	IPC$            IPC       IPC Service (Samba Server)
Reconnecting with SMB1 for workgroup listing.
protocol negotiation failed: NT_STATUS_INVALID_NETWORK_RESPONSE
Failed to connect with SMB1 -- no workgroup available
```


2. 挂载
```
mount.cifs -o user=stu1,pass=123456 //192.168.221.129/zeke /stu1
```

查看id
```
╰─○ id
uid=1001(cgl) gid=1001(cgl) 组=1001(cgl),110(ssl-cert),999(docker)
```
带id挂载
```
mount -t cifs //192.155.1.93/zeke /mnt/93_smb -o username=zeke,password=113113,uid=1001
```

3. 卸载
```
sudo umount /mnt/93_smb
```