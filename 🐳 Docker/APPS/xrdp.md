```yaml
version: "3.8"
services:
  uxrdp:
    image: danielguerra/ubuntu-xrdp:20.04
    container_name: uxrdp
    hostname: terminalserver
    shm_size: 1g
    ports:
      - "7189:3389"
      - "7122:22"
    volumes:
      - ./data:/root
```


`dockerfile`
```dockerfile
FROM danielguerra/ubuntu-xrdp:20.04 AS builder
RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list
ENV LANG=zh_CN.UTF-8 LANGUAGE=zh_CN:zh LC_ALL=zh_CN.UTF-8 DEBIAN_FRONTEND=noninteractive
RUN rm -rf  /etc/apt/sources.list.d/  && apt update


RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping \
    wget \
    zsh \
    ranger \
    neofetch \
    build-essential \
    cmake \
    git \
    curl \
    vim \
    htop \
    iptables \
    zip \
    unzip \
    ca-certificates \
    fonts-wqy-zenhei \
    language-pack-zh-hans

RUN locale-gen zh_CN.UTF-8
RUN dpkg-reconfigure locales


# 配置zsh
FROM builder as zsh
RUN wget https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh -O /root/install.sh
RUN sed -i 's#REPO=${REPO:-ohmyzsh/ohmyzsh}#REPO=${REPO:-mirrors/oh-my-zsh}#g' /root/install.sh && \
    sed -i 's#REMOTE=${REMOTE:-https://github.com/${REPO}.git}#REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}#g' /root/install.sh && \
    chmod +777 /root/install.sh && \
    ./root/install.sh && \
    rm /root/install.sh
RUN git clone https://kgithub.com/Zeke-chin/my-config /root/my-config && \
    rm /root/.zshrc && \
    ln -s /root/my-config/.zshrc /root/.zshrc
RUN git clone https://kgithub.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://kgithub.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
RUN chsh -s `which zsh`


FROM builder AS conda
ENV MINICONDA_VERSION 3
ENV CONDA_FORGE https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
RUN chsh -s `which zsh`
RUN curl -o ~/miniconda.sh -O  https://mirrors.bfsu.edu.cn/anaconda/miniconda/Miniconda${MINICONDA_VERSION}-latest-Linux-x86_64.sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
RUN ln /opt/conda/bin/conda /usr/local/bin/conda
RUN conda init zsh
RUN conda install mamba -n base -c ${CONDA_FORGE}
RUN ln /opt/conda/bin/mamba /usr/local/bin/mamba && mamba init zsh
```