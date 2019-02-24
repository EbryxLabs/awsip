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
handle.setFormatter(logging.Formatter('%(asctime)s > %(message)s'))
logger.addHandler(handle)


AWS_RANGE_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def get_params():

    parser = argparse.ArgumentParser()
    parser.add_argument('ip', nargs='+',
                        help='white spaced list of ip addresses / ip ranges. '
                             'AND/OR filename containing ip address / range'
                             'at each line.')

    args = parser.parse_args()
    return args


class AWSIPChecker:

    def __init__(self):

        res = requests.get(AWS_RANGE_URL)
        res = json.loads(res.content)
        if 'prefixes' not in res:
            logger.info('Could not get ip prefixes from url: %s',
                        AWS_RANGE_URL)
            exit(0)

        self.ipdata = res['prefixes']

    def get_aws_range(self, ips, logging=False):

        aws_ranges = dict()
        for ip in ips:
            aws_ranges[ip] = list()
            ips_to_check = list()
            if '/' in ip:
                ips_to_check.append(ipaddress.ip_network(ip)[0])
                ips_to_check.append(ipaddress.ip_network(ip)[-1])
            else:
                ips_to_check.append(ip)

            for data in self.ipdata:
                is_within_range = list()
                iprange = data['ip_prefix'] if 'ip_prefix' in \
                    data else data['ipv6_prefix']

                for target_ip in ips_to_check:
                    if ipaddress.ip_address(target_ip) in \
                            ipaddress.ip_network(iprange):
                        is_within_range.append(True)
                    else:
                        is_within_range.append(False)

                if False not in is_within_range:
                    aws_ranges[ip].append(data)
                    if logging:
                        logger.info('%s belongs to [%s][%s][%s]',
                                    ip, iprange, data['region'],
                                    data['service'])
        return aws_ranges


def main():

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
    checker = AWSIPChecker()
    checker.get_aws_range(ips, logging=True)
