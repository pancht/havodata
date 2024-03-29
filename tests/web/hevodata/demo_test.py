import time

import pytest
from nrobo.util.common import Common
from faker import Faker
from db import db_connector

from pages.hevo_data.public.public_landing import PagePublic


class TestDemo:
    """Demo test for Hevo Data"""

    # @pytest.mark.skip
    def test_demo(self, driver, logger):
        """Demo test for Hevo Data"""

        cred = Common.read_yaml('cred.yaml')
        hevo_cred = cred['havodata']
        ssh = cred['ssh']
        mysql_src = cred['mysql_src']
        mysql_dst = cred['mysql_dst']
        aws_cred = cred['aws']
        __database__ = 'database'

        copy_mysql_src = mysql_src.copy()
        copy_mysql_src.pop(__database__)
        print(copy_mysql_src)
        connect = db_connector(copy_mysql_src)
        db_cnx_src, db_cur_src = connect['connection'], connect['cursor']

        # Drop source db if exists
        stmt_drop_db = f"DROP DATABASE IF EXISTS {mysql_src[__database__]};"
        db_cur_src.execute(stmt_drop_db)

        # Drop destination db if exists
        stmt_drop_db = f"DROP DATABASE IF EXISTS {mysql_dst[__database__]};"
        db_cur_src.execute(stmt_drop_db)

        # create source db
        stmt_drop_db = f"CREATE DATABASE {mysql_src[__database__]};"
        db_cur_src.execute(stmt_drop_db)

        # create destination db
        stmt_drop_db = f"CREATE DATABASE {mysql_dst[__database__]};"
        db_cur_src.execute(stmt_drop_db)
        db_cnx_src.commit()

        db_cur_src.close()
        db_cnx_src.close()

        # Reconnect
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

        stmt_select = "SELECT count(name) FROM `panchdev_chauhan_automation_names`;"
        db_cur_dst.execute(stmt_select)

        assert db_cur_dst.fetchone()[0] == 2

        db_cur_dst.close()
        db_cnx_dst.close()
