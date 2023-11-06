
1. 添加内核
```bash
conda install ipython ipykernel -y 
python -m ipykernel install --user --name py38 --display-name "py38"
```
2. 查看内核列表
```bash
jupyter kernelspec list
```
3. 卸载内核
```bash
jupyter kernelspec remove kernel_name
```

python -m ipykernel install --user --name py10_milvus --display-name "py10_milvus"


jupyter kernelspec remove py38 -y