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
    def __init__(self, button: Pin, cycle_time: int = 500, hold_time: int = 1000, interval_time: int = 500):
        """
        Args:
            button: 例如： `Pin(2, Pin.IN, Pin.PULL_UP)`
            cycle_time: 按下的后的每个判断周期时长，单位：毫秒
            hold_time: 按钮按下行为判定为长按的时间，单位：毫秒
            interval_time: 两次按键的检测间隔时间，单位：毫秒
        """
        self.__cycle_num = 1
        '周期函数执行次数'
        self.__interval = 0
        '按钮按下时到松开时的时间间隔'
        self.button = button
        '按钮对象'
        self.cycle_time = cycle_time
        '按下的后的每个判断周期时长，单位：毫秒'
        self.hold_time = hold_time
        '按钮按下行为判定为长按的时间，单位：毫秒'
        self.interval_time = interval_time
        '两次按键的检测间隔时间，单位：毫秒'
        self._start_time = 0
        '按钮被按下的开始时间，单位：毫秒'
        self.irq = self.button.irq(handler=self._detection, trigger=Pin.IRQ_FALLING)
        '按钮是否被按下的状态'
        self.__up = None
        '按钮按下时执行的函数'
        self.__down = None
        '按钮松开时执行的函数'
        self.__hold = None
        '按钮长按松开时执行的函数'
        self.__cycle = None
        '按钮按下时每个周期执行的函数'
        self.up_state = True
        '按钮松开时对应函数的启用状态'
        self.down_state = True
        '按钮按下时对应函数的启用状态'
        self.hold_state = True
        '按钮长按松开时对应函数的启用状态'
        self.cycle_state = True
        '按钮按下时每个周期对应函数的启用状态'

    def _detection(self, pin):
        if time.ticks_ms() > self._start_time + self.__interval + self.interval_time:  # 防止由按钮接触原因造成的双击现象
            self._down()  # 执行按钮被按下的函数
            self._start_time = time.ticks_ms()  # 获取当前被按下的开始时间
            while not self.button.value():  # 在按钮松开之前一直循环
                self.__interval = time.ticks_ms() - self._start_time  # 获取现在和开始之间的时差
                if self.__interval > self.cycle_time * self.__cycle_num:  # 每达到一个周期执行一次周期函数
                    self.__cycle_num += 1
                    self._cycle()
                time.sleep_ms(50)  # 不知道这样能不能稍微节省一点点功耗，减少计算次数()
            if self.__interval > self.hold_time:  # 如果按钮判断为长按
                self._hold()
            self.__cycle_num = 1  # 复位周期函数执行次数
            self._up()  # 执行按钮被松开的函数

    def _up(self):
        if self.__up and self.up_state:
            self.__up()

    def _down(self):
        if self.__down and self.down_state:
            self.__down()

    def _cycle(self):
        if self.__cycle and self.cycle_state:
            self.__cycle()

    def _hold(self):
        if self.__hold and self.hold_state:
            self.__hold()

    def set_up(self, func):
        """设置按钮松开时执行的函数"""
        self.__up = func

    def set_down(self, func):
        """设置按钮松开时执行的函数"""
        self.__down = func

    def set_hold(self, func, hold_time: int = None):
        """设置按钮长按时执行的函数"""
        if hold_time:
            self.hold_time = hold_time
        self.__hold = func

    def set_cycle(self, func, cycle_time: int = None):
        """设置按钮按下时每个周期执行的函数"""
        if cycle_time:
            self.cycle_time = cycle_time
        self.__cycle = func
