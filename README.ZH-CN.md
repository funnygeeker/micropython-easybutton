[English (英语)](./README.md)
# micropython-easybutton
- 使用用中断和循环实现按钮状态识别，按钮按下时执行指定函数，适用于 `micropython`

### 功能
- 按钮按下后，每隔一段时间执行一次函数
- 按钮短按后，松开时执行函数
- 按钮长按后，松开时执行函数
- 按钮按下时执行函数
- 按钮松开时执行函数

### 说明
`./main.py` 为使用示例文件
`./libs/easybutton.py` 为按钮库文件

### 示例
- 在本次示例中，按钮所在的引脚接按钮，按钮接的是 `GND`

```python
import time
from machine import Pin
from libs.easybutton import EasyButton

# 初始化按钮
btn = Pin(2, Pin.IN, Pin.PULL_UP)
b = EasyButton(btn)  # 还有更多参数可以设置，详见源码注释，如果有不规范的命名，请提交 PR，我们会修正


# 定义函数，可以先定义，也可以后续使用匿名函数
def test():
    print("up")


b.set_down(lambda: print("down"))  # 按钮按下时执行函数
b.set_hold(lambda: print("hold"))  # 按钮按下后，每隔一段时间执行一次函数
b.set_short(lambda: print("short"))  # 按钮短按后，松开时执行函数
b.set_long(lambda: print("long"))  # 按钮长按后，松开时执行函数
b.set_up(test)  # 按钮松开时执行函数

# 可以通过修改 xx_func 来启用或者禁用对应的函数，比如：
b.up_func = False  # 禁用松开按钮时执行的函数

# 由于使用了中断，所以后续可以继续执行代码，只有在按钮被按下时才会暂停继续执行的代码，松开则恢复
while True:
    print("---- running ----")
    time.sleep(1)
```
