```yaml
FROM ubuntu:22.04

ENV TZ=Asia/Shanghai LANG=zh_CN.UTF-8 LANGUAGE=zh_CN:zh LC_ALL=zh_CN.UTF-8 DEBIAN_FRONTEND=noninteractive

RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
	language-pack-zh-hans \
	vim \
	jq \
	curl \
	wget \
	git \
	unzip \
	locales \
	tzdata


# 修改时区设置部分
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "set encoding=utf-8" >> /etc/vim/vimrc \
    && echo "set termencoding=utf-8" >> /etc/vim/vimrc \
    && echo "set fileencoding=utf-8" >> /etc/vim/vimrc \
    && echo "set fileencodings=utf-8,ucs-bom,gb18030,gbk,gb2312,cp936" >> /etc/vim/vimrc \
    && locale-gen zh_CN.UTF-8
```