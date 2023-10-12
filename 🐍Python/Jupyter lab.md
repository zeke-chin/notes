
1. 添加内核
```
conda install ipython ipykernel -y 
python -m ipykernel install --user --name py38 --display-name "py38"
```
2. 查看内核列表
```
jupyter kernelspec list
```
1. 

python -m ipykernel install --user --name torch --display-name "torch"