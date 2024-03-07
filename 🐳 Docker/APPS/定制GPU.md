```yaml
services:
  test:
    image: nvidia/cuda:10.2-base
    command: nvidia-smi
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s
      resources:
        limits:
          cpus: "0.50"
          memory: 50M
        reservations:
          cpus: "0.25"
          memory: 20M
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu, utility]
            - capabilities: ["gpu"]
              device_ids: ["GPU-e22d27e9-e9e5-3653-0bd4-1312b0a12db5"]
      update_config:
        parallelism: 2
        delay: 10s
        order: stop-first
```