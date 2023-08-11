import click
import log
import dpos

DEFAULT_UNDELEGATE_FILE_LOCATION = 'data/undelegate.csv'

logger = log.get_logger_instance()

@click.group()
def cli():
    """Event indexer"""
    pass

@cli.command()
@click.argument('csv_file', required=False, default=DEFAULT_UNDELEGATE_FILE_LOCATION)
def index_undelegations(csv_file):
    """Index undelegate events to file"""
    dpos.index_events(csv_file)

if __name__ == '__main__':
    cli()