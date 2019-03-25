#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: xiaolanger1989@gmail.com
import os
import re
import sys

def get_smali(path, ext, out):
    dirs = os.listdir(path)
    for d in dirs:
        dpath = path + "/" + d
        if os.path.isdir(dpath):
            get_smali(dpath, ext, out)
        elif ext in dpath:
            out.append(dpath)

def get_identifier(path, out):
    # smali in lines
    lines = []
    # rules to the variables
    rules = []
    # values to the variables
    ret = []

    with open(path, 'r') as smali:
        for line in smali.readlines():
            lines.append(line)

        for line in lines[::-1]:
            # invoke-virtual {v0, p4, v2, v1}, Landroid/content/res/Resources;->getIdentifier
            rule = r'invoke-virtual \{\w+, (\w+), (\w+), \w+\}, Landroid/content/res/Resources;->getIdentifier'
            pattern = re.compile(rule)
            matcher = re.search(pattern, line)
            if matcher != None:
                # variables to find
                v2 = matcher.group(1)
                v3 = matcher.group(2)

                # init
                rules = []
                ret = []

                # const-string v2, "moxie_client_common_title"
                # const-string/jumbo v5, "layout_inflater"
                rules.append("const-string " + v3 + ', "(\w+)"')
                rules.append("const-string " + v2 + ', "(\w+)"')
            elif len(rules) > 0:
                if len(ret) == 0:
                    pattern = re.compile(rules[0])
                elif len(ret) == 1:
                    pattern = re.compile(rules[1])

                matcher = re.search(pattern, line)
                if matcher != None:
                    ret.append(matcher.group(1))

                if len(ret) == 2:
                    # save
                    out["R." + ret[0] + "." + ret[1]] = 1

                    # init
                    rules = []
                    ret = []

def prompt():
    print "eg: python {0} -file path".format(sys.argv[0])

if __name__ == "__main__":
    if len(sys.argv) > 2:
        f = ""
        for i in range(len(sys.argv)):
            cmd = sys.argv[i]
            if cmd == "-file":
                f = sys.argv[i + 1]
        try:
            # smali paths
            paths = []
            get_smali(f, ".smali", paths)
            # result
            strs = {}
            for path in paths:
                get_identifier(path, strs)
            for s in strs.keys():
                print s
        except:
            prompt()
    else:
        prompt()
