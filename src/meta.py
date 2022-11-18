import datetime as dt

import datazimmer as dz
from colassigner import Col


class Coordinates(dz.CompositeTypeBase):
    lon = float
    lat = float


class GpsPing(dz.AbstractEntity):

    device_id = str
    datetime = dt.datetime
    loc = Coordinates


class PingPartitioner(dz.AbstractEntity):
    def device_group(self, df) -> Col[str]:
        return df[GpsPing.device_id].str[:2]

    def year_month(self, df) -> Col[str]:
        return df[GpsPing.datetime].astype(str).str[:7]


class ExtendedPing(GpsPing, PingPartitioner):
    pass
