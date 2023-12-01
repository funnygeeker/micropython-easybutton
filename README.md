[简体中文 (Chinese)](./README.ZH-CN.md)
# micropython-easybutton
- Recognize button status using interrupts and loops, suitable for `micropython`

### Features
- Execute a specified function at regular intervals after the button is pressed
- Execute a function when the button is released after a short press
- Execute a function when the button is released after a long press
- Execute a function when the button is pressed
- Execute a function when the button is released

### Notes
- `./main.py` is the example file
- `./libs/easybutton.py` is the button library file

### Example
- In this example, the button is connected to a pin and the other end is connected to `GND`

```python
import time
from machine import Pin
from libs.easybutton import EasyButton

# Initialize the button
btn = Pin(2, Pin.IN, Pin.PULL_UP)
b = EasyButton(btn)  # There are more parameters you can set, see source code comments for details. If you find any naming inconsistencies, please submit a PR and we will correct them.

# Define functions, you can define them earlier or use anonymous functions later
def test():
    print("up")

b.set_down(lambda: print("down"))  # Execute the function when the button is pressed
b.set_hold(lambda: print("hold"))  # Execute the function at regular intervals after the button is pressed
b.set_short(lambda: print("short"))  # Execute the function when the button is released after a short press
b.set_long(lambda: print("long"))  # Execute the function when the button is released after a long press
b.set_up(test)  # Execute the function when the button is released

# You can enable or disable corresponding functions by modifying xx_func, for example:
b.up_func = False  # Disable the function executed when the button is released

# Since interrupts are used, you can continue executing code later. The code execution will only pause when the button is pressed and resume when released.
while True:
    print("---- running ----")
    time.sleep(1)
```