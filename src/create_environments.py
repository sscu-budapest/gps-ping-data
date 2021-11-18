import dask.dataframe as dd
from sscutils import dump_dfs_to_tables

from . import namespace_metadata as ns

NON_COVID_MONTH = "2019-11"
COVID_MONTH = "2020-11"


def create_environments(env_name, is_covid: bool = False, ind_of_weekday: int = None):
    """create environments that are described in the config of the repo"""

    month = COVID_MONTH if is_covid else NON_COVID_MONTH
    ddf = dd.read_parquet([p for p in ns.ping_table.trepo.paths if month in p])
    weeks = ddf.loc[:, ns.PingFeatures.datetime].dt.isocalendar().week
    week_filter = weeks == (weeks.min() + 1)
    full_filter = (
        week_filter
        if ind_of_weekday is None
        else (week_filter & (ddf.loc[:, ns.PingFeatures.datetime].dt.dayofweek == ind_of_weekday))
    )
    filtered_ddf = ddf.loc[full_filter, :]

    dump_dfs_to_tables(env_name, [(filtered_ddf, ns.ping_table)])
