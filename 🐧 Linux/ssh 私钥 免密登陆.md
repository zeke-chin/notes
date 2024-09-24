# 1. **创建SSH密钥**: 

- 如果你还没有SSH密钥对（公钥和私钥），首先需要创建它们。打开终端，然后输入以下命令：
	```bash
	╰─(base) ○ ssh-keygen -t rsa
	Generating public/private rsa key pair.
	Enter file in which to save the key (/root/.ssh/id_rsa):	# 共钥和私钥 存储位置
	Enter passphrase (empty for no passphrase):	# 密码 回车设置无密码
	Enter same passphrase again:	# 再次输入密码
	```
	
- 上一步骤中 会创建两个文件
	
	- 私钥: `~/.ssh/id_rsa`	密码组件 需要保密
	- 共钥: `~/.ssh/id_rsa.pub`	 需求分享给服务器

# 2. **复制公钥到远程服务器**

- 将**公钥**（默认是`~/.ssh/id_rsa.pub`）**复制**到 服务器到 `~/.ssh/authorized_keys`文件中

  - `ssh-copy-id`

    - ```bash
      ssh-copy-id -i ~/.ssh/id_rsa.pub 用户名@服务器地址
      ```

  - 手动

    - ```bash
      scp ~/.ssh/id_rsa.pub 用户名@服务器地址:~/
      ssh 用户名@服务器地址
      cat ~/id_rsa.pub >> ~/.ssh/authorized_keys
      rm ~/id_rsa.pub
      ```

- 确认服务器上的SSH配置

  - 登陆到服务器后，确保`~/.ssh`目录的权限是正确的。你的home目录，`~/.ssh`目录和`~/.ssh/authorized_keys`文件不应该对组或其他用户开放写权限。

  - ```bash
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_keys
    ```

- **编辑SSH配置文件`/etc/ssh/sshd_config`** 启用密钥登陆

  - ```sh
    PubkeyAuthentication yes
    AuthorizedKeysFile .ssh/authorized_keys
    ```
  
  - ```shell
    cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak && \
    sed -i '/^#\?PubkeyAuthentication/s/^#\?//g' /etc/ssh/sshd_config && \
    sed -i '/^#\?AuthorizedKeysFile/s/^#\?//g' /etc/ssh/sshd_config && \
    sed -i '/^PubkeyAuthentication/s/.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i '/^AuthorizedKeysFile/s/.*/AuthorizedKeysFile .ssh\/authorized_keys/' /etc/ssh/sshd_config
    
    ```
  


# 3. 重启ssh服务(当PubkeyAuthentication已经启动再次新增 则不需要重启)

```bash
sudo systemctl restart sshd
```

or

```bash
sudo service ssh restart	
```

