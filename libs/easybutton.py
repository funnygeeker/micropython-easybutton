# EasyButton_1.0.0 https://github.com/funnygeeker/micropython-easybutton
# 参考资料：
# MicroPython优雅的实现中断：https://www.skyone.host/2021/05/13/micropython-you-ya-de-shi-xian-zhong-duan/
import time
from machine import Pin


class EasyButton:
    """
    利用中断和循环实现按钮状态的识别，可以在按钮按下时执行指定函数，适用于 `micropython`
        - Author: funnygeeker
        - License: MIT
    """

    def __init__(self, button: Pin, hold: int = 350, long: int = 1000, interval: int = 30):
        """
        Args:
            button: 例如：`Pin(2, Pin.IN, Pin.PULL_UP)`
            hold: 按下的后的每个判断周期时长，单位：毫秒
            long: 按钮按下行为判定为长按的时间，单位：毫秒
            interval: 两次按键的检测间隔时间，单位：毫秒
        """
        self.__num = 1
        'hold 函数执行次数（循环次数）'
        self.__interval = 0
        '上一次按钮按下时到松开时的时间间隔，单位：毫秒'
        self.__end_time = 0
        '上一次按钮被按下的结束时间，单位：毫秒'
        self.__start_time = 0
        '按钮被按下的开始时间，单位：毫秒'
        self.button = button
        '按钮对象'
        self.hold_time = hold
        '按下的后函数每隔多久执行一次，单位：毫秒'
        self.long_time = long
        '按钮按下行为判定为长按的时间，单位：毫秒'
        self.interval_time = interval
        '两次按键的检测间隔时间，单位：毫秒'
        self.irq = self.button.irq(handler=self._detection, trigger=Pin.IRQ_FALLING)
        'https://docs.micropython.org/en/latest/library/machine.Pin.html'
        self.__up = None
        '按钮按下时执行的函数'
        self.__down = None
        '按钮松开时执行的函数'
        self.__long = None
        '按钮长按松开时执行的函数'
        self.__hold = None
        '按钮按下时每隔一段时间执行的函数'
        self.__short = None
        '按钮短按松开时执行的函数'
        self.up_state = True
        '按钮松开时对应函数的启用状态'
        self.down_state = True
        '按钮按下时对应函数的启用状态'
        self.long_state = True
        '按钮长按松开时对应函数的启用状态'
        self.hold_state = True
        '按钮按下时每隔一段时间对应函数的启用状态'
        self.short_state = True
        '按钮短按松开时对应函数的启用状态'

    def _detection(self, pin):
        # 防止由按钮接触原因造成的双击现象
        if time.ticks_ms() > self.__end_time + self.interval_time:
            self.__start_time = time.ticks_ms()
            self._down()  # 执行按钮被按下的函数
            while not self.button.value():  # 在按钮松开之前一直循环
                self.__interval = time.ticks_ms() - self.__start_time  # 获取现在和开始之间的时差
                if self.__interval > self.hold_time * self.__num:  # 每达到一个周期执行一次周期函数
                    self.__num += 1
                    self._hold()
            if self.__interval > self.long_time:  # 如果按钮判断为长按
                self._long()
            else:
                self._short()
            self._up()  # 执行按钮被松开的函数
            self.__num = 1  # 复位周期函数执行次数
            self.__run_time = 0  # 复位函数运行时消耗的时间
            self.__end_time = time.ticks_ms()  # 获取当前被按下的开始时间

    def _up(self):
        if self.__up and self.up_state:
            self.__up()

    def _down(self):
        if self.__down and self.down_state:
            self.__down()

    def _hold(self):
        if self.__hold and self.hold_state:
            self.__hold()

    def _long(self):
        if self.__long and self.long_state:
            self.__long()

    def _short(self):
        if self.__short and self.short_state:
            self.__short()

    def set_up(self, func):
        """设置按钮松开时执行的函数"""
        self.__up = func

    def set_down(self, func):
        """设置按钮松开时执行的函数"""
        self.__down = func

    def set_long(self, func, long: int = None):
        """设置按钮长按时执行的函数"""
        if long:
            self.long_time = long
        self.__long = func

    def set_hold(self, func, hold: int = None):
        """设置按钮按下时每个周期执行的函数"""
        if hold:
            self.hold_time = hold
        self.__hold = func

    def set_short(self, func, hold: int = None):
        """设置按钮短按松开后执行的函数"""
        if hold:
            self.hold_time = hold
        self.__short = func
