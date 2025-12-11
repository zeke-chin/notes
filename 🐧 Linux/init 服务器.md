# 安装常用软件

```
 sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
     && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list
 
 git clone https://ghproxy.net/https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git clone https://ghproxy.net/https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
 
 apt update && apt install zsh vim htop wget curl git nload autojump tmux neofetch ranger gcc make linux-headers-`uname -r` -y
 
 # miniconda3
 wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

# 安装 zim

```shell

curl -fsSL https://raw.githubusercontent.com/zimfw/install/master/install.zsh | zsh

	wget -nv -O - https://raw.githubusercontent.com/zimfw/install/master/install.zsh | zsh

```

### `.zimrc`
```shell
zmodule environment
zmodule input
zmodule termtitle
zmodule utility
zmodule duration-info
zmodule git-info
zmodule asciiship
zmodule zsh-users/zsh-completions --fpath src
zmodule completion
zmodule zsh-users/zsh-syntax-highlighting
zmodule zsh-users/zsh-history-substring-search
zmodule zsh-users/zsh-autosuggestions

zmodule ohmyzsh/ohmyzsh --root plugins/sudo
zmodule ohmyzsh/ohmyzsh --root plugins/extract
zmodule ohmyzsh/ohmyzsh --root plugins/autojump
zmodule ohmyzsh/ohmyzsh --root plugins/git
```

### `.zshrc`
```shell
# -----------------
# Zsh configuration
# -----------------

#
# History
#

# Remove older command from the history if a duplicate is to be added.
setopt HIST_IGNORE_ALL_DUPS
bindkey -e
WORDCHARS=${WORDCHARS//[\/]}
# zsh-users/zsh-autosuggestions is the last module in your ~/.zimrc.
ZSH_AUTOSUGGEST_MANUAL_REBIND=1

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)

# ------------------
# Initialize modules
# ------------------

ZIM_HOME=${ZDOTDIR:-${HOME}}/.zim
# Download zimfw plugin manager if missing.
if [[ ! -e ${ZIM_HOME}/zimfw.zsh ]]; then
  if (( ${+commands[curl]} )); then
    curl -fsSL --create-dirs -o ${ZIM_HOME}/zimfw.zsh \
        https://github.com/zimfw/zimfw/releases/latest/download/zimfw.zsh
  else
    mkdir -p ${ZIM_HOME} && wget -nv -O ${ZIM_HOME}/zimfw.zsh \
        https://github.com/zimfw/zimfw/releases/latest/download/zimfw.zsh
  fi
fi
# Install missing modules, and update ${ZIM_HOME}/init.zsh if missing or outdated.
if [[ ! ${ZIM_HOME}/init.zsh -nt ${ZIM_CONFIG_FILE:-${ZDOTDIR:-${HOME}}/.zimrc} ]]; then
  source ${ZIM_HOME}/zimfw.zsh init
fi
# Initialize modules.
source ${ZIM_HOME}/init.zsh

# ------------------------------
# Post-init module configuration
# ------------------------------

#
# zsh-history-substring-search
#

zmodload -F zsh/terminfo +p:terminfo
# Bind ^[[A/^[[B manually so up/down works both before and after zle-line-init
for key ('^[[A' '^P' ${terminfo[kcuu1]}) bindkey ${key} history-substring-search-up
for key ('^[[B' '^N' ${terminfo[kcud1]}) bindkey ${key} history-substring-search-down
for key ('k') bindkey -M vicmd ${key} history-substring-search-up
for key ('j') bindkey -M vicmd ${key} history-substring-search-down
unset key
# }}} End configuration added by Zim install

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
(( ! ${+functions[p10k]} )) || p10k finalize


  


alias f='fuck'
# alias j="autojump"
alias zshc="vim ~/.zshrc"
alias zshcc="source ~/.zshrc"
alias nload="bash -c 'nload -u H'"

alias gcm="git commit -m "



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
http_p="http://192.155.1.10:37890"
https_proxy="http://192.155.1.10:37890"
alias dpon="dpm -httpProxy $http_p -httpsProxy $https_proxy -onProxy 1"
alias dpoff="dpm -onProxy 0"

alias onc="export http_proxy=$http_p https_proxy=$https_proxy all_proxy=$https_proxy"
alias offc="unset http_proxy https_proxy all_proxy"



# PATH
path=('/home/zeke/.local/bin' $path)


```

## 安装插件
```
zimfw install
```

```shell
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
&& \
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```
-----

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
http_p="http://192.155.1.10:37890"
https_proxy="http://192.155.1.10:37890"
alias dpon="dpm -httpProxy $http_p -httpsProxy $https_proxy -onProxy 1"
alias dpoff="dpm -onProxy 0"

alias onc="export http_proxy=$http_p https_proxy=$https_proxy all_proxy=$https_proxy"
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