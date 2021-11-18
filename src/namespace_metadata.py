import datetime as dt

from sscutils import CompositeTypeBase, ScruTable, TableFeaturesBase


class Coordinates(CompositeTypeBase):
    lon = float
    lat = float


class PingFeatures(TableFeaturesBase):

    device_id = str
    datetime = dt.datetime
    year_month = str
    dayofmonth = str

    loc = Coordinates


ping_table = ScruTable(
    PingFeatures, partitioning_cols=[PingFeatures.year_month, PingFeatures.dayofmonth], max_partition_size=2_000_000
)
