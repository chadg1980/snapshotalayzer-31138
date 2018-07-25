import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

@click.command()
def list_instances():
    "list_instances\t\tList EC2 instances"
    print("listing instances...")
    for x in ec2.instances.all():
        print(', '.join((
            x.id,
            x.instance_type,
            x.placement['AvailabilityZone'],
            x.state['Name'],
            x.public_dns_name)))
    return
    
if __name__ == '__main__':
    list_instances()
    
