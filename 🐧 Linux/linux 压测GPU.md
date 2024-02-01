1. https://github.com/OguzPastirmaci/gpu-burn


https://github.com/OguzPastirmaci/gpu-burn
```
 docker run -it --rm --gpus all --entrypoint bash oguzpastirmaci/gpu-burn
```

2. **使用方法：**

`gpu_burn [选项] [时间]`

**选项：**

- **-m X**：使用 X MB 的内存。
- **-m N%**：使用 N% 的可用 GPU 内存。
- **-d**：使用双精度浮点数进行计算。
- **-tc**：尝试使用 Tensor 核心（如果可用）。
- **-l**：列出系统中所有 GPU 的列表。
- **-i N**：仅在 GPU N 上执行测试。
- **-h**：显示帮助信息。

**示例：**

`gpu_burn -d 3600` 这会使用双精度浮点数进行计算，并运行 3600 秒。

3. GPU计算能力
`nvidia-smi --query-gpu=compute_cap --format=csv`