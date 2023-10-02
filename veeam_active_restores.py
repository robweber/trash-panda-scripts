"""
Active Restores

Connects to a Veeam B+R instance to retrieve a list of all restore jobs
Details on those actively running are given
"""
import argparse
import json
from veeam_easy_connect import VeeamEasyConnect

# parse the arguments
parser = argparse.ArgumentParser(description="Get Running Restore Jobs")
parser.add_argument("-H", '--host', required=True, help="Veeam B+R Host IP")
parser.add_argument("-u", '--username', required=True, help="Veeam username")
parser.add_argument("-p", '--password', required=True, help="Veeam password")

args = parser.parse_args()

result = {"total": 0, "in_progress": 0, "jobs": []}

# connect to Veeam
vec = VeeamEasyConnect(args.username, args.password, False) # insecure
vec.vbr().login(args.host)

# get all the restore sessions
res = vec.get("sessions?typeFilter=8", full=False)

# filter on the ones currently working
working_only = list(filter(lambda j: j['state'] in ('Working', 'Starting'), res['data']))

for j in working_only:
    result['jobs'].append({"name": j['name'], "progress": j['progressPercent'] })

# print the result as json
result['total'] = len(res['data'])
result['in_progress'] = len(working_only)
print(json.dumps(result))
