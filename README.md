# Let's Encrypt DCOS!

This is a sample [Marathon](https://github.com/mesosphere/marathon) app for encrypting your [Marathon-lb](https://github.com/mesosphere/marathon-lb) HAProxy endpoints using [Let's Encrypt](https://letsencrypt.org/). With this, you can automatically generate and renew valid SSL certs with Marathon-lb.

## Getting started

Clone (or manually copy) this repo, and modify the [letsencrypt-dcos.json](letsencrypt-dcos.json) file to include:
 - The list of hostnames (must be FQDNs) you want to generate SSL certs for (in both `SSL_DOMAINS` and `HAPROXY_0_VHOST`)
 - An admin email address for your certificate (in `SSL_EMAIL`)
 - The Marathon API endpoint (in `MARATHON_URL`)
 - The Marathon-lb app ID (in `MARATHON_LB_ID`)

Now launch the `letsencrypt-dcos` Marathon app:

```
$ dcos marathon app add letsencrypt-dcos.json
```

There are 2 test apps included, based on [openresty](https://openresty.org/), which you can use to test everything. Have a look in the `test/` directory within the repo.

## How does it work?

The app includes 2 scripts: [`run.sh`](run.sh) and [`post_cert.py`](post_cert.py). The first script (`run.sh`) will generate the initial SSL cert and POST the cert to Marathon for Marathon-lb. It will then attempt to renew & update the cert every 24 hours. The `post_cert.py` script will compare the current cert in Marathon to the current live cert, and update it as necessary. `post_cert.py` is called after the initial cert is generated, and again every 24 hours after a renewal attempt.

## Limitations

 - You may only have up to 100 domains per cert.
 - Currently, when the cert is updated, it requires a full redeploy of Marathon-lb. This means there may be a few seconds of downtime as the deployment occurs. This can be mitigated by placing another LB (such as an ELB or F5) in front of HAProxy.