from pathlib import Path
import sys


from colassigner import allcols
from src.raw_cols import PingCols
from src.trepos import pings_table
from tqdm import tqdm

import pandas as pd


def dump_path(raw_path, size=2_500_000):
    pbar = tqdm()
    rs = []
    with raw_path.open() as fp:
        for i, line in enumerate(fp):
            rs.append(line.strip().split("\t"))
            if ((i + 1) % size) == 0:
                pd.DataFrame(
                    rs,
                    columns=[
                        "country",
                        PingCols.devide_id,
                        "lat",
                        "lon",
                        "ts",
                        "date",
                        "time",
                    ],
                ).assign(
                    **{
                        PingCols.datetime: lambda df: pd.to_datetime(
                            df["date"] + " " + df["time"]
                        ),
                        PingCols.Location.lon: lambda df: df["lon"].astype(float),
                        PingCols.Location.lat: lambda df: df["lat"].astype(float),
                        PingCols.month: lambda df: df[PingCols.datetime]
                        .dt.date.astype(str)
                        .str[:7],
                        PingCols.dayofmonth: lambda df: df[PingCols.datetime].dt.day,
                    }
                ).loc[
                    :, allcols(PingCols)
                ].pipe(
                    pings_table.extend
                )
                rs = []
                pbar.update()


if __name__ == "__main__":
    rpath = Path(sys.argv[1])
    print(rpath)
    dump_path(rpath)
