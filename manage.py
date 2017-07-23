"""
The Manager class keeps track of all the commands and handles how they are called from the command line
The MigrateCommand contains a set of migration commands
The manager also adds the migration commands and enforces that they start with db
"""
import os
from flask_script import Manager  # manager class handles migration commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app, models

app = create_app(configuration=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
