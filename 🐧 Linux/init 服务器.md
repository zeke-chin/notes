# 安装ohmyzsh

```bash
wget https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh -O ~/install.sh && sed -i 's#REPO=${REPO:-ohmyzsh/ohmyzsh}#REPO=${REPO:-mirrors/oh-my-zsh}#g' ~/install.sh && sed -i 's#REMOTE=${REMOTE:-https://github.com/${REPO}.git}#REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}#g' ~/install.sh && chmod +777 ~/install.sh && sh ~/install.sh && rm ~/install.sh
```
  

# 安装常用软件
```bash
git clone https://gitclone.com/github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git clone https://gitclone.com/github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

apt update && apt install zsh vim htop wget curl git nload autojump tmux neofetch ranger gcc make linux-headers-`uname -r` -y
```

# Init zshrc
```sh
# If you come from bash you might have to change your $PATH.
export PATH=$HOME/bin:/usr/local/bin:/usr/libexec/docker/cli-plugins:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="fino-time"
#ZSH_THEME="random"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
# 
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

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
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
```