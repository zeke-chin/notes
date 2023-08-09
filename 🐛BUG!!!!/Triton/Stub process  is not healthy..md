1. 描述
dev和test环境都有一样的模型、服务
test正常 -> 15G 内存 使用70%
dev报错 -> 10G 内存 使用70%

2. 问题所在
内存 不足 但是triton只会bao