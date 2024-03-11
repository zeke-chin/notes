# 1. **创建SSH密钥**: 

- 如果你还没有SSH密钥对（公钥和私钥），首先需要创建它们。打开终端，然后输入以下命令：
	```bash
	╰─(base) ○ ssh-keygen -t rsa
	Generating public/private rsa key pair.
	Enter file in which to save the key (/root/.ssh/id_rsa):	# 共钥和私钥 存储位置
	Enter passphrase (empty for no passphrase):	# 密码 回车设置无密码
	Enter same passphrase again:	# 再次输入密码

# 2. **复制公钥到远程服务器**

- 上一步骤中 会创建两个文件
  - 私钥	
