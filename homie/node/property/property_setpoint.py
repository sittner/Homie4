from .property_float import Property_Float


class Property_Setpoint(Property_Float):
    def __init__(
        self,
        node,
        id=None,
        name=None,
        settable=True,
        retained=True,
        qos=1,
        unit=None,
        data_type=None,
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
            data_type,
            data_format,
            value,
            set_value,
            tags,
            meta,
            restore,
        )

