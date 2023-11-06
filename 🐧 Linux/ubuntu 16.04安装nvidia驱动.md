
- 卸载原有驱动
    
     sudo apt-get remove --purge nvidia*
    
- 禁用nouveau
    
     # 添加黑名单，添加可编辑权限  
     sudo chmod 666 /etc/modprobe.d/blacklist.conf  
     # 编辑  
     # 进入后添加最后行添加:  
     blacklist nouveau  
     blacklist lbm-nouveau  
     options nouveau modeset=0  
     alias nouveau off  
     alias lbm-nouveau off  
     ​  
     ​  
     sudo vim /etc/modprobe.d/blacklist.conf  
     # 恢复权限  
     sudo chmod 644 /etc/modprobe.d/blacklist.conf
    
- 更新启动项
    
     sudo reboot  
     sudo update-initramfs -u  
     # 验证: 在终端输 lsmod | grep nouveau ，若无任何显示说明已禁用
    
- 关闭图形相关服务
    
     sudo service lightdm stop  
     sudo service docker stop  
     sudo service nvidia-docker stop
    
- 安装
    
     sudo ./NVIDIA-Linux-x86_64-510.60.02.run --no-x-check --no-nouveau-check --no-opengl-files  
     # –no-x-check 不检查x服务  
     # –no-nouveau-check 不检查nouveau  
     # –no-opengl-files 不安装OpenGL文档
    
    > **安裝過程中的選項：**
    > 
    > The distribution-provided pre-install script failed! Are you sure you want to continue? 選擇 yes 繼續。
    > 
    > Would you like to register the kernel module souces with DKMS? This will allow DKMS to automatically build a new module, if you install a different kernel later? 選擇 No 繼續。
    > 
    > 問題大概是：Nvidia’s 32-bit compatibility libraries? 選擇 No 繼續。
    > 
    > Would you like to run the nvidia-xconfigutility to automatically update your x configuration so that the NVIDIA x driver will be used when you restart x? Any pre-existing x confile will be backed up. 選擇 Yes 繼續
    
- 重启相关服务
    
     sudo service lightdm start  
     sudo service docker start  
     sudo service nvidia-docker start
    

## 参考文档

- [https://www.notion.so/ubuntu-16-04-nvidia-510-2f761714d33e4efa941d6c4533a889c9#c8d10ccfa2ed4c1b8e9afe172144007f](https://www.notion.so/ubuntu-16-04-nvidia-510-2f761714d33e4efa941d6c4533a889c9#c8d10ccfa2ed4c1b8e9afe172144007f)
    
- [https://blog.csdn.net/qq_46350148/article/details/108650556](https://blog.csdn.net/qq_46350148/article/details/108650556)