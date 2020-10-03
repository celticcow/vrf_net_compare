#!/usr/bin/python3

"""
class define list of networks
and meta data for compare convert
for vrf conversions
"""
class Netzone(object):

    #constructor
    def __init__(self, name="default"):
        self.name = name
        self.networks = list()
        ##

    #accessor
    def get_network_count():
        return(len(self.networks))


    #modifiers
    def set_name(self, name):
        self.name = name

    def add_network(self, net):
        self.networks.append(net)


