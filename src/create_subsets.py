import dask.dataframe as dd
from sscutils import dump_dfs_to_trepos

from .raw_cols import PingCols
from .trepos import pings_table

NON_COVID_MONTH = "2019-11"
COVID_MONTH = "2020-11"


def create_subsets(subset_name, is_covid: bool = False, ind_of_weekday: int = None):
    if subset_name == "complete":
        return

    month = COVID_MONTH if is_covid else NON_COVID_MONTH
    ddf = dd.read_parquet([p for p in pings_table.paths if month in p])
    weeks = ddf.loc[:, PingCols.datetime].dt.isocalendar().week
    week_filter = weeks == (weeks.min() + 1)
    full_filter = (
        week_filter
        if ind_of_weekday is None
        else (week_filter & (ddf.loc[:, PingCols.datetime].dt.dayofweek == ind_of_weekday))
    )
    filtered_ddf = ddf.loc[full_filter, :]

    dump_dfs_to_trepos(subset_name, [(filtered_ddf, pings_table)])
