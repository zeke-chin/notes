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