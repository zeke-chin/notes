```yaml
version: '3'
services:
  jupyter:
    hostname: jupyter
    container_name: jupyter
    restart: always
    image: registry.cn-shanghai.aliyuncs.com/zekechin/jupyter:cpu_py310
    privileged: true
    ipc: host
    tty: true
    working_dir: /
    ports:
      - '30388:8888'
      - '30122:22'
    volumes:
      - /root:/mnt_root
      - ./j_ws:/jupyter
```

`Dockerfile`
```
FROM nvidia/cuda:11.0-cudnn8-devel-ubuntu18.04 AS builder

RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list

ENV LANG=zh_CN.UTF-8 LANGUAGE=zh_CN:zh LC_ALL=zh_CN.UTF-8 DEBIAN_FRONTEND=noninteractive

RUN rm -rf  /etc/apt/sources.list.d/  && apt update

RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    tmux \
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
    libjpeg-dev \
    libpng-dev \
    iptables \
    zip \
    unzip \
    openssh-server \
    ca-certificates \
    language-pack-zh-hans \
    ttf-wqy-zenhei \
    libglib2.0-0 \
    locales \
    clang \
    libgl1 \
    libxext6 \
    libsm6 \
    ffmpeg \
    ca-certificates \
    autojump \
    libgl1-mesa-glx


RUN locale-gen zh_CN.UTF-8
RUN dpkg-reconfigure locales

CMD ["supervisord", "-n"]


# 配置ssh
FROM builder as builder1
RUN mkdir /var/run/sshd
RUN echo 'root:113113' | chpasswd
RUN sed -i 's/.*PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
RUN echo "\
[program:sshd] \n\
command=/usr/sbin/sshd -D\n\
autorestart=True\n\
autostart=True\n\
redirect_stderr = true\n\
" > /etc/supervisor/conf.d/sshd.conf
EXPOSE 22

# 配置zsh
FROM builder1 as builder2
RUN wget https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh -O /root/install.sh
RUN sed -i 's#REPO=${REPO:-ohmyzsh/ohmyzsh}#REPO=${REPO:-mirrors/oh-my-zsh}#g' /root/install.sh && \
    sed -i 's#REMOTE=${REMOTE:-https://github.com/${REPO}.git}#REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}#g' /root/install.sh && \
    chmod +777 /root/install.sh && \
    ./root/install.sh && \
    rm /root/install.sh
RUN git clone https://gitclone.com/github.com/Zeke-chin/my-config /root/my-config && \
    rm /root/.zshrc && \
    ln -s /root/my-config/.zshrc /root/.zshrc
RUN git clone https://gitclone.com/github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://gitclone.com/github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
RUN chsh -s `which zsh`

# # 配置zerotier
# FROM builder2 as builder3
# RUN apt install 
# RUN git clone https://gitclone.com/github.com/Zeke-chin/zerotier-one /root/zerotier-one && \
#     cp /root/zerotier-one/zero* /usr/sbin/
# RUN ln -sf /usr/sbin/zerotier-one /usr/sbin/zerotier-idtool && \
#     ln -sf /usr/sbin/zerotier-one /usr/sbin/zerotier-cli && \
#     rm -r /root/zerotier-one
# EXPOSE 9993

# 配置conda、mamba
WORKDIR /root/my-config
RUN git pull
FROM builder2 as builder3
ENV PYTHON_VERSION 3
RUN chsh -s `which zsh`
RUN curl -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda${PYTHON_VERSION}-latest-Linux-x86_64.sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
RUN ln /opt/conda/bin/conda /usr/local/bin/conda
RUN conda init zsh
RUN conda install mamba -n base -c conda-forge
RUN ln /opt/conda/bin/mamba /usr/local/bin/mamba && mamba init zsh

# 配置jupyter
FROM builder3 as builder4
RUN mamba install -y jupyterlab -n base 
RUN /opt/conda/bin/pip install jupyterlab-language-pack-zh-CN -i https://mirror.baidu.com/pypi/simple
WORKDIR /jupyter
RUN /opt/conda/bin/jupyter notebook --generate-config && \
    cp -f /root/my-config/jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

RUN echo "\
[program:jupyter]\n\
directory=/\n\
command=/opt/conda/bin/jupyter lab --ip 0.0.0.0 --port 8888 --allow-root \n\
autorestart=true\n\
startretries=0\n\
redirect_stderr=true\n\
stdout_logfile=/dev/stdout\n\
stdout_logfile_maxbytes=0\n\
" > /etc/supervisor/conf.d/jupyter.conf
EXPOSE 8888

# 配置paddle环境
FROM builder4 as builder5
WORKDIR /jupyter
ADD environment.yml /environment.yml
RUN sed -i 's#- paddlepaddle#- paddlepaddle-gpu==2.3.0.post110#g' /environment.yml && cat /environment.yml
RUN mamba update -n base -c defaults conda -y && mamba env create -f /environment.yml && rm -rf /root/.cache

RUN /opt/conda/envs/py38/bin/python -m ipykernel install --name py38 --display-name "py38"
RUN echo "c.MultiKernelManager.default_kernel_name = 'py38'">>/root/.jupyter/jupyter_notebook_config.py

```