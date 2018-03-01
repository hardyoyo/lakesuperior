import sys
sys.path.append('.')
import numpy
import random
import uuid

import pytest

from PIL import Image

from lakesuperior.app import create_app
from lakesuperior.config_parser import config
from lakesuperior.store.ldp_rs.lmdb_store import TxnManager
from util.generators import random_image
from util.bootstrap import bootstrap_binary_store


@pytest.fixture(scope='module')
def app():
    app = create_app(config['test'], config['logging'])

    yield app


@pytest.fixture(scope='module')
def db(app):
    '''
    Set up and tear down test triplestore.
    '''
    db = app.rdfly
    db.bootstrap()
    bootstrap_binary_store(app)

    yield db

    print('Tearing down fixture graph store.')
    if hasattr(db.store, 'destroy'):
        db.store.destroy(db.store.path)


@pytest.fixture
def rnd_img():
    '''
    Generate a square image with random color tiles.
    '''
    return random_image(8, 256)


