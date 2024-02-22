

## 阿里源
``` Dockerfile
RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list
```

## 浙江大学
``` Dockerfile
RUN sed -i 's#archive.ubuntu.com#mirrors.zju.edu.cn#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.zju.edu.cn#g' /etc/apt/sources.list
```