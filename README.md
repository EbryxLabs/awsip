# awsip

A simple python library to check if an IP address, a list of IP addresses or a list of IP address ranges
exist inside Amazon (AWS) infrastructure.
```
pip install awsip
```
After installation, you can make use of `awsip` utility to check for IP addresses.
```
awsip 1.1.1.1 2.2.2.2 5.4.3.0/28
```
You can provide a white-spaced list of IP addresses / ranges. You can also provide a filename containing IP address / range on each line. For example, you have a file `myips.txt` with following format.
```
192.0.0.1
7.7.7.0/28
9.9.9.0/30
```
You can pass the IP addresses to utility while providing extra ips on the go like this:
```
awsip myips.txt 1.1.1.1 2.2.2.0/24
```
You can also make use of it in your custom code like this:
```
from awsip import AWSIPChecker
checker = AWSIPChecker()
checker.get_aws_range(['18.208.0.0', '18.208.0.0/16'])
```
You can provide a list of IP address, IP address ranges or a mixture of both and program will check if they belong to AWS and return appropriate data if they do belong.
