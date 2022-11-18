import datazimmer as dz
import pandas as pd

from ..meta import ExtendedPing
from .raw_proc import ping_table

NON_COVID_MONTH = "2019-11"
COVID_MONTH = "2020-11"


@dz.register_env_creator
def create_environments(is_covid: bool = False, ind_of_weekday: int = None):
    month = COVID_MONTH if is_covid else NON_COVID_MONTH
    for gid, paths in ping_table.get_partition_paths(ExtendedPing.year_month):
        if gid == month:
            df = pd.concat(map(ping_table.trepo.read_df_from_path, paths))
    weeks = df.loc[:, ExtendedPing.datetime].dt.isocalendar().week
    week_filter = weeks == (weeks.min() + 1)
    day_filter = df.loc[:, ExtendedPing.datetime].dt.dayofweek == ind_of_weekday
    full_filter = week_filter if ind_of_weekday is None else (week_filter & day_filter)
    ping_table.replace_all(df.loc[full_filter, :])
