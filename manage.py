#!/usr/bin/env python
# encoding: utf-8

from app import create_app, db, models
from scrape.scrape import populate
from flask.ext.script import Manager, Shell, Server
from flask.ext.migrate import Migrate, MigrateCommand
import unittest

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """
    Make the shell context
    """
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='0.0.0.0'))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """
    Tests for app
    """
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def refresh():
    """
    Update the database with newdata
    """
    db.drop_all()
    db.create_all()
    populate()


if __name__ == '__main__':
    manager.run()
