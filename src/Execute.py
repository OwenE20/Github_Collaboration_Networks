# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:16:54 2020

@author: Mikes_Surface2
"""

from Org_Network import Org_Network
import Create_Network
import Individuals
import pandas as pd



"""
Main class to easily implement solution for multiple orgs

Major TODOS:
    -clean up and follow style guide
    -implement other measures of network
    -include more attributes of members
    -Get rid of hard coding
    -Make project presentable
    -Google GeoCoding API [2] to get lat and lon

"""

def create_results(orgs,attributes, measures):
    for org in orgs:
        print(f"processing {org}")
        try:
            print("____Creating Name List____")
            
            #If implementing sample size, need to check if within bounds
            #Maybe with proportion version? Dunno if that would be useful
            #Set true for testing
            org_members = Org_Network(org,False).load_results()
            
            print("__Constructing Network____")
            net = Create_Network.match_collaborators(org_members)
            node_list = net._node
            
            print("____Matching Atts, Measures____")
            atts = Individuals.match_attributes(node_list, attributes, org)
            meas = Individuals.match_measure(node_list,net,measures)
            
            print(atts)
            
            #Hard coding for now
            #@TODO: don't
            print("____Cleaning Dfs_____")
            col_list = ["id"]
            col_list.extend(attributes)
            col_list.extend(["member"])
            
            
            atts.columns = col_list
            atts = atts.set_index("id")
        
            print(meas)
                
            meas_col = ["name"]
            meas_col.extend(measures)
            print(meas_col)
            meas.columns = meas_col
            meas = meas.set_index("name")
            
            
            
            combined = pd.concat([meas,atts],axis=1)
            
            #Making a copy just in case we want to save raw
            #@TODO: get rid of hard coding
            sample = org_members.copy()
            sample["contributions"] = sample["contributions"].astype("int32")
            sample["name"] = sample.index
            summarized = sample.groupby(by=["name",]).sum()
            
            final = pd.concat([summarized,combined],axis=1)
            
            
            print("Saving....")
        
            file_name = f"{org}_final.csv"
            final.to_csv(file_name)
            
            #save query results to look at repo-level information
            raw_file_name = f"{org}_raw.csv"
            org_members.to_csv(raw_file_name)
            
            

            #return final, org_members

        except Exception as e:
            print(e)
            print("broke at above step")
            pass
        

        
    
orgs_of_interest = ["google-research",]
create_results(orgs_of_interest,("location",
                                     "totalCommitContributions",
                                     "totalIssueContributions",
                                     "totalPullRequestReviewContributions",
                                     "totalRepositoriesWithContributedCommits",
                                     "totalRepositoriesWithContributedIssues"),
                   ["centrality"])



