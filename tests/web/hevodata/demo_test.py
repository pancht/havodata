import logging

from nrobo.util.common import Common
import mysql.connector
from faker import Faker
import sshtunnel
import pymysql
from sshtunnel import SSHTunnelForwarder

from pages.hevo_data.public.public_landing import PagePublic

hevo_cred = Common.read_yaml('cred.yaml')['havodata']


class TestDemo:
    """Demo test for Hevo Data"""

    def test_demo(self, driver, logger, db_connector):
        """Demo test for Hevo Data"""

        db_cnx_src = db_connector['src']['connection']
        db_cur_src = db_connector['src']['cursor']

        db_cnx_dst = db_connector['dst']['connection']
        db_cur_dst = db_connector['dst']['cursor']

        print(f"{db_cnx_src} <> {db_cur_src}\n"
              f"{db_cnx_dst} <> {db_cur_dst}")

        page_landing = PagePublic(driver=driver, logger=logger)
        page_login_email = page_landing.go_to_login_page()

        page_login_email.type_registered_email(hevo_cred['email'])
        page_login_pass = page_login_email.click_button_continue()

        page_login_pass.type_password(hevo_cred['password'])
        page_dashboard = page_login_pass.click_button_login()

        page_select_source_type = page_dashboard.click_button_create_pipeline()
        page_config_source = page_select_source_type.select_source_type_mysql()


        # drop all tables

        # create names table

        # insert a row in names table

        # run pipeline manually

        # verify destination db table

        # update existing row

        # run pipeline manually

        # verify destination db table

        # insert a row in names table

        # run pipeline manually

        # verify destination db table

        # mydb = mysql.connector.connect(
        #     host=f"{mysql_source['host']}",
        #     user=f"{mysql_source['username']}",
        #     password=f"{mysql_source['password']}",
        #     database=f"{mysql_source['database']}"
        # )
        #
        # print(mydb)
        # exit()
        # table = mysql_source['table']
        #
        # mycursor = mydb.cursor()
        #
        # sql = f"INSERT INTO {table} (name) VALUES (%s)"
        #
        # fake = Faker()
        # name = fake.name()
        #
        # val = f"{name}"
        # mycursor.execute(sql, val)
        #
        # mydb.commit()
        #
        # print(mycursor.rowcount, "record inserted.")
