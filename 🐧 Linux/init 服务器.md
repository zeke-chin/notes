# 安装ohmyzsh

```bash
wget https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh -O ~/install.sh && sed -i 's#REPO=${REPO:-ohmyzsh/ohmyzsh}#REPO=${REPO:-mirrors/oh-my-zsh}#g' ~/install.sh && sed -i 's#REMOTE=${REMOTE:-https://github.com/${REPO}.git}#REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}#g' ~/install.sh && chmod +777 ~/install.sh && sh ~/install.sh && rm ~/install.sh
```


# 安装常用软件
```bash
git clone https://gitclone.com/github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git clone https://gitclone.com/github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

apt update && apt install zsh vim htop wget curl git nload autojump tmux neofetch ranger gcc make linux-headers-`uname -r` -y

# miniconda3
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

# Init zshrc
```sh
# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:/usr/local/bin:/usr/libexec/docker/cli-plugins:$PATH

export ZSH="$HOME/.oh-my-zsh"

# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="fino-time"
#ZSH_THEME="random"

plugins=(
    git
    autojump
    sublime
    common-aliases
    themes
    tmux
    history
    docker
    zsh-syntax-highlighting
    zsh-autosuggestions
    kubectl
    docker-compose
    helm
    extract
    sudo  
)
source $ZSH/oh-my-zsh.sh

# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias ra='ranger'
alias zshc='vim ~/.zshrc'
alias zshcc='source ~/.zshrc'

# docker
alias ndc='nvidia-docker-compose'
alias ndcud='nvidia-docker-compose up -d'
alias deit='docker exec -i -t'
alias dc='docker-compose'
alias dcps='docker-compose ps'
alias dcud='docker-compose up -d'
alias dm='docker-machine'
alias dps='docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
alias dt="docker_exec"

# ghcr.io替换为ghcr.nju.edu.cn
gpull() {
  image=${1/#ghcr.io/ghcr.nju.edu.cn}
  echo "Pulling image: $image"
  docker pull $image
}


# 快速进入容器
docker_exec() {
    local shell=${1:-bash}

    container_name=$(docker-compose ps --quiet)
    if [ $(echo "$container_name" | wc -l) -eq 1 ]; then
        docker exec -it $container_name $shell
    else
        docker-compose ps
    fi
}

# proxy
http_proxy="http://192.155.1.10:37890"
https_proxy="http://192.155.1.10:37890"
alias dpon="dpm -httpProxy $http_proxy -httpsProxy $http_proxy -onProxy 1"
alias dpoff="dpm -onProxy 0"

alias onc="export http_proxy=$https_proxy https_proxy=$https_proxy all_proxy=$https_proxy"
alias offc="unset http_proxy https_proxy all_proxy"


#export RUSTC_WRAPPER=/usr/local/bin/sccache
#export AWS_ACCESS_KEY_ID=FFVAYWLfxSubfTcfjUns
#export AWS_SECRET_ACCESS_KEY=MgD4NOBWvZTjPcsLnwGhZchhnY7oULQRgZbIpAjo
#export SCCACHE_BUCKET=cache
#export SCCACHE_ENDPOINT=https://minio-api.haihuman.com
#export SCCACHE_S3_USE_SSL=true
#export SCCACHE_REGION=auto


alias nload="bash -c 'nload -u H'"
alias gcm='git commit -m '
```