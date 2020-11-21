# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 17:12:59 2020

@author: Mikes_Surface2
"""

# location of src 
import sys

sys.path.insert(0, "C:/Users/Mikes_Surface2/PycharmProjects/GHub-Networks/src") 
import pandas as pd
import networkx
import Query as Q

import matplotlib.pyplot as plt


"""
First 2 methods for GraphQL Queries with specific results in mind
Later Methods deal with org_network type of data

"""

#Function should take json result
#Get a list of primary ids: iterate and find friends for each
#id labels are from the query
#relevant layer is the top level where we can iterate through and extract data
def match_friends(json_result, layer):
    #Arrays are less data intensive and easier to use
    arr = []
    edge_layer = Q.json_subset(json_result, layer)[layer]
    #edge should be a dict
    for edge in edge_layer:
        #TODO: get rid of hard coding
        i_d = Q.json_extract(edge, "p_id")[0]
        following = Q.json_extract(edge, "following_id")
        followers = Q.json_extract(edge, "follower_id")
        arr.append([i_d,following,followers])
        
    return pd.DataFrame(data=arr,
                        columns=("id","following","followers")).set_index("id")
        

def make_net(friends_df):
    id_net = networkx.MultiDiGraph()
    for index, data in friends_df.iterrows():
       for label, col_val in data.iteritems():
           #TODO: get rid of hard coding
           if(label == "following"):
               for val in col_val:
                   id_net.add_edge(index,val)
           elif(label == "follower"):
               for val in col_val:
                   id_net.add_edge(val,index)
                    
    return id_net



#Iterate through df, create network based on network info
#Store contribution numbers, other data?\
def match_collaborators(df):
    collab_net = networkx.Graph()
    repos = set(df["repo"])
    for repo in list(repos):
        members = []
        #Determines who is in each repo
        belong = df["repo"] == repo
        belongers = df[belong].index
        members.extend(list(belongers))
        
        if(len(members) == 1):
            #Check case when sampling: possible only one member selected
            collab_net.add_node(members[0])
        else:
            for index, member in enumerate(members):
                exclude = members[:index]+members[index+1:]
                for person in exclude:
                    collab_net.add_edge(member,person)
            
    return collab_net



"""

from Org_Network import Org_Network
import Create_Network
load = Org_Network("facebook",True).load_results()
facebook = load.sample(50)
a = Create_Network.match_collaborators(facebook)
"""

#node_list = a._node




