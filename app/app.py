# -*- coding: utf-8 -*-
# pylint: disable=


import logging
import os
import random
import re
import time
from datetime import datetime

import names
import sqlalchemy
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from retry import retryas


@retry(Exception, delay=5, jitter=(1, 3))
def test():
    logger.info('Establishing connection to db...')
    db = create_engine(db_string)
    base = declarative_base()

    class People(base):
        __tablename__ = 'people'

        id = Column(Integer, primary_key=True)
        name = Column(String)

        def __str__(self):
            return self.name

    smaker = sessionmaker(db)
    session = smaker()

    base.metadata.create_all(db)

    # initialize data
    logger.info('Initializing data...')
    for _ in range(100):
        people = People(name=names.get_full_name())
        session.add(people)
        session.commit()

    # operations counter
    ops_count = {
        'create': 0,
        'read': 0,
        'update': 0,
        'delete': 0
    }

    logger.info('Generating random data...')
    while True:
        operations = ['create', 'read', 'update', 'delete']
        operation = operations[random.randint(0, 3)]

        if operation == 'create':
            people = People(name=names.get_full_name())
            session.add(people)
            session.commit()
            ops_count['create'] += 1

        if operation == 'read':
            people = session.query(People)
            ops_count['read'] += 1

        if operation == 'update':
            people = session.query(People)
            people[0].name = names.get_full_name()
            session.commit()
            ops_count['update'] += 1

        if operation == 'delete':
            people = session.query(People)
            session.delete(people[0])
            session.commit()
            ops_count['delete'] += 1

            logger.info('Executed %s operations.', str(ops_count))

        time.sleep(0.05)

if __name__ == "__main__":
    # change logging config
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s.%(msecs)03d][%(filename)s:%(lineno)d][%(levelname)s]%(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(__file__)

    # waiting db
    logger.info('Waiting for 5 seconds...')
    time.sleep(5)

    # get db settings from environment
    db_user = os.getenv('DB_USER', 'test')
    db_password = os.getenv('DB_PASSWORD', 'test')
    db_host = os.getenv('DB_HOST', 'db')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'test')
    db_string = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(
        db_user, db_password, db_host, db_port, db_name)


    test()
