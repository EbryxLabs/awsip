# awsip

A simple python library to check if an ip, a list of ips or a list of ip ranges
exist inside Amazon (AWS) infrastructure.
```
pip install awsip
```
After installation, you can make use of `awsip` utility to check for ips.
```
awsip -ips 1.1.1.1 2.2.2.2 5.4.3.0/28
```
Using `-ips` parameter, you can provide a white-spaced list of ip addresses / ranges. You can also provide a filename containing ip address / range on each line. For example, you have a file `myips.txt` with following format.
```
192.0.0.1
7.7.7.0/28
9.9.9.0/30
```
You can pass the ips to utility while providing extra ips on the go like this:
```
awsip -ips myips.txt 1.1.1.1 2.2.2.0/24
```