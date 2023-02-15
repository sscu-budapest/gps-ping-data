import datetime as dt

import datazimmer as dz
import pandas as pd
import psutil

from .meta import ExtendedPing
from .ubermedia.raw_proc import ping_table


class DateAggregation(dz.AbstractEntity):
    datatime = dz.Index & dt.datetime
    count = int
    nunique = int


def dategroup(_df):
    return (
        _df.assign(
            **{DateAggregation.datatime: _df[ExtendedPing.datetime].dt.floor("D")}
        )
        .groupby(DateAggregation.datatime)[ExtendedPing.device_id]
        .agg(["nunique", "count"])
    )


date_agg_table = dz.ScruTable(DateAggregation)


@dz.register(dependencies=[ping_table])
def step():
    date_agg_table.replace_all(
        pd.concat(
            ping_table.map_partitions(
                fun=dategroup, workers=psutil.virtual_memory().total // (5 * 10**9)
            )
        )
        .groupby(level=0)
        .sum()
    )
