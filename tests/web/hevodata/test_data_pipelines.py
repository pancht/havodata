import boto3
import time

import pytest
from nrobo.util.common import Common
from faker import Faker
from db import db_connector

from pages.hevo_data.public.public_landing import PagePublic


class TestHevoDataPipelines:
    """Tests for validating HevoData Pipelines"""

    # @pytest.mark.skip
    def test_mysql_to_mysql_data_pipeline(self, driver, logger, setup_aws_instance):
        """Validate that MySql to MySql Data Pipeline is working as expected.

           Data:



                Source: MySql Database
                Destination: MySql Database
                ....

                """

        cred = setup_aws_instance['cred']
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
        page_login_email = page_landing.go_to_login_page(hevo_cred['url'])

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

    @pytest.mark.skip
    def test_iam_mamagement_console(self):
        aws_management_console = boto3.session.Session(profile_name="default")
        iam_console = aws_management_console.resource('iam')

        for each_user in iam_console.users.all():
            print(each_user.name)

    @pytest.mark.skip
    def test_iam_mamagement_console(self):
        aws_management_console = boto3.session.Session(profile_name="default")
        print(dir(aws_management_console))
        print(aws_management_console.available_profiles)
        print(aws_management_console.get_available_regions('ec2'))
        print(aws_management_console.get_available_regions('ssm'))

        print(aws_management_console.get_available_resources())
        """
        ['cloudformation', 'cloudwatch', 'dynamodb', 'ec2', 'glacier', 'iam', 'opsworks', 's3', 'sns', 'sqs']
        """

        print(aws_management_console.get_available_services())
        """
        ['accessanalyzer', 'account', 'acm', 'acm-pca', 'alexaforbusiness', 'amp', 'amplify', 'amplifybackend', 'amplifyuibuilder', 'apigateway', 'apigatewaymanagementapi', 'apigatewayv2', 'appconfig', 'appconfigdata', 'appfabric', 'appflow', 'appintegrations', 'application-autoscaling', 'application-insights', 'applicationcostprofiler', 'appmesh', 'apprunner', 'appstream', 'appsync', 'arc-zonal-shift', 'artifact', 'athena', 'auditmanager', 'autoscaling', 'autoscaling-plans', 'b2bi', 'backup', 'backup-gateway', 'backupstorage', 'batch', 'bcm-data-exports', 'bedrock', 'bedrock-agent', 'bedrock-agent-runtime', 'bedrock-runtime', 'billingconductor', 'braket', 'budgets', 'ce', 'chatbot', 'chime', 'chime-sdk-identity', 'chime-sdk-media-pipelines', 'chime-sdk-meetings', 'chime-sdk-messaging', 'chime-sdk-voice', 'cleanrooms', 'cleanroomsml', 'cloud9', 'cloudcontrol', 'clouddirectory', 'cloudformation', 'cloudfront', 'cloudfront-keyvaluestore', 'cloudhsm', 'cloudhsmv2', 'cloudsearch', 'cloudsearchdomain', 'cloudtrail', 'cloudtrail-data', 'cloudwatch', 'codeartifact', 'codebuild', 'codecatalyst', 'codecommit', 'codedeploy', 'codeguru-reviewer', 'codeguru-security', 'codeguruprofiler', 'codepipeline', 'codestar', 'codestar-connections', 'codestar-notifications', 'cognito-identity', 'cognito-idp', 'cognito-sync', 'comprehend', 'comprehendmedical', 'compute-optimizer', 'config', 'connect', 'connect-contact-lens', 'connectcampaigns', 'connectcases', 'connectparticipant', 'controltower', 'cost-optimization-hub', 'cur', 'customer-profiles', 'databrew', 'dataexchange', 'datapipeline', 'datasync', 'datazone', 'dax', 'detective', 'devicefarm', 'devops-guru', 'directconnect', 'discovery', 'dlm', 'dms', 'docdb', 'docdb-elastic', 'drs', 'ds', 'dynamodb', 'dynamodbstreams', 'ebs', 'ec2', 'ec2-instance-connect', 'ecr', 'ecr-public', 'ecs', 'efs', 'eks', 'eks-auth', 'elastic-inference', 'elasticache', 'elasticbeanstalk', 'elastictranscoder', 'elb', 'elbv2', 'emr', 'emr-containers', 'emr-serverless', 'entityresolution', 'es', 'events', 'evidently', 'finspace', 'finspace-data', 'firehose', 'fis', 'fms', 'forecast', 'forecastquery', 'frauddetector', 'freetier', 'fsx', 'gamelift', 'glacier', 'globalaccelerator', 'glue', 'grafana', 'greengrass', 'greengrassv2', 'groundstation', 'guardduty', 'health', 'healthlake', 'honeycode', 'iam', 'identitystore', 'imagebuilder', 'importexport', 'inspector', 'inspector-scan', 'inspector2', 'internetmonitor', 'iot', 'iot-data', 'iot-jobs-data', 'iot1click-devices', 'iot1click-projects', 'iotanalytics', 'iotdeviceadvisor', 'iotevents', 'iotevents-data', 'iotfleethub', 'iotfleetwise', 'iotsecuretunneling', 'iotsitewise', 'iotthingsgraph', 'iottwinmaker', 'iotwireless', 'ivs', 'ivs-realtime', 'ivschat', 'kafka', 'kafkaconnect', 'kendra', 'kendra-ranking', 'keyspaces', 'kinesis', 'kinesis-video-archived-media', 'kinesis-video-media', 'kinesis-video-signaling', 'kinesis-video-webrtc-storage', 'kinesisanalytics', 'kinesisanalyticsv2', 'kinesisvideo', 'kms', 'lakeformation', 'lambda', 'launch-wizard', 'lex-models', 'lex-runtime', 'lexv2-models', 'lexv2-runtime', 'license-manager', 'license-manager-linux-subscriptions', 'license-manager-user-subscriptions', 'lightsail', 'location', 'logs', 'lookoutequipment', 'lookoutmetrics', 'lookoutvision', 'm2', 'machinelearning', 'macie2', 'managedblockchain', 'managedblockchain-query', 'marketplace-agreement', 'marketplace-catalog', 'marketplace-deployment', 'marketplace-entitlement', 'marketplacecommerceanalytics', 'mediaconnect', 'mediaconvert', 'medialive', 'mediapackage', 'mediapackage-vod', 'mediapackagev2', 'mediastore', 'mediastore-data', 'mediatailor', 'medical-imaging', 'memorydb', 'meteringmarketplace', 'mgh', 'mgn', 'migration-hub-refactor-spaces', 'migrationhub-config', 'migrationhuborchestrator', 'migrationhubstrategy', 'mobile', 'mq', 'mturk', 'mwaa', 'neptune', 'neptune-graph', 'neptunedata', 'network-firewall', 'networkmanager', 'networkmonitor', 'nimble', 'oam', 'omics', 'opensearch', 'opensearchserverless', 'opsworks', 'opsworkscm', 'organizations', 'osis', 'outposts', 'panorama', 'payment-cryptography', 'payment-cryptography-data', 'pca-connector-ad', 'personalize', 'personalize-events', 'personalize-runtime', 'pi', 'pinpoint', 'pinpoint-email', 'pinpoint-sms-voice', 'pinpoint-sms-voice-v2', 'pipes', 'polly', 'pricing', 'privatenetworks', 'proton', 'qbusiness', 'qconnect', 'qldb', 'qldb-session', 'quicksight', 'ram', 'rbin', 'rds', 'rds-data', 'redshift', 'redshift-data', 'redshift-serverless', 'rekognition', 'repostspace', 'resiliencehub', 'resource-explorer-2', 'resource-groups', 'resourcegroupstaggingapi', 'robomaker', 'rolesanywhere', 'route53', 'route53-recovery-cluster', 'route53-recovery-control-config', 'route53-recovery-readiness', 'route53domains', 'route53resolver', 'rum', 's3', 's3control', 's3outposts', 'sagemaker', 'sagemaker-a2i-runtime', 'sagemaker-edge', 'sagemaker-featurestore-runtime', 'sagemaker-geospatial', 'sagemaker-metrics', 'sagemaker-runtime', 'savingsplans', 'scheduler', 'schemas', 'sdb', 'secretsmanager', 'securityhub', 'securitylake', 'serverlessrepo', 'service-quotas', 'servicecatalog', 'servicecatalog-appregistry', 'servicediscovery', 'ses', 'sesv2', 'shield', 'signer', 'simspaceweaver', 'sms', 'sms-voice', 'snow-device-management', 'snowball', 'sns', 'sqs', 'ssm', 'ssm-contacts', 'ssm-incidents', 'ssm-sap', 'sso', 'sso-admin', 'sso-oidc', 'stepfunctions', 'storagegateway', 'sts', 'supplychain', 'support', 'support-app', 'swf', 'synthetics', 'textract', 'timestream-influxdb', 'timestream-query', 'timestream-write', 'tnb', 'transcribe', 'transfer', 'translate', 'trustedadvisor', 'verifiedpermissions', 'voice-id', 'vpc-lattice', 'waf', 'waf-regional', 'wafv2', 'wellarchitected', 'wisdom', 'workdocs', 'worklink', 'workmail', 'workmailmessageflow', 'workspaces', 'workspaces-thin-client', 'workspaces-web', 'xray']
        """

        iam_console_client = aws_management_console.client('iam')
        print(dir(iam_console_client))
        print(iam_console_client.list_users())
        for each_user in iam_console_client.list_users()['Users']:
            print(each_user['UserName'])

    @pytest.mark.skip
    def test_write_boto3_script(self):
        # imports
        # aws management console
        # open client with which you want to work
        # your boto3 script
        aws_management_console = boto3.session.Session(profile_name="default")
        iam_console = aws_management_console.resource('iam')

        for each_user in iam_console.users.all():
            print(each_user.name)

    @pytest.mark.skip
    def test_run_script(self):
        # imports
        # aws management console
        # open client with which you want to work
        # your boto3 script
        # aws_management_console = boto3.session.Session(profile_name="default", region_name='ap-southeast-2')
        from aws import AWS
        response = AWS.execute_commands(commands=[
            "sudo docker --version"])  # aws_management_console.client(service_name='ssm', region_name='ap-southeast-2')

        # response = ssm_console.send_command(
        #             DocumentName="AWS-RunShellScript",  # One of AWS' preconfigured documents
        #             Parameters={'commands': ["sudo docker --version"]},
        #             InstanceIds=['i-03d6c038d09c09288'],
        #         )

        print(response)


