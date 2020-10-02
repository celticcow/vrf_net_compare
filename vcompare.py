#!/usr/bin/python3

import csv
import sys
import argparse
import ipaddress


"""
read in exiting group / list of networks
compare with output of vrf collections
"""

def build_ip_list(filename):
    print("in build_ip_list")
    debug = 1

    with open(filename) as csvreader:
        reader = csv.reader(csvreader, delimiter=',', quotechar='|')

        for row in reader:
            net = row[0]
            print(net)

#endof build_ip_list()

def main():
    print("begin network list compare")

    file1 = "/home/gdunlap/Code/python/vrf_net_compare/ind1.csv"
    file2 = "/home/gdunlap/Code/python/vrf_net_compare/ind2.csv"

    build_ip_list(file1)
    build_ip_list(file2)

    print("end")

if __name__ == "__main__":
    main()
#end of program