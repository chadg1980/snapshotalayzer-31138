import boto3
import click
import botocore

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()
    return instances
#Click Groups
@click.group()
def cli():
    """Shotty manages snapshots"""

#Snapshots
@cli.group('snapshots')
def snapshots():
    """commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, 
help="Only snapshots for project (tag Project:<name>)")
    
def list_snapshots(project):
    "List EC2 snapshots" 
    
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                print(", ".join((
                    s.id, 
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
    return

#volumes
@cli.group('volumes')
def volumes():
    """commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, 
help="Only volumes for project (tag Project:<name>)")
    
def list_volumes(project):
    "List EC2 volumes" 
    
    instances = filter_instances(project)
    for i in instances:
        for v in i.volumes.all():
             print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) +"GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
             )))
    
    return

#instances
@cli.group('instances')
def instances():
    """commands for instances"""

@instances.command('list')
@click.option('--project', default=None, help="Only instances for project (tag Project:<name>)")
    
def list_instances(project):
    "list_instances/t/t list EC2 instances" 
    
    instances = filter_instances(project)
    for i in instances:
        tags = { t['Key']:t['Value'] for t in i.tags or [] }
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project>')
            )))
    return

@instances.command('stop')
@click.option('--project', default=None, help="Only instances for project")
def stop_instance(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        try:
            i.stop()
        except botocore.exceptions.ClientError as e:
            print(" Could not stop {0} ".format(i.id) + str(e))
            continue
    return


@instances.command('start')
@click.option('--project', default=None, help="Only instances for project")
def start_instance(project):
    "start EC2 instances"
    instances = filter_instances(project)

    for i in instances:
        print("Starting {0}...".format(i.id))
        try:
            i.start()
        except botocore.exceptions.ClientError as e:
            print(" Could not start {0} ".format(i.id) + str(e))
            continue
    return

#take snapshot of the instance
@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None, help="Only instances for project")
def create_snapshot(project):
    """Create snapshots for EC2 instances"""
    instances = filter_instances(project)

    for i in instances:
        print("Stopping {0}...".format(i.id))
        
        i.stop()
        i.wait_until_stopped()
        
        for v in i.volumes.all():
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by Snapshotalayzer 311138")
        
        print("Starting {0}...".format(i.id))
        i.start()
        i.wait_until_running()
    print("Jobs all done!")
    return



# MAIN 
if __name__ == '__main__':
    cli()
    
