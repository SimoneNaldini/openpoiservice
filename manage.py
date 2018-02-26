# manage.py


import unittest
from flask.cli import FlaskGroup
from openpoiservice.server import create_app, db
from openpoiservice.server.db_import import parser
from openpoiservice.server import ops_settings
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def test():
    """Runs the unit tests without test coverage."""

    tests = unittest.TestLoader().discover('openpoiservice/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def create_db():
    """Creates the db tables."""

    db.create_all()


@cli.command()
def drop_db():
    """Drops the db tables."""

    db.drop_all()


@cli.command()
def import_data():
    """Imports osm pbf data to postgis."""

    db.drop_all()

    db.create_all()

    logger.info("Starting to import data...")

    # add option to add multiple osm pbf files
    parser.run_import(os.path.join(os.getcwd() + '/osm', ops_settings['osm_file']))


if __name__ == '__main__':
    cli()
