1. 安装
```shell
 wget https://mirror.ghproxy.com/https://github.com/mozilla/sccache/releases/download/v0.7.6/sccache-v0.7.6-x86_64-unknown-linux-musl.tar.gz
mv sccache /usr/bin
```
2. 配置S3
```
export RUSTC_WRAPPER=/usr/local/bin/sccache
export AWS_ACCESS_KEY_ID=FFVAYWLfxSubfTcfjUns
export AWS_SECRET_ACCESS_KEY=MgD4NOBWvZTjPcsLnwGhZchhnY7oULQRgZbIpAjo
export SCCACHE_BUCKET=cache
export SCCACHE_ENDPOINT=https://minio-api.haihuman.com
export SCCACHE_S3_USE_SSL=true
export SCCACHE_REGION=auto
```
3. 清除缓存
```
sccache --clear
cargo clean
cargo build
```