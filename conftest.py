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
import os
import sys
from nrobo.conftest import *

sys.path.append(os.path.join(os.path.dirname(__file__), ''))


@pytest.fixture(scope='package', autouse=True)
def aws():
    from aws import AWS
    yield AWS()


def update_host_ip_in_cred_yaml(prev_public_ip: str, cred: {}, instance_id: str = None):
    from aws import AWS
    import time

    for attempt in range(10):
        print(f"Update IP => {attempt}")

        # Get public ip of instance
        instance_info = AWS.describe_instance(instance_id)
        instance_public_ip = instance_info['PublicIpAddress']

        if not len(instance_public_ip) == 0 and not instance_public_ip == prev_public_ip:
            print(f"public ip=> {instance_public_ip}")
            # update instance public ip in cred.yaml
            cred['mysql_src']['host'] = cred['mysql_dst']['host'] = instance_public_ip
            Common.write_yaml('cred.yaml', cred)
            time.sleep(2)

            break

        time.sleep(2)


@pytest.fixture(scope='package', autouse=True)
def setup_aws_instance() -> None:
    """
    Prepare dockerized MySql instance prior to test run.
    And remove dockerized MySql instance after testrun completes.
    """
    # Read AWS credential
    cred = Common.read_yaml('cred.yaml')
    aws = cred['aws']
    prev_public_ip = cred['mysql_src']['host']

    from aws import AWS
    import time

    if AWS.get_instance_attribute('State')['Name'] == 'running':
        AWS.stop_ec2_instances()
        AWS.wait_until_instance_state(aws['instance_id'], instance_state='stopped')

    # Start instance
    AWS.start_ec2_instance()
    time.sleep(2)  # 2 secs
    # Wait until running
    AWS.wait_until_instance_state(aws['instance_id'])

    # wait few more seconds
    update_host_ip_in_cred_yaml(prev_public_ip=prev_public_ip, cred=cred)

    # Check if docker is already installed
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

    yield {'cred': cred}

    commands = [
        f'sudo docker rm --force {container_name}'
    ]
    response = AWS.execute_commands(commands=commands)
    print(response)

    # Stop ec2 instance
    AWS.stop_ec2_instances()
    # Wait until stopped
    AWS.wait_until_instance_state(aws['instance_id'], instance_state='stopped')
    # wait few more seconds
    time.sleep(2)
