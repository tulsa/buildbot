import os
from fabric.api import *

# Get ssh commands working with this:
# http://stackoverflow.com/questions/5327465/using-an-ssh-keyfile-with-fabric

AWS_AMI = {
    "Ubuntu:14.04" : "d05e75b8",
} 

args = {
    "keypair_name"   : "AWS_buildbot",
    "security_group_name" : "buildbot_instance",
    "instance_type"  : "t2.medium",
    "AWS_AMI" : AWS_AMI["Ubuntu:14.04"],
    "AWS_VPC" : os.environ["AWS_VPC"],
    "AWS_SUBNET" : os.environ["AWS_SUBNET"],
}

env.hosts = [
    'localhosts',
]

def KILL_ALL():
    # This removes the keypair, security group and shuts down the instance
    pass

# Create AWS key/pair
def create_keypair():
    #ec2-delete-keypair AWS_buildbot

    f_keypair = "settings/{keypair_name}.pem".format(**args)
    if os.path.exists(f_keypair):
        msg = "keypair file already exists! exiting"
        raise ValueError(msg)
    cmd = "ec2-create-keypair {keypair_name} > " + f_keypair
    local(cmd.format(**args))

def _read_security_group():
    f_group = "settings/{security_group_name}.group".format(**args)
    
    # Determine the security group
    with open(f_group) as FIN:
        tokens = FIN.read().split()
        args["security_group"] = tokens[1]

def _read_instance_file():
    _read_security_group()
    f_instance = "settings/{security_group}.EC2".format(**args)
        
    # Determine the security group
    with open(f_instance) as FIN:
        tokens = FIN.read().split()
        args["instance_name"] = tokens[4]

def _read_public_IP():
    _read_instance_file()
    f_describe = "settings/{instance_name}.EC2".format(**args)
        
    # Determine the security group
    with open(f_describe) as FIN:
        tokens = FIN.read().split()
        args["status"] = tokens[8]
        args["public_IP"] = tokens[15] 
        print "INSTANCE STATUS", args["status"]
        print "PUBLIC IP", args["public_IP"]
        
# Create a security group
def create_security_group():
    f_group = "settings/{security_group_name}.group".format(**args)
    
    if os.path.exists(f_group):
        msg = "group file already exists! exiting"
        raise ValueError(msg)
    
    cmd = (
        'ec2-create-group {security_group_name} '
        '-d "BuildBot/Dispatch" '
        '--vpc {AWS_VPC} '
        '> '
    )
    local(cmd.format(**args) + f_group)
    _read_security_group()
    
    cmd = "ec2-authorize {security_group} -P 'all' >> "
    local(cmd.format(**args) + f_group)
 
# Launch an instance
def launch_EC2_instance():
    _read_security_group()

    f_instance = "settings/{security_group}.EC2".format(**args)

    if os.path.exists(f_instance):
        msg = "instance file already exists! exiting"
        raise ValueError(msg)
    
    bcmd = (
        "ec2-run-instances ami-{AWS_AMI} "
        "-t {instance_type} "
        "-k {keypair_name} "
        "-g {security_group} "
        "-s {AWS_SUBNET} "
        "--associate-public-ip-address true "
    )

    local(bcmd.format(**args) + " > " + f_instance)

# Get the state of the instance and save it
def get_public_IP():
    _read_instance_file()
    f_describe = "settings/{instance_name}.EC2".format(**args)

    #if os.path.exists(f_describe):
    #    msg = "instance description already exists! skipping"
    #    print msg
    #else:
    cmd = "ec2din {instance_name} > " + f_describe
    local(cmd.format(**args) )
        
    _read_public_IP()


def ssh():
    _read_public_IP()
    f_keypair = "settings/{keypair_name}.pem".format(**args)

    cmd = "ssh -i settings/{keypair_name}.pem ubuntu@{public_IP}"
    local(cmd.format(**args))

def _runscript(f_script):
    _read_public_IP()
    f_keypair = "settings/{keypair_name}.pem".format(**args)

    # Copy the file to the remote machine
    cmd = "scp -i settings/{keypair_name}.pem {f_script} ubuntu@{public_IP}:/home/ubuntu"
    local(cmd.format(f_script=f_script,**args))

    cmd = "ssh -t -i settings/{keypair_name}.pem ubuntu@{public_IP} 'sudo bash {f_script}'"
    local(cmd.format(f_script=f_script,**args))


def configure_server():
    _runscript("configure_server.sh")

def deploy():
    _runscript("deploy_buildbot.sh")
