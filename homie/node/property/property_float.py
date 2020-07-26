import logging
from .property_base import Property_Base

logger = logging.getLogger(__name__)


class Property_Float(Property_Base):
    def __init__(
        self,
        node,
        id,
        name,
        settable=True,
        retained=True,
        qos=1,
        unit=None,
        data_type="float",
        data_format=None,
        value=None,
        set_value=None,
        tags=[],
        meta={},
        restore=False,
    ):
        super().__init__(
            node,
            id,
            name,
            settable,
            retained,
            qos,
            unit,
            "float",
            data_format,
            value,
            set_value,
            tags,
            meta,
            restore,
        )

        if data_format:
            _range = data_format.split(":")
            self.low_value = float(_range[0])
            self.high_value = float(_range[1])
        else:
            self.low_value = None
            self.high_value = None

    def validate_value(self, value):
        valid = True

        if self.low_value is not None and value < self.low_value:
            valid = False
        if self.high_value is not None and value > self.high_value:
            valid = False

        return valid

    def get_value_from_payload(self, payload):
        try:
            return float(payload)
        except:
            return None
