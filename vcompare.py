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
    debug = 0

    netlist = list()

    with open(filename) as csvreader:
        reader = csv.reader(csvreader, delimiter=',', quotechar='|')

        for row in reader:
            net = row[0]

            if("/null" in net):
                if(debug == 1):
                    print("\na_null\n")
                ## replace returns replaced string instead of by reference
                net = net.replace("null", "32")
                ##print("-- " + net)

            try:
                if(ipaddress.ip_network(net)):
                    ## add to list
                    if(debug == 1):
                        print("Good Network")
                    netlist.append(net)
                else:
                    print("bad network")
            except:
                ## bad data
                print("bad data in network\t" + net)

            if(debug == 1):
                print(net)

    return(netlist)
#endof build_ip_list()

def compare_net(list1, list2, meta_string1, meta_string2):
    print("in function compare_net")

    debug = 0
    print(meta_string1 + " " + meta_string2)

    len_list1 = len(list1)
    len_list2 = len(list2)

    for x in range(len_list1):
        if(debug == 1):
            print(list1[x] + " ++")
        l_match = 0

        for y in range(len_list2):
            if(list1[x] == list2[y]):
                l_match = 1
        
        if(l_match == 0):
            print(list1[x] + " found on " + meta_string1 + " but not on " + meta_string2)


def main():
    print("begin network list compare")

    debug = 0

    file1 = "/home/gdunlap/Code/python/vrf_net_compare/ind1.csv"
    file2 = "/home/gdunlap/Code/python/vrf_net_compare/ind2.csv"

    prelist = build_ip_list(file1)
    vrflist = build_ip_list(file2)

    if(debug == 1):
        print(len(prelist))
        print(len(vrflist))

    compare_net(prelist, vrflist, "Pre", "VRF")
    compare_net(vrflist, prelist, "VRF", "Pre")

    print("end")

if __name__ == "__main__":
    main()
#end of program