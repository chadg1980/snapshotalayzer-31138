from setuptools import setup

setup(
    name='snapshotalayzer-31138',
    version='0.1',
    author='Chad H. Glaser',
    author_email='codingwithchad@gmail.com',
    description='snapshotalayzer-31138 is a tool to manage AWS EC2 snapshots',
    license='GPLv3+',
    packages=['shotty'],
    url='https://github.com/chadg1980/snapshotalayzer-31138',
    install_requres=[
        'click',
        'boto3'
    ],
    entry_points='''
        [consile_scripts]
        shotty=shotty.shotty:cli
    ''',
)