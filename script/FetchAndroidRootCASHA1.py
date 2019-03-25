#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: xiaolanger1989@gmail.com

import urllib2
import re

debug = False
url = "https://android.googlesource.com/platform/system/ca-certificates/+/master/files/"

# visit ca list page
req = urllib2.Request(url)
res_data = urllib2.urlopen(req)
res = res_data.read()

if debug:
    # save ca list page for debug
    with open("ca_list_page", 'w') as f:
        f.write(res)

# extract ca list
rule = r'>([a-z0-9\.]+0)<'
pattern = re.compile(rule)
matchers = re.findall(pattern, res)

if debug:
    # save ca list for debug
    ca_list = ""
    for name in matchers:
        ca_list = ca_list + name + "\n"
    with open("ca_list", 'w') as f:
        f.write(ca_list)

sha1_list = ""
index = 0
for ca in matchers:
    # visit ca page
    req = url + ca
    res_data = urllib2.urlopen(req)
    res = res_data.read()

    if debug:
        # save ca page for debug
        with open("ca_page_" + ca, 'w') as f:
            f.write(res)

    # extract ca page
    rule = r'>([a-zA-Z0-9\-=,:/ ]+)<'
    pattern = re.compile(rule)
    matchers = re.findall(pattern, res)
    # concat text
    ca_page = ""
    for word in matchers:
        ca_page = ca_page + word

    # extract ca sha1
    rule = r'Fingerprint=([A-Z0-9:]+)'
    pattern = re.compile(rule)
    matchers = re.findall(pattern, ca_page)

    sha1 = matchers[0]
    sha1 = sha1.replace(":", "")
    index += 1
    print str(index) + ": " + sha1
    sha1_list = sha1_list + sha1 + "\n"

# save sha1 list
with open("ca_sha1_list", 'w') as f:
    f.write(sha1_list)
