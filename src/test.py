# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 18:47:11 2020

@author: Mikes_Surface2
"""

from Org_Network import Org_Network
import Create_Network
import networkx as nx

org_members = Org_Network("facebook",True).load_results()
net = Create_Network.match_collaborators(org_members)



#%%

#nx.draw_spring(net, node_size=10, width = 1)

a = nx.k_components(net)
