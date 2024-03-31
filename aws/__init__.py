import boto3
from nrobo.util.common import Common


class AWS:

    @staticmethod
    def get_session() -> {boto3.session.Session, str}:
        """
        Creates AWS session.

        :return: a dictionary containing session object and aws credential
        """
        # Read AWS credential
        cred = Common.read_yaml('cred.yaml')
        aws = cred['aws']

        return {'session': boto3.session.Session(aws_access_key_id=aws['access_key'],
                                                 aws_secret_access_key=aws['secret_key'],
                                                 region_name='ap-southeast-2',
                                                 profile_name='default'),
                'aws': aws}

    @staticmethod
    def get_ec2_resource():
        """Get ec2 resource or service object"""

        return boto3.resource('ec2')

    @staticmethod
    def get_ec2_client():
        """
        Instantiates ec2 client

        :return: an ec2 Client object
        """
        return boto3.client('ec2')

    @staticmethod
    def create_ec2_instances(image_id: str = None,
                             instance_type: str = None,
                             key_name: str = None,
                             min_count: int = 0,
                             max_count: int = 0):
        """Create EC2 instance and starts it"""

        _session = AWS.get_session()
        aws = _session['aws']

        instances = AWS.get_ec2_resource().create_instances(
            ImageId=aws['image_id'] if image_id is None else image_id,
            MinCount=1 if min_count == 0 else min_count,
            MaxCount=1 if max_count == 0 else max_count,
            InstanceType=aws['instance_type'] if instance_type is None else instance_type,
            KeyName=aws['keypair'] if key_name is None else key_name
        )

        return instances

    @staticmethod
    def start_ec2_instance(instance_ids: [] = None,
                           additional_info: str = "No Additional Info",
                           dry_run: bool = False) -> dict:
        """
        Start given instances

        :param additional_info: reserved
        :param instance_ids: List of instance ids :param additional_info: additional info
        :param dry_run: Checks whether you have the required permissions for the action, without actually making the
                        request, and provides an error response. If you have the required permissions,
                        the error response is DryRunOperation. Otherwise, it is UnauthorizedOperation.
        :return:
        """

        _session = AWS.get_session()
        aws = _session['aws']

        response = AWS.get_ec2_client().start_instances(
            InstanceIds=[
                aws['instance_id'] if instance_ids is None else instance_ids,
            ],
            AdditionalInfo=additional_info,
            DryRun=dry_run
        )

        return response

    @staticmethod
    def stop_ec2_instances(instance_ids: [] = None,
                           hibernate: bool = False,
                           dry_run: bool = False,
                           force: bool = False) -> dict:
        """
        Stop given ec2 instances

        :param instance_ids: The IDs of the instances.
        :param hibernate: Hibernates the instance if the instance was enabled for hibernation at launch.
                          If the instance cannot hibernate successfully, a normal shutdown occurs.
        :param dry_run: Checks whether you have the required permissions for the action,
                        without actually making the request, and provides an error response.
                        If you have the required permissions, the error response is DryRunOperation.
                        Otherwise, it is UnauthorizedOperation.
        :param force: Forces the instances to stop. The instances do not have an opportunity
                      to flush file system caches or file system metadata.
                      If you use this option, you must perform file system check and repair procedures.
                      This option is not recommended for Windows instances.
        :return:
        """
        _session = AWS.get_session()
        aws = _session['aws']

        response = AWS.get_ec2_client().stop_instances(
            InstanceIds=[
                aws['instance_id'] if instance_ids is None else instance_ids,
            ],
            Hibernate=hibernate,
            DryRun=dry_run,
            Force=force
        )

        return response

    @staticmethod
    def describe_instances(filters: [] = None,
                           instance_ids: [] = None,
                           dry_run: bool = False,
                           max_results: int = 256,
                           next_token: str = ""):
        _session = AWS.get_session()
        aws = _session['aws']

        response = None

        if filters is not None:
            if next_token == "":
                response = AWS.get_ec2_client().describe_instances(
                    Filters=[] if filters is None else filters,
                    InstanceIds=[
                        aws['instance_id'] if instance_ids is None else instance_ids,
                    ],
                    DryRun=dry_run,
                    MaxResults=max_results
                )
            else:
                response = AWS.get_ec2_client().describe_instances(
                    Filters=[] if filters is None else filters,
                    InstanceIds=[
                        aws['instance_id'] if instance_ids is None else instance_ids,
                    ],
                    DryRun=dry_run,
                    MaxResults=max_results,
                    NextToken=next_token
                )
        else:
            response = AWS.get_ec2_client().describe_instances(
                InstanceIds=[
                    aws['instance_id'] if instance_ids is None else instance_ids,
                ],
                DryRun=dry_run
            )

        return response

    @staticmethod
    def describe_instance(instance_id: str = None, descriptions: {} = None) -> {}:

        _session = AWS.get_session()
        aws = _session['aws']

        _instance_id = aws['instance_id'] if instance_id is None else instance_id
        _descriptions = AWS.describe_instances() if descriptions is None else descriptions
        for reservation in _descriptions['Reservations']:
            for instance in reservation['Instances']:
                if instance['InstanceId'] == _instance_id:
                    return instance

        return {}

    @staticmethod
    def get_instance_attribute(attribute: str, instance_id: str = None, descriptions: {} = None):

        return AWS.describe_instance(instance_id=instance_id, descriptions=descriptions)[attribute]

    @staticmethod
    def wait_until_instance_state(instance_ids: str, instance_state: str = "running"):
        import time

        # Wait until status is running
        wait = 5
        max_iter = (60 / wait) * 15  # 15 min
        counter = 0
        while True:
            response = AWS.describe_instances(instance_ids=instance_ids)
            description = AWS.describe_instance(instance_id=instance_ids, descriptions=response)
            if description['State']['Name'] == instance_state:
                time.sleep(2)
                break

            # wait for 5 sec
            time.sleep(5)

            counter = counter + 1

            if counter > max_iter:
                raise Exception("TimeOut Error!")

    @staticmethod
    def get_ssm_client():
        """
        Instantiates SSM client

        :return: an SSM Client object
        """
        _session = AWS.get_session()
        return _session['session'].client(service_name='ssm', region_name=_session['aws']['region'])

    @staticmethod
    def execute_commands(commands: [] = None) -> str:
        """Runs given commands on remote linux instances

           using boto/boto3 Official AWS SSM Client python module.

           Reads AWS credentials from the cred.yaml file.

           Requirements:

                1. AWS Access Key ID
                2. AWS Secret Key ID
                3. Instance ID
                4. Instance Region

           param commands: a list of strings, each one a command to execute on the instances
           return: Command response as string

           """
        # Create session and get aws credential
        __session = AWS.get_session()
        aws_cred = __session['aws']

        # get SSM Client
        ssm = AWS.get_ssm_client()

        # Get instance ids
        instance_ids = [aws_cred['instance_id']]

        # Run given command list through SSM client and get response
        for attempt in range(30):
            try:
                response = ssm.send_command(
                    DocumentName="AWS-RunShellScript",  # One of AWS' preconfigured documents
                    Parameters={'commands': commands},
                    InstanceIds=instance_ids,
                )

                break

            except Exception as e:
                import time
                time.sleep(10)

        # Get command id from response
        command_id = response['Command']['CommandId']

        # Get command invocation output from SSM client
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_ids[0])

        # Wait and fetch output until command status is InProgress
        while output['Status'] == 'InProgress':
            output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_ids[0])

        # Return Command output as Standard Output Content
        return output['StandardOutputContent']
