```
alias ndc='nvidia-docker-compose'
alias ndcud='nvidia-docker-compose up -d'
alias deit='docker exec -i -t'
alias dc='docker-compose'
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
```


