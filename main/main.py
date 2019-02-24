import os
import json
import logging
import argparse
import ipaddress


import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handle = logging.StreamHandler()
handle.setLevel(logging.INFO)
handle.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(handle)


RANGE_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_params():

    parser = argparse.ArgumentParser()
    parser.add_argument('ip', nargs='+',
                        help='white spaced list of ip addresses / ip ranges. '
                             'AND/OR filename containing ip address / range'
                             'at each line.')

    args = parser.parse_args()
    return args


def main():

    print(str())
    params = get_params()
    ips = params.ip
    if not ips:
        logger.info('No ips detected.')
        exit(0)

    for ip in ips.copy():
        if os.path.isfile(ip):
            ips.remove(ip)
            ips.extend([x.strip('\n') for x in open(ip, 'r').readlines()])

    ips = list(set(ips))
    res = requests.get(RANGE_URL)
    res = json.loads(res.content)
    if 'prefixes' not in res:
        logger.info('Could not get ip prefixes from url: %s', RANGE_URL)
        exit(0)

    ipdata = res['prefixes']
    for ip in ips:

        ips_to_check = list()
        if '/' in ip:
            ips_to_check.append(ipaddress.ip_network(ip)[0])
            ips_to_check.append(ipaddress.ip_network(ip)[-1])
        else:
            ips_to_check.append(ip)

        for data in ipdata:
            within_range = list()
            iprange = data['ip_prefix'] if 'ip_prefix' in \
                data else data['ipv6_prefix']

            for target_ip in ips_to_check:
                if ipaddress.ip_address(target_ip) in \
                        ipaddress.ip_network(iprange):
                    within_range.append(True)
                else:
                    within_range.append(False)

            if False not in within_range:
                logger.info('%s belongs to [%s][%s][%s]',
                            ip, iprange, data['region'], data['service'])


if __name__ == "__main__":
    main()
