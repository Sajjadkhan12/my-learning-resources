"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import s3,ec2

# Create an AWS resource (S3 Bucket)
bucket = s3.Bucket('my-bucket')

# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

sg = ec2.SecurityGroup('web-server-sg',description="Security group for web server")

allow_ssh = ec2.SecurityGroupRule("AllowSSH",type="ingress",from_port=22,to_port=22,
                                  protocol="tcp",cidr_blocks=["0.0.0.0/0"],security_group_id=sg.id)

allow_http = ec2.SecurityGroupRule("AllowHTTP",type="ingress",from_port=80,to_port=80,
                                  protocol="tcp",cidr_blocks=["0.0.0.0/0"],security_group_id=sg.id)
allow_all = ec2.SecurityGroupRule("AllowALL",type="ingress",from_port=0,to_port=0,
                                  protocol="-1",cidr_blocks=["0.0.0.0/0"],security_group_id=sg.id)


ec2_instance = ec2.Instance('web-server',
                            ami="ami-053b0d53c279acc90",
                            instance_type="t3.nano",
                            key_name="linux_key",
                            tags = {
                                "Name": "web"
                            },
                            vpc_security_group_ids = [sg.id]
                            )
pulumi.export('public_ip', ec2_instance.public_ip)
