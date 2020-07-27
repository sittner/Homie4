from .node_base import Node_Base

from homie.node.property.property_switch import Property_Switch
from homie.device_base import Device_Base

class Node_Switch(Node_Base):
    def __init__(
        self,
        device,
        id="switch",
        name="Switch",
        type_="switch",
        retain=True,
        qos=1,
        set_switch=None,
        max_on_time = 0,
    ):
        super().__init__(device, id, name, type_, retain, qos)

        assert set_switch  # must provide a function to set the value of the switch

        self.property = Property_Switch(self, set_value=self.handle_switch, restore=True)
        self.add_property(self.property)

        self.set_switch = set_switch
        self.max_on_time = max_on_time
        self.on_timer = 0

    def update_switch(self, state):
        self.property.value = "ON" if state else "OFF"

    def handle_switch(self, onoff):
        pass

    def periodic(self, now, dt):
        if self.property.value == "ON" and self.max_on_time > 0:
            self.on_timer += dt

        if self.on_timer > self.max_on_time:
            self.update_switch(False)

        if self.property.value == "ON":
            self.set_switch(True)
        else:
            self.set_switch(False)
            self.on_timer = 0

