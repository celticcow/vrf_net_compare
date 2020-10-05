#!/usr/bin/python3 -W ignore::DeprecationWarning

import csv
import sys
import json
import time
import getpass
import requests
import argparse
import ipaddress
import apifunctions
from netzone import Netzone

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

"""
compare networks lists 
gdunlap / celticow

read in exiting group / list of networks
compare with output of vrf collections
"""

"""
read in file info.  defunct now, can be used in emergency with csv files.
"""
def build_ip_list_file(filename):
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

"""
compare lists and give diff
"""
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
#end_of_compare_net

"""
don't need function but it gave birth to a new one.
"""
#can we pass netlist by ref ??
def extract_group_to_list(name, netlist, mds_ip, sid):
    print("in extract group to list")

    debug = 0

    get_grp_json = {'name' : name}

    get_grp_result = apifunctions.api_call(mds_ip, "show-group", get_grp_json, sid)

    if(debug == 1):
        print(json.dumps(get_grp_result))

    if(debug == 1):
        print(len(get_grp_result['members']))

    for x in range(len(get_grp_result['members'])):
        if(debug == 1):
            print(get_grp_result['members'][x]['type'])

        if(get_grp_result['members'][x]['type'] == "network"):
            net_2_add = get_grp_result['members'][x]['subnet4'] + "/" + str(get_grp_result['members'][x]['mask-length4'])
            if(debug == 1):
                print(get_grp_result['members'][x]['subnet4'])
                print(get_grp_result['members'][x]['mask-length4'])
            netlist.append(net_2_add)
        elif(get_grp_result['members'][x]['type'] == "host"):
            net_2_add = get_grp_result['members'][x]['ipv4-address'] + "/32"

            netlist.append(net_2_add)
#end_of_extract_group_to_list

def extract_group_data_to_obj_list(name, Netzone, mds_ip, sid):
    print("in extract group data for netzone")
    debug = 0

    get_grp_json = {'name' : name}

    get_grp_result = apifunctions.api_call(mds_ip, "show-group", get_grp_json, sid)

    if(debug == 1):
        print(json.dumps(get_grp_result))

    if(debug == 1):
        print(len(get_grp_result['members']))

    for x in range(len(get_grp_result['members'])):
        if(debug == 1):
            print(get_grp_result['members'][x]['type'])

        if(get_grp_result['members'][x]['type'] == "network"):
            net_2_add = get_grp_result['members'][x]['subnet4'] + "/" + str(get_grp_result['members'][x]['mask-length4'])
            if(debug == 1):
                print(get_grp_result['members'][x]['subnet4'])
                print(get_grp_result['members'][x]['mask-length4'])
            
            Netzone.add_network(net_2_add)
            #netlist.append(net_2_add)
        elif(get_grp_result['members'][x]['type'] == "host"):
            net_2_add = get_grp_result['members'][x]['ipv4-address'] + "/32"

            #netlist.append(net_2_add)
            Netzone.add_network(net_2_add)
#end_of_extract_group_data_to_obj_list


def main():
    print("begin network list compare")

    debug = 1

    ## VRF1-OLIV-389
    ## TMP-OLIV

    ip_addr = "204.135.121.150"
    ip_cma  = "204.135.121.158"
    user    = "roapi"
    passwd  = "1qazxsw2"

    sid = apifunctions.login(user, passwd, ip_addr, ip_cma)

    if(debug == 1):
        print("session id : " + sid)

    ## pre lim versions of compare
    #file1 = "/home/gdunlap/Code/python/vrf_net_compare/ind1.csv"
    #file2 = "/home/gdunlap/Code/python/vrf_net_compare/ind2.csv"

    #prelist = build_ip_list_file(file1)
    #vrflist = build_ip_list_file(file2)
    
    #egrp1 = list()
    #egrp2 = list()

    #compare_net(prelist, vrflist, "Pre", "VRF")
    #compare_net(vrflist, prelist, "VRF", "Pre")

    #extract_group_to_list("TMP-OLIV", egrp1, ip_addr, sid)

    #print(len(egrp1))
    #extract_group_to_list("VRF1-OLIV-389", egrp2, ip_addr, sid)

    #print(len(egrp2))

    #print("-------------------------------------------------")

    #compare_net(egrp1, egrp2, "Pre", "VRF")
    #compare_net(egrp2, egrp1, "VRF", "Pre")
    
    """
    need to figure out what we're doing here
    """
    nzone_list = list()
    n1 = Netzone()
    n2 = Netzone()

    nzone_list.append(n1)
    nzone_list.append(n2)

    nz = 0
    with open('compare.csv') as csvreader:
        reader = csv.reader(csvreader, delimiter=',', quotechar='|')

        for row in reader:
            dataset = row[0]

            nzone_list[nz].set_name(dataset)
            #if(nz == 0):
            #    n1.set_name(dataset)
            #if(nz == 1):
            #    n2.set_name(dataset)

            for i in range(len(row)):
                if(i == 0):
                    pass
                else:
                    print("@@@ " + row[i])
                    extract_group_data_to_obj_list(row[i], nzone_list[nz], ip_addr, sid)
                    ###extract_group_to_list(row[i], nzone_list[nz].get_nets(), ip_addr, sid)
            ##print(len(row))
            nz += 1
            print("*^*^*^*^")

    ###
    compare_net(nzone_list[0].get_nets(), nzone_list[1].get_nets(), nzone_list[0].get_name(), nzone_list[1].get_name())
    compare_net(nzone_list[1].get_nets(), nzone_list[0].get_nets(), nzone_list[1].get_name(), nzone_list[0].get_name())

    ###
    print("Logging out Zzzzzzzz")
    time.sleep(20)

    ### logout
    logout_result = apifunctions.api_call(ip_addr, "logout", {}, sid)
    if(debug == 1):
        print(logout_result)

    print("end")

if __name__ == "__main__":
    main()
#end of program