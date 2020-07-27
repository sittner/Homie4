from homie.node.node_switch import Node_Switch

import RPi.GPIO as GPIO

class GPIO_Switch(Node_Switch):
    def __init__(
        self,
        device,
        gpio,
        id="switch",
        name="Switch",
        type_="switch",
        retain=True,
        qos=1,
        max_on_time = 0,
    ):
        super().__init__(device, id, name, type_, retain, qos, self.set_switch, max_on_time)
        self.gpio = gpio
        GPIO.setup(gpio, GPIO.OUT)

    def set_switch(self, state):
        pass
        GPIO.output(self.gpio, state)

