1. 查看网络结构
- `pip install bigmodelvis -i https://mirror.baidu.com/pypi/simple`
``` python
from transformers import BertTokenizer, BertModel
from bigmodelvis import Visualization

model = BertModel.from_pretrained("bert-base-uncased")
model_vis = Visualization(model)
model_vis.structure_graph()
```
![[Pasted image 20231130135413.png]]

2. 查看onnx输入输出 
