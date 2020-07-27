from .node_base import Node_Base

import time

from homie.device_base import Device_Base
from homie.node.property.property_enum import Property_Enum
from homie.node.property.property_integer import Property_Integer

class Node_Rollershutter(Node_Base):
    def __init__(
        self,
        device,
        id="rollershutter",
        name="Roller Shutter",
        type_="rollershutter",
        retain=True,
        qos=1,
        time_full = 10000,
        time_extra = 1000,
        time_pause = 1000,
        set_up=None,
        set_down=None,
    ):
        super().__init__(device, id, name, type_, retain, qos)

        assert set_up  # must provide a function to set the value of the up relay
        assert set_down  # must provide a function to set the value of the down relay

        self.prop_cmd = Property_Enum(
            self,
            id="cmd",
            name="Roller Shutter Command",
            value="STOP",
            data_format="STOP,UP,DOWN",
            set_value=self.handle_cmd)
        self.add_property(self.prop_cmd)

        self.prop_pos = Property_Integer(
            self,
            id="state",
            name="Roller Shutter State",
            settable=False,
            unit="%",
            data_format="0:100",
            restore=True,
            set_value=self.handle_pos)
        self.add_property(self.prop_pos)

        self.time_full = time_full
        self.time_extra = time_extra
        self.time_pause = time_pause
        self.set_up = set_up
        self.set_down = set_down

        self.out = 0
        self.pos = 0

        now = Device_Base.monotonic_ms()
        self.last_up = now
        self.last_down = now

    def periodic(self, now, dt):
        self.out = 0
        if self.prop_cmd.value == "DOWN" and now >= (self.last_down + self.time_pause):
            self.out = 1
        if self.prop_cmd.value == "UP" and now >= (self.last_up + self.time_pause):
            self.out = -1

        if self.out > 0:
            self.last_up = now
            self.pos += dt
            self.set_up(False)
            self.set_down(True)
            if self.pos >= (self.time_full + self.time_extra):
                self.prop_cmd.value = "STOP"
                self.pos = self.time_full

        if self.out < 0:
            self.last_down = now
            self.pos -= dt
            self.set_down(False)
            self.set_up(True)
            if self.pos <= (0 - self.time_extra):
                self.prop_cmd.value = "STOP"
                self.pos = 0

        if self.out == 0:
            self.set_up(False)
            self.set_down(False)

        pos = self.pos * 100 // self.time_full
        if pos < 0:
            pos = 0
        if pos > 100:
            pos = 100

        if self.out != 0 and pos != self.prop_pos.value:
            self.prop_pos.value = pos;

    def handle_cmd(self, cmd):
        pass

    def handle_pos(self, pos):
        self.pos = pos * self.time_full // 100;

