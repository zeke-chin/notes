```python
import json
from html import escape

def dict_to_highlighted_html(data, indent=0):
    """
    将字典或列表转换为带语法高亮的 HTML
    
    Args:
        data: 要转换的字典或列表
        indent: 当前缩进级别
    
    Returns:
        str: HTML 字符串
    """
    # 颜色定义
    colors = {
        'bracket': '#6a737d',  # 灰色 - 括号、冒号、逗号
        'key': '#005cc5',      # 蓝色 - 键名
        'string': '#22863a',   # 绿色 - 字符串值
        'number': '#b31d28',   # 红色 - 数字值
        'boolean': '#b31d28',  # 红色 - 布尔值
        'null': '#b31d28'      # 红色 - null值
    }
    
    def get_indent_str(level):
        """获取缩进字符串"""
        return '    ' * level
    
    def format_value(value, current_indent):
        """格式化值"""
        if value is None:
            return f'<span style="color:{colors["null"]}">null</span>'
        elif isinstance(value, bool):
            return f'<span style="color:{colors["boolean"]}">{"true" if value else "false"}</span>'
        elif isinstance(value, (int, float)):
            return f'<span style="color:{colors["number"]}">{value}</span>'
        elif isinstance(value, str):
            # 转义特殊字符并添加引号
            escaped_value = escape(value).replace('"', '&quot;')
            return f'<span style="color:{colors["string"]}">"{escaped_value}"</span>'
        elif isinstance(value, list):
            return format_list(value, current_indent)
        elif isinstance(value, dict):
            return format_dict(value, current_indent)
        else:
            # 其他类型转为字符串
            return f'<span style="color:{colors["string"]}">"{escape(str(value))}"</span>'
    
    def format_list(lst, current_indent):
        """格式化列表"""
        if not lst:
            return f'<span style="color:{colors["bracket"]}">[]</span>'
        
        result = f'<span style="color:{colors["bracket"]}">[</span>\n'
        for i, item in enumerate(lst):
            indent_str = get_indent_str(current_indent + 1)
            result += indent_str
            result += format_value(item, current_indent + 1)
            if i < len(lst) - 1:
                result += f'<span style="color:{colors["bracket"]}">,</span>'
            result += '\n'
        result += get_indent_str(current_indent) + f'<span style="color:{colors["bracket"]}">]</span>'
        return result
    
    def format_dict(dct, current_indent):
        """格式化字典"""
        if not dct:
            return f'<span style="color:{colors["bracket"]}">{{}}</span>'
        
        result = f'<span style="color:{colors["bracket"]}>{{</span>\n'
        items = list(dct.items())
        for i, (key, value) in enumerate(items):
            indent_str = get_indent_str(current_indent + 1)
            result += indent_str
            result += f'<span style="color:{colors["key"]}">"{escape(key)}"</span>'
            result += f'<span style="color:{colors["bracket"]}">: </span>'
            result += format_value(value, current_indent + 1)
            if i < len(items) - 1:
                result += f'<span style="color:{colors["bracket"]}">,</span>'
            result += '\n'
        result += get_indent_str(current_indent) + f'<span style="color:{colors["bracket"]}">}}</span>'
        return result
    
    # 开始格式化
    if isinstance(data, dict):
        html_content = format_dict(data, indent)
    elif isinstance(data, list):
        html_content = format_list(data, indent)
    else:
        html_content = format_value(data, indent)
    
    # 包装成完整的 HTML
    full_html = f'<div>\n<pre style="margin:0">{html_content}</pre>\n</div>'
    return full_html


def json_to_highlighted_html(json_str):
    """
    将 JSON 字符串转换为带语法高亮的 HTML
    
    Args:
        json_str: JSON 字符串
    
    Returns:
        str: HTML 字符串
    """
    try:
        data = json.loads(json_str)
        return dict_to_highlighted_html(data)
    except json.JSONDecodeError as e:
        return f"<div><pre>JSON 解析错误: {e}</pre></div>"


# 使用示例
if __name__ == "__main__":
    # 示例1：简单字典
    data1 = {
        "category": "goodsNameOptimize",
        "algResData": '{"goosIds": [123, 456]}',
        "content": "帮我优化商品标题"
    }
    
    # 示例2：复杂字典
    data2 = {
        "result": [
            {
                "goodsId": "101",
                "original_title": "原标题",
                "generate_title": "新标题",
                "id": 1001
            },
            {
                "goodsId": "102",
                "original_title": "原标题",
                "generate_title": "新标题",
                "id": 1002
            }
        ],
        "success_count": 10,
        "total_count": 10,
        "task_id": 31321,
        "type": 15
    }
    
    # 生成 HTML
    html1 = dict_to_highlighted_html(data1)
    print("示例1 HTML:")
    print(html1)
    print("\n" + "="*50 + "\n")
    
    html2 = dict_to_highlighted_html(data2)
    print("示例2 HTML:")
    print(html2)
    
    # 也可以从 JSON 字符串生成
    json_str = '{"name": "测试", "age": 25, "active": true, "score": null}'
    html3 = json_to_highlighted_html(json_str)
    print("\n" + "="*50 + "\n")
    print("从 JSON 字符串生成:")
    print(html3)
    
    # 保存到文件
    with open("output.html", "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>JSON Viewer</title>
    <style>
        body { font-family: monospace; background: #f5f5f5; padding: 20px; }
        div { background: white; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
""")
        f.write(html1)
        f.write(html2)
        f.write(html3)
        f.write("</body></html>")
    
    print("\nHTML 已保存到 output.html")
```


示例 
```html
<div> <pre style="margin:0"><span style="color:#6a737d">{</span> &nbsp; &nbsp; <span style="color:#005cc5">"category"</span><span style="color:#6a737d">: </span><span style="color:#22863a">"goodsNameOptimize"</span><span style="color:#6a737d">,</span> &nbsp; &nbsp; <span style="color:#005cc5">"algResData"</span><span style="color:#6a737d">: </span><span style="color:#22863a">"{\"goosIds\": [</span><span style="color:#b31d28">123</span><span style="color:#6a737d">, </span><span style="color:#b31d28">456</span><span style="color:#22863a">]}"</span><span style="color:#6a737d">,</span> &nbsp; &nbsp; <span style="color:#005cc5">"content"</span><span style="color:#6a737d">: </span><span style="color:#22863a">"帮我优化商品标题"</span> <span style="color:#6a737d">}</span></pre> </div>
```