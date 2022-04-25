import datetime as dt
from io import StringIO
from itertools import islice
import os

import dask.dataframe as dd
import datazimmer as dz
import pandas as pd

NON_COVID_MONTH = "2019-11"
COVID_MONTH = "2020-11"


class Coordinates(dz.CompositeTypeBase):
    lon = float
    lat = float


class PingFeatures(dz.TableFeaturesBase):

    device_id = str
    datetime = dt.datetime
    year_month = str
    dayofmonth = str

    loc = Coordinates


ping_table = dz.ScruTable(
    PingFeatures,
    partitioning_cols=[PingFeatures.year_month, PingFeatures.dayofmonth],
    max_partition_size=2_000_000,
)


@dz.register_data_loader
def update_data(chunksize=1_000_000):

    data_path = os.environ["RAW_GPS_PING_LOC"]
    with open(data_path, "r") as fp:
        while True:
            data = [*islice(fp, int(chunksize))]
            if not data:
                break
            sio = StringIO()
            sio.writelines(data)
            sio.seek(0)
            dump_raw(sio)


@dz.register_env_creator
def create_environments(is_covid: bool = False, ind_of_weekday: int = None):
    """create environments that are described in the config of the repo"""

    month = COVID_MONTH if is_covid else NON_COVID_MONTH
    ddf = dd.read_parquet([p for p in ping_table.trepo.paths if month in p])
    weeks = ddf.loc[:, PingFeatures.datetime].dt.isocalendar().week
    week_filter = weeks == (weeks.min() + 1)
    day_filter = ddf.loc[:, PingFeatures.datetime].dt.dayofweek == ind_of_weekday
    full_filter = week_filter if ind_of_weekday is None else (week_filter & day_filter)
    filtered_ddf = ddf.loc[full_filter, :]
    ping_table.replace_all(filtered_ddf)


def dump_raw(raw_in):
    csv_cols = {
        1: PingFeatures.device_id,
        2: PingFeatures.loc.lat,
        3: PingFeatures.loc.lon,
    }
    ping_table.extend(
        pd.read_csv(raw_in, sep="\t", header=None)
        .rename(columns=csv_cols)
        .assign(
            **{
                PingFeatures.datetime: lambda df: pd.to_datetime(
                    df.iloc[:, 4] * 10 ** 9
                ),
                PingFeatures.dayofmonth: lambda df: df[PingFeatures.datetime]
                .dt.day.astype(str)
                .str.zfill(2),
                PingFeatures.year_month: lambda df: df.loc[:, 5].str[:7],
            }
        )
    )
