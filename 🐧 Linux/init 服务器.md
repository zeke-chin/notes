# 安装ohmyzsh

```bash
wget https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh -O ~/install.sh && sed -i 's#REPO=${REPO:-ohmyzsh/ohmyzsh}#REPO=${REPO:-mirrors/oh-my-zsh}#g' ~/install.sh && sed -i 's#REMOTE=${REMOTE:-https://github.com/${REPO}.git}#REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}#g' ~/install.sh && chmod +777 ~/install.sh && sh ~/install.sh && rm ~/install.sh
```
  

# 安装常用软件
```bash
git clone https://gitclone.com/github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git clone https://gitclone.com/github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

apt update && apt install zsh vim htop wget curl git nload autojump tmux neofetch ranger gcc make linux-headers-`uname -r` -y
```
