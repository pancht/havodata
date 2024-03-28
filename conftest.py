"""
=====================CAUTION=======================
DO NOT DELETE THIS FILE SINCE IT IS PART OF NROBO
FRAMEWORK AND IT MAY CHANGE IN THE FUTURE UPGRADES
OF NROBO FRAMEWORK. THUS, TO BE ABLE TO SAFELY UPGRADE
TO LATEST NROBO VERSION, PLEASE DO NOT DELETE THIS
FILE OR ALTER ITS LOCATION OR ALTER ITS CONTENT!!!
===================================================


@author: Panchdev Singh Chauhan
@email: erpanchdev@gmail.com
"""
import pytest
from nrobo.conftest import *

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), ''))


@pytest.fixture(scope='session', autouse=True)
def aws():
    from aws import AWS
    yield AWS()


@pytest.fixture(scope='session', autouse=True)
def db_connector():
    pass
    # import mysql.connector
    # from mysql.connector import errorcode
    #
    # try:
    #     cred = Common.read_yaml('cred.yaml')
    #     mysql_src = cred['mysql_src']
    #     mysql_dst = cred['mysql_dst']
    #
    #     _db_connection_src = mysql.connector.connect(**mysql_src)
    #     db_cursor_src = _db_connection_src.cursor()
    #
    #     _db_connection_dest = mysql.connector.connect(**mysql_dst)
    #     db_cursor_dest = _db_connection_dest.cursor()
    #
    # except mysql.connector.Error as err:
    #     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    #         print("Something is wrong with your user name or password")
    #     elif err.errno == errorcode.ER_BAD_DB_ERROR:
    #         print("Database does not exist")
    #     else:
    #         print(err)
    #
    # print("connection established")
    #
    # yield {'src': {'connection': _db_connection_src, 'cursor': db_cursor_src},
    #        'dst': {'connection': _db_connection_dest, 'cursor': db_cursor_dest}}
    #
    # # close db cursors
    # db_cursor_src.close()
    # db_cursor_dest.close()
    #
    # # close db connection
    # _db_connection_src.close()
    # _db_connection_dest.close()
