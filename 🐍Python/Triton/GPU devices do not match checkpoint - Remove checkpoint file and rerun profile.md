1. 报错：
```
14:09:16 [Model Analyzer] Initializing GPUDevice handles
14:09:17 [Model Analyzer] Using GPU 0 NVIDIA GeForce RTX 3090 with UUID GPU-34ebebfa-2ec3-53fc-93c1-21ebfe9bc0f0
14:09:17 [Model Analyzer] WARNING: Overriding the output model repo path "/workspace/behavior_emotion_multi_测试报告/output_model_repository"
14:09:17 [Model Analyzer] Starting a local Triton Server
14:09:17 [Model Analyzer] Loaded checkpoint from file /workspace/behavior_emotion_multi_测试报告/checkpoints/0.ckpt
Traceback (most recent call last):
  File "/usr/local/bin/model-analyzer", line 8, in <module>
    sys.exit(main())
  File "/usr/local/lib/python3.10/dist-packages/model_analyzer/entrypoint.py", line 267, in main
    analyzer.profile(client=client,
  File "/usr/local/lib/python3.10/dist-packages/model_analyzer/analyzer.py", line 115, in profile
    self._get_server_only_metrics(client, gpus)
  File "/usr/local/lib/python3.10/dist-packages/model_analyzer/analyzer.py", line 201, in _get_server_only_metrics
    raise TritonModelAnalyzerException(
model_analyzer.model_analyzer_exceptions.TritonModelAnalyzerException: GPU devices do not match checkpoint - Remove checkpoint file and rerun profile
```

2. 原因 
Model Analyzer使用检查点文件来保存和恢复进度。如果你更改了GPU设置，或者如果Model Analyzer在与之前不同的环境中运行（例如，不同的Docker容器，或系统配置发生变化后），就可能会出现这种不匹配。

3. 解决方案 删除之前生成的文件
```
root@c67b4fbd5109:/workspace/behavior_emotion_multi_测试报告# ls
checkpoints  config.pbtxt  config.yml  docker-compose.yml  output_model_repository
root@c67b4fbd5109:/workspace/behavior_emotion_multi_测试报告# rm -r checkpoints output_model_repository
```

