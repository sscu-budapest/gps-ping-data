import gzip
import os

import datazimmer as dz
import pandas as pd

from ..meta import ExtendedPing, GpsPing, PingPartitioner

ping_table = dz.ScruTable(
    ExtendedPing,
    partitioning_cols=[ExtendedPing.year_month, ExtendedPing.device_group],
)

csv_cols = {1: GpsPing.device_id, 2: GpsPing.loc.lat, 3: GpsPing.loc.lon}


@dz.register_data_loader
def create_data(chunksize_mil):

    data_path = gzip.open(os.environ["RAW_UM_GPS_PING_LOC"])
    chsz = chunksize_mil * 10**6
    iterable = pd.read_csv(data_path, sep="\t", header=None, chunksize=chsz)
    for df in iterable:
        dump_raw(df)
    data_path.close()


def dump_raw(df: pd.DataFrame):
    ping_table.extend(
        df.rename(columns=csv_cols)
        .assign(
            **{GpsPing.datetime: lambda df: pd.to_datetime(df.iloc[:, 4] * 10**9)}
        )
        .pipe(PingPartitioner())
    )
