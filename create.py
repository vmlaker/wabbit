"""Create MySQL database and user."""

import sys
import sqlalchemy as sa
import coils
import mapping

# Load configuration file.
CONFIG = sys.argv[1] if len(sys.argv)>=2 else 'wabbit.cfg'
config = coils.Config(CONFIG)

# Connect to database engine.
root_u = coils.user_input('Admin username', default=config['admin'])
root_p = coils.user_input('Admin password', password=True)
engine = sa.create_engine('mysql://{}:{}@{}'.format(root_u, root_p, config['host']))
try:
    conn = engine.connect()
except sa.exc.OperationalError:
    print('Failed to connect.')
    sys.exit(1)

# Create the database and user.
try:
    conn.execute('CREATE DATABASE {}'.format(config['db_name']))
except sa.exc.ProgrammingError: 
    print('Failed to create database.')
try:
    conn.execute('CREATE USER "{}"@"{}" IDENTIFIED BY "{}"'.format(
            config['username'], config['host'], config['password']))
    conn.execute('GRANT ALL ON `{}`.* TO "{}"@"{}"'.format(
            config['db_name'], config['username'], config['host']))
except sa.exc.OperationalError:
    print('Failed to create user.')
    sys.exit(1)

# Disconnect from database engine.
conn.close()

# Create the tables.
# First create another engine, this time giving it database name.
engine2 = sa.create_engine(
    'mysql://{}:{}@{}/{}'.format(
        config['username'], config['password'],
        config['host'], config['db_name'],
        )
    )

# Create tables if they don't exist.
mapping.Base.metadata.create_all(engine2)

# Create the "size" field in "info" table, this time using ORM.
Session = sa.orm.sessionmaker(bind=engine2)
session = Session()
datum = mapping.Datum('size', 0)
session.add(datum)
session.commit()
