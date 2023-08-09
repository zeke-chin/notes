1. 描述
dev和test环境都有一样的模型、服务
test正常 -> 15G 内存 使用70%
dev报错 -> 10G 内存 使用70%

2. 问题所在
内存 不足 但是triton只会爆
```
I0809 05:31:51.687639 49 stub_launcher.cc:257] Starting Python backend stub: exec /opt/tritonserver/backends/python/triton_python_backend_stub /app/models/faq-inference_hi/1/model.py triton_python_backend_shm_region_7 67108864 67108864 49 /opt/tritonserver/backends/python 336 faq-inference_hi_0_1  
I0809 05:32:23.259680 49 python_be.cc:2224] TRITONBACKEND_ModelInstanceExecute: model instance name faq-inference_hi_0_1 released 1 requests
```