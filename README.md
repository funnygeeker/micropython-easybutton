# micropython-easybutton
利用中断和循环实现按钮状态的识别，可以在按钮按下时执行指定函数，适用于 micropython

### 功能
- 按钮按下后，每隔一段时间执行一次函数
- 按钮长按后，松开时执行函数
- 按钮按下时执行函数
- 按钮松开时执行函数

### 说明
`./main.py` 为使用示例文件
`./libs/easybutton.py` 为按钮库文件

### 示例
```python
import time
from machine import Pin
from libs import EasyButton


# 初始化按钮
btn = Pin(2, Pin.IN, Pin.PULL_UP)
b = EasyButton(btn)  # 还有更多参数可以设置，详见源码注释，如果有不规范的命名，请提交 PR，我们会修正

# 定义函数，可以先定义也可以用匿名函数
def test():
    print("up")

mid.set_down(lambda x: print("down"))  # 按钮按下时执行函数
mid.set_cycle(lambda x: print("cycle"))  # 按钮按下后，每隔一段时间执行一次函数
mid.set_hold(lambda x: print("hold"))  # 按钮长按后，松开时执行函数
mid.set_up(test)  # 按钮松开时执行函数

# 由于使用了中断，所以后续可以继续执行代码，只有在按钮被按下时才会暂停继续执行的代码，松开则恢复
while True:
    print("---- running ----")
    time.sleep(1)
```
