#! /usr/bin/env python

import os
import sys
import json
import argparse
import subprocess

def usage(name=None):
        return '''bigpanda.py usage
-----------------

Download jobs info from BigPanda:

    bigpanda.py --download -u USERNAME [-f jobs.json]

Show (and filter) jobs:

    bigpanda.py --show [--taskname XXX] [--status done] [--sort taskname]
'''

parser = argparse.ArgumentParser(description='Show jobs from bigpanda', usage=usage())

parser.add_argument('-d', '--download', dest='download', action='store_true', help='Download jobs from bigpanda')
parser.add_argument('-s', '--show', dest='show', action='store_true', help='Show jobs from bigpanda')

parser.add_argument('-f', dest='jobs_file', default='jobs.json',  help='Jobs file (default: jobs.json)')
parser.add_argument('-u', dest='username', default=os.environ['USER'], help='Username')

# Filter
parser.add_argument('--taskname', dest='taskname', help='Filter by taskname')
parser.add_argument('--status',   dest='status',   help='Filter by status')
parser.add_argument('--taskid',   dest='taskid',   help='Filter by taskid')

# Sort
parser.add_argument('--sort', dest='sort', default='taskname',  help='Sort by taskname/status (default: taskname)')


args = parser.parse_args()

if not args.download and not args.show:
    print(usage())
    sys.exit(0)


jobs_file = args.jobs_file

# Dowload jobs
if args.download:

    if os.path.isfile(jobs_file):
        os.system('rm %s' % jobs_file)

    cmd1 = 'ssh falonso@lxplus.cern.ch "cern-get-sso-cookie -u https://bigpanda.cern.ch/ -o bigpanda.cookie.txt;"'

    os.system(cmd1)

    cmd2 = 'ssh falonso@lxplus.cern.ch "curl -b ~/bigpanda.cookie.txt -H \'Accept: application/json\' -H \'Content-Type: application/json\' "https://bigpanda.cern.ch/tasks/?taskname=user.%s*&days=10\&json""' % args.username

    output = subprocess.check_output(cmd2, shell=True)

    with open(jobs_file, 'w') as f:
        f.write(output)




# Show jobs
def print_job(j):

    dsinfo = j['dsinfo']

    nfiles = dsinfo['nfiles']
    nfiles_failed = dsinfo['nfilesfailed']
    nfiles_finished = dsinfo['nfilesfinished']

    print('{0: <10} {1: <125} {2: <15} {3: >5}/{4: >5}'.format(j['jeditaskid'], j['taskname'], j['status'], nfiles_finished, nfiles))


if args.show:

    with open(jobs_file) as f:

        jobs = json.load(f)

        # Filter task name
        if args.taskname is not None:
            jobs = [ j for j in jobs if args.taskname in j['taskname'] ]

        # Filter status
        if args.status is not None:
            jobs = [ j for j in jobs if args.status == j['status'] ]

        # Filter taksID
        if args.taskid is not None:
            jobs = [ j for j in jobs if args.taskid == str(j['jeditaskid']) ]



        # Show jobs
        for j in sorted(jobs, key=lambda t: t[args.sort]):
            print_job(j)
