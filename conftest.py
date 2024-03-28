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


@pytest.fixture(scope='package', autouse=True)
def aws():
    from aws import AWS
    yield AWS()


@pytest.fixture(scope='package', autouse=True)
def setup_aws_instance() -> None:
    """
    Prepare dockerized MySql instance prior to test run.
    And remove dockerized MySql instance after testrun completes.
    """
    # Read AWS credential
    cred = Common.read_yaml('cred.yaml')
    aws = cred['aws']

    from aws import AWS

    response = AWS.execute_commands(commands=["sudo docker --version"])

    container_name = f"{aws['container_name_mysql']}"

    commands = [
        'sudo yum update -y'
    ]

    if len(response):
        # Docker is already installed, just start it
        # https://medium.com/@srijaanaparthy/step-by-step-guide-to-install-docker-on-amazon-linux-machine-in-aws-a690bf44b5fe
        commands.extend(
            [
                'sudo systemctl start docker',
                f'sudo docker rm --force {container_name}',
                'sudo docker --version'
            ]
        )
    else:
        # docker is not installed
        commands.extend(
            [
                'sudo yum install docker -y',
                'sudo systemctl start docker',
                'sudo docker --version'
            ]
        )

    commands.extend(
        [
            f'sudo docker run -p 33061:3306 --name {container_name} '
            f'-e MYSQL_ROOT_PASSWORD={aws["container_password"]} -d mysql:latest',
        ]
    )

    response = AWS.execute_commands(commands=commands)
    print(response)

    yield

    commands = [
        f'sudo docker rm --force {container_name}'
    ]
    response = AWS.execute_commands(commands=commands)
    print(response)

