[English (英语)](./README.md)
# micropython-easybutton
- 使用中断实现的多种按钮状态识别，按钮按下时执行指定函数，适用于 `micropython`

### 功能
- 按钮按下后，每隔一段时间执行一次函数
- 按钮短按后，松开时执行函数
- 按钮长按后，松开时执行函数
- 按钮按下时执行函数
- 按钮松开时执行函数

### 说明
`./main.py` 为使用示例文件
`./lib/easybutton.py` 为按钮库文件

### 示例
- 在本次示例中，按钮所在的引脚接按钮，按钮接的是 `GND`

```python
import time
from machine import Pin
from lib.easybutton import EasyButton

# Initialize the button
btn = Pin(2, Pin.IN, Pin.PULL_UP)
# if there are any non-standard naming, please submit a PR, thanks.
# 如果有不规范的命名，请提交 PR，谢谢
b = EasyButton(btn)

# Define functions, they can be defined first or later used as anonymous functions
# 定义函数，可以先定义，也可以后续使用匿名函数
def test():
    print("up")

# Set trigger functions for the button
b.down_func = lambda: print("down")  # Executed when the button is pressed  # 按钮按下时执行
b.hold_func = lambda: print("hold")  # Executed at regular intervals after the button is pressed  # 按钮按下后，每隔一段时间执行一次
b.short_func = lambda: print("short")  # Executed when the button is short pressed and released  # 按钮短按后，松开时执行
b.long_func = (print, "long")  # Executed when the button is long pressed and released  # 按钮长按后，松开时执行
b.up_func = test  # Executed when the button is released  # 按钮松开时执行函数

# Since an interrupt is used, the code can continue to execute, and it will only pause when the button is pressed.
# 由于使用了中断，所以后续可以继续执行代码，只有在按钮被按下时才会暂停继续执行的代码，松开则恢复
# This loop is not necessary, it's just for demonstration purposes. It's not necessary in actual use.
# 这里的循环并不是必须，仅为演示使用，实际使用中并非必要
while True:
    print("---- running ----")
    time.sleep(1)
```
