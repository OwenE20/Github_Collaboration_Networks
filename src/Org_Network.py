# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 18:37:02 2020

@author: Mikes_Surface2
"""





class Org_Network:
    import requests
    import pickle
    import pandas as pd
    
    def __init__(self,org,built):
        self.org = org
        self.headers = {"Authorization": "token 1d16088cd6f7dc7ad05d8a983d7626037e0475bc"}
        if(not built):
            self.construct_individuals()

    
    def get_repos(self,headers):
        #Query github, get links for repos
        result = []
        empty = False
        page = 1
        while not empty:
            new_result = self.requests.get("https://api.github.com/orgs/{0}/repos?page={1}&per_page=100".format(self.org,page), 
                                      headers=headers).json()
            result.extend(new_result)
            if(len(new_result) == 0):
                empty = True       
            page += 1
        
        repos = []
        for call in result:
            repos.append(call["name"])
            
        return repos
    
    
    #def get_org_people(org):
        
    
    def get_collaborators(self,repo,headers):
        result = []
        
        empty = False
        page = 1

        while not empty:
            new_result = self.requests.get("https://api.github.com/repos/{0}/{1}/contributors?page={2}&per_page=100?anon=1".format(self.org,repo,page), 
                                      headers=headers).json()
            result.extend(new_result)
            if(len(new_result) == 0):
                empty = True       
            page += 1
        
        #consider adding personal attributes here
        contributor_contributions = []
        for call in result:
            individual = []
            
            #name of individual
            individual.append(call["login"])
            
            #total contributions
            individual.append(call["contributions"])
        
            individual.append(repo)
            
            contributor_contributions.append(individual)
            
            #@TODO: more 
            #Can add things to keep track of
            #Maybe get all attributes through this query? More complex
            # GET /repos/:owner/:repo/commits?path=:path-to-file
            
            
        return self.pd.DataFrame(data=contributor_contributions,
                            columns=("id","contributions",
                                     "repo")).set_index("id")



    def save_results(self,df):
        file_name = "{}.pickle".format(self.org)
        try:
            open(file_name, "x")
            with open(file_name, 'wb') as f:
                self.pickle.dump(df, f)
                
        except:
            with open(file_name, 'wb') as f:
                self.pickle.dump(df, f)
                
        
    def load_results(self):
        file = "{}.pickle".format(self.org)
        try:
            with open(file, 'rb') as f:
                return self.pickle.load(f)
        except:
            return None
        

    def construct_individuals(self):
        #Wrapper that uses all the methods
        repos = self.get_repos(self.headers)


        #Hard coded, would need to be changed if changing vals of interest
        total_individuals = self.pd.DataFrame(columns=("contributions",
                                                  "repo"))
        for repo in repos:
            repo_indiv = self.get_collaborators(repo,self.headers)
            total_individuals = self.pd.concat([total_individuals,repo_indiv],sort=False)
        
        
        self.save_results(total_individuals)
        



       
    
