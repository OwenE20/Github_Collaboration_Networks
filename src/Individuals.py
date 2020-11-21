# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 20:47:12 2020

@author: Mikes_Surface2
"""

import Query as Q
import pandas as pd
import networkx as nx

import re

#When making this smarter, have an object per graph?


def match_attributes(node_list,fields,org):
    #If adding information to the user query, this should accomodate
    #Given current hard coded df cleaning, col names won't be the same
    arr=[]
    org_id = Q.get_org_id(org)
    progress = len(node_list)
    if isinstance(node_list,dict):
        for label in node_list.keys():
            atts = []
            atts.append(label)
            var = Q.get_result(Q.define_user_query(label,org_id))
            for field in fields:
            
                atts.append(Q.json_extract(var,field))
            atts.append(determine_membership(var,org))
            arr.append(atts)
            progress -= 1
            print(progress)
        
    
    df = pd.DataFrame(data=arr)
    return df


#Figure out smarter way to do this
#Have a limited set of measures you want to add
#Broad classes: centrality, smthn, smthn, smthn
#Within classes, different measures
def match_measure(node_list, net, measure):
    #For now, with just one measure:
    measure = measure[0]
    arr = []
    if(measure == "centrality"):
        rel_measures = [nx.algorithms.centrality.betweenness_centrality(net)]
        for label in node_list.keys():
           measures = []
           measures.append(label)
           for meas in rel_measures:
               measures.append(meas[label])
           arr.append(measures)
               
              
               
    df = pd.DataFrame(arr)
    return df


def determine_membership(var, target_org):
    #Implements a few ways to see membership: company, org, and bio mentions
    fields = ("org_name","company","bio")
    pat = r"(?i){0}\b".format(target_org)
    
    orgs = Q.json_extract(var,fields[0])
    emplyr = Q.json_extract(var,fields[1])    
    bio = Q.json_extract(var,fields[2])
    
    if(orgs != None and len(orgs) != 0):
        if(target_org in orgs):
            return True
    elif(emplyr != None and len(emplyr) != 0):
        if(re.search(pat,emplyr) != None):
            return True
    elif(bio != None and len(bio) != 0):
        if(re.search(pat,bio) != None):
            return True
    
    return False
    
    
    
        

