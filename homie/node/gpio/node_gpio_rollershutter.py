from homie.node.node_rollershutter import Node_Rollershutter

import RPi.GPIO as GPIO

class GPIO_Rollershutter(Node_Rollershutter):
    def __init__(
        self,
        device,
        gpio_up,
        gpio_down,
        id="rollershutter",
        name="Roller Shutter",
        type_="rollershutter",
        retain=True,
        qos=1,
        time_full = 10000,
        time_extra = 1000,
        time_pause = 1000,
    ):
        super().__init__(
            device,
            id,
            name,
            type_,
            retain,
            qos,
            time_full,
            time_extra,
            time_pause,
            set_up=self.gpio_set_up,
            set_down=self.gpio_set_down)

        self.gpio_up = gpio_up
        self.gpio_down = gpio_down
        GPIO.setup(gpio_up, GPIO.OUT)
        GPIO.setup(gpio_down, GPIO.OUT)

    def gpio_set_up(self, state):
        pass
        GPIO.output(self.gpio_up, state)

    def gpio_set_down(self, state):
        pass
        GPIO.output(self.gpio_down, state)

