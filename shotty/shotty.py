import boto3

if __name__ == '__main__':
    session = boto3.Session(profile_name='shotty')

    ec2 = session.resource('ec2')
    for x in ec2.instances.all():
        print(x)
    
