from io import StringIO
from itertools import islice

import pandas as pd
from colassigner.meta_base import get_all_cols

from .namespace_metadata import PingFeatures, ping_table


def update_data(data_path: str, chunksize=1_000_000):

    with open(data_path, "r") as fp:
        while True:
            data = [*islice(fp, int(chunksize))]
            if not data:
                break
            sio = StringIO()
            sio.writelines(data)
            sio.seek(0)
            dump_raw(sio)


def dump_raw(raw_in):
    (
        pd.read_csv(
            raw_in,
            sep="\t",
            header=None,
        )
        .rename(columns={1: PingFeatures.device_id, 2: PingFeatures.loc.lat, 3: PingFeatures.loc.lon})
        .assign(
            **{
                PingFeatures.datetime: lambda df: pd.to_datetime(df.iloc[:, 4] * 10 ** 9),
                PingFeatures.dayofmonth: lambda df: df[PingFeatures.datetime].dt.day.astype(str).str.zfill(2),
                PingFeatures.year_month: lambda df: df.loc[:, 5].str[:7],
            }
        )
        .loc[:, get_all_cols(PingFeatures)]
    ).pipe(ping_table.extend)
