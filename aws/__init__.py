import boto3
import boto3.session as session
from nrobo.util.common import Common


class AWS:

    @staticmethod
    def get_session():
        """
        Creates AWS session.

        :return: a dictionary containing session object and aws credential
        """
        # Read AWS credential
        cred = Common.read_yaml('cred.yaml')
        aws = cred['aws']

        return {'session': session.Session(aws_access_key_id=aws['access_key'],
                                           aws_secret_access_key=aws['secret_key'],
                                           region_name='ap-southeast-2'),
                'aws': aws}

    @staticmethod
    def get_ec2_resource():
        """Get ec2 resource or service object"""

        return boto3.resource('ec2')

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
    def get_ssm_client():
        """
        Instantiates SSM client

        :return: an SSM Client object
        """
        return boto3.client('ssm')

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
        response = ssm.send_command(
            DocumentName="AWS-RunShellScript",  # One of AWS' preconfigured documents
            Parameters={'commands': commands},
            InstanceIds=instance_ids,
        )

        # Get command id from response
        command_id = response['Command']['CommandId']

        # Get command invocation output from SSM client
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_ids[0])

        # Wait and fetch output until command status is InProgress
        while output['Status'] == 'InProgress':
            output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instance_ids[0])

        # Return Command output as Standard Output Content
        return output['StandardOutputContent']
