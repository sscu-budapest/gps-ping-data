from invoke import task
from sscutils import dataset_ns as ns

@task
def update_data(ctx):
    pass

ns.add_task(update_data)
