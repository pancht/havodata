import logging

from nrobo.util.common import Common
import mysql.connector
from faker import Faker
import sshtunnel
import pymysql
from sshtunnel import SSHTunnelForwarder

from pages.hevo_data.public.public_landing import PagePublic

cred = Common.read_yaml('cred.yaml')
hevo_cred = cred['havodata']
ssh = cred['ssh']
mysql_src = cred['mysql_src']
mysql_dst = cred['mysql_dst']


def db_connector(config):
    import mysql.connector
    from mysql.connector import errorcode

    try:
        _db_connection = mysql.connector.connect(**config)
        db_cursor = _db_connection.cursor()

        # _db_connection_dest = mysql.connector.connect(**mysql_dst)
        # db_cursor_dest = _db_connection_dest.cursor()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    print("connection established")

    return {'connection': _db_connection, 'cursor': db_cursor}


class TestDemo:
    """Demo test for Hevo Data"""

    def test_demo(self, driver, logger):
        """Demo test for Hevo Data"""

        connect = db_connector(mysql_src)
        db_cnx_src, db_cur_src = connect['connection'], connect['cursor']

        # Drop table if exists, and create it new
        stmt_drop = "DROP TABLE IF EXISTS `automation`.`names`"
        db_cur_src.execute(stmt_drop)

        #################################
        # create names table            #
        # insert a row in names table   #
        #################################
        stmt_create = "CREATE TABLE `automation`.`names` " \
                      "(`id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT, `name` VARCHAR(30) NOT NULL " \
                      ", `last_modified` TIMESTAMP on update CURRENT_TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP , " \
                      "PRIMARY KEY (`id`)) ENGINE = InnoDB; "
        db_cur_src.execute(stmt_create)

        faker = Faker()
        # Insert 2 records
        names = ([faker.name()], [faker.name()])
        stmt_insert = "INSERT INTO names (name) VALUES (%s)"
        db_cur_src.executemany(stmt_insert, names)
        db_cnx_src.commit()

        db_cur_src.close()
        db_cnx_src.close()

        page_landing = PagePublic(driver=driver, logger=logger)
        page_login_email = page_landing.go_to_login_page()

        page_login_email.type_registered_email(hevo_cred['email'])
        page_login_pass = page_login_email.click_button_continue()

        page_login_pass.type_password(hevo_cred['password'])
        page_dashboard = page_login_pass.click_button_login()

        page_select_source_type = page_dashboard.click_button_create_pipeline()
        page_config_source = page_select_source_type.select_source_type_mysql()

        page_select_objects_step_one = \
            page_config_source.config_source_type_save_test_continue(config=mysql_src, ssh=ssh)

        page_select_dest_step_one = page_select_objects_step_one.click_button_continue()

        # page_select_dest_step_one = page_select_objects_step_two.click_button_continue()
        page_config_dest = page_select_dest_step_one.click_button_mysql()
        page_select_dest_step_two = page_config_dest.config_dest_type_save_test_continue(mysql_dst, ssh)

        page_select_dest_step_two.type_destination_tbl_prefix('panchdev_chauhan')
        page_select_dest_step_two.select_scheduled_12_hours()
        page_pipeline_overview = page_select_dest_step_two.click_continue()

        page_pipeline_overview.click_button_run_now_pipeline_header()

        # run pipeline manually

        # verify destination db table
        connect = db_connector(mysql_dst)
        db_cnx_dst, db_cur_dst = connect['connection'], connect['cursor']

        stmt_select = "SELECT count(name) as ROW FROM `panchdev_chauhan_automation_names`;"
        db_cur_dst.execute(stmt_select)

        assert db_cur_dst.fetchone()[0] == 2

        db_cur_dst.close()
        db_cnx_dst.close()
