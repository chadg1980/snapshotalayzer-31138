# snapshotalayzer-31131
Demo project to manage AWS EC2 instance snapshots

## About
This project is a demo, and uses boto3 to manage AWC EC2 instance snapshots.

## Configuring

shotty uses the configureation file created by the AWS cli
`aws configure`


## Running

`pipenv run python shotty/shotty.py <command> <subcommand> <--project=PROJECT>`

*command* is instances, volumes, or snapshots
*subcommand* - depends on command 
*project* is optional
