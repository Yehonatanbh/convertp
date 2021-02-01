import pytest
from tempfile import tempdir
import os
from shutil import rmtree

TEMP_DIR = os.path.join(tempdir, 'convertp_tests')


@pytest.fixture()
def work_dir():
    if os.path.exists(TEMP_DIR):
        rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)

    yield TEMP_DIR

    if os.path.exists(TEMP_DIR):
        rmtree(TEMP_DIR)
