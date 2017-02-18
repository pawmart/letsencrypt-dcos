#!/usr/bin/env python

import os
import sys
import json
import requests
import time

base_url = os.environ.get('MARATHON_URL')
headers = {'Content-Type': 'application/json', 'Authorization': 'token=' + os.environ.get('MARATHON_AUTH_TOKEN')}

marathon_lb_id = os.environ.get('MARATHON_LB_ID')
marathon_lb_cert_env = \
    os.environ.get('MARATHON_LB_CERT_ENV', 'HAPROXY_SSL_CERT')

print("Retrieving current marathon-lb cert")
sys.stdout.flush()

marathon_lb_url = base_url + '/v2/apps/' + marathon_lb_id
r = requests.get(marathon_lb_url, headers=headers)
mlb = r.json()
env = mlb['app']['env']
cert = ''

with open(sys.argv[1], 'r') as f:
    cert = f.read()

print("Comparing old cert to new cert")
sys.stdout.flush()
if cert != env.get(marathon_lb_cert_env, ''):
    env[marathon_lb_cert_env] = cert

    print("Deploying marathon-lb with new cert")
    sys.stdout.flush()
    r = requests.put(marathon_lb_url,
                     headers=headers,
                     data=json.dumps({
                         'id': marathon_lb_id,
                         'env': env
                     }, encoding='utf-8'))
    deploymentId = r.json()['deploymentId']

    # Wait for deployment to complete
    deployment_exists = True
    while deployment_exists:
        time.sleep(5)
        print("Waiting for deployment to complete")
        sys.stdout.flush()
        r = requests.get(base_url + '/v2/deployments', headers=headers)
        deployments = r.json()
        deployment_exists = False
        for deployment in deployments:
            if deployment['id'] == deploymentId:
                deployment_exists = True
                break
    print("Deployment complete")
    sys.stdout.flush()
else:
    print("Cert did not change")
    sys.stdout.flush()
