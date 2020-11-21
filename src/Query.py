



import requests
import os

oauth = os.getenv('GHUB_OAUTH')
headers = {"Authorization": f"token {oauth}"}
            
# method from https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers,timeout=5)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# method from https://hackersandslackers.com/extract-data-from-complex-json-python/
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    if len(values) == 1:
        values = values[0]
    return values


#this should navigate to a desired level in the tree
#The idea is that from that level, we can iterate through a list of edges
def json_subset(obj,level_name):
    current_dict = obj
    if isinstance(obj,dict):
        if(len(obj.keys()) == 1):
            if(list(obj.keys())[0] == level_name):
                return current_dict
            else:
                key = list(obj.keys())[0]
                return json_subset(obj[key], level_name)
    elif isinstance(obj,list):
        return json_subset(obj[0], level_name)
        
    else:
        print("broken")
    
            


def get_result(query):
    try:
      result = run_query(query)
      return result
    except Exception as e:
        print(f"running again: {e}", flush=True)
        pass

def define_net_query(name,owner):
    return network_query.format(name,owner)

def define_user_query(login,org_id):
    return user_query.format(login,org_id)

def get_org_id(org):
    query  = get_result(org_query.format(org))
    org_id = json_extract(query,"org_id")
    return org_id


#define queries (copypaste from GraphiQL):
#Use f-strings for variable queries? or .format
# rename with aliases
network_query = """
query MyQuery2 {{
  repository(name: "{0}", owner: "{1}") {{
    stargazers(first: 80) {{
      edges {{
        node {{
          p_id: login
          following(first: 10) {{
            edges {{
              cursor
              node {{
                following_id: login
              }}
            }}
          }}
          followers(first: 10) {{
            edges {{
              cursor
              node {{
                follower_id: login
              }}
            }}
          }}
        }}
        cursor
      }}
    }}
  }}
}}
"""


#IMPORTANT: contColl only consists of last year
#@TODO: replicate with different time frames
#Q: maybe only look at most imporant members? time concerns

user_query = """
query MyQuery {{
  user(login: "{0}") {{
    organizations(first: 20) {{
      nodes {{
        org_name: name
      }}
    }}
    location: location
    company: company
    bio: bio
    contributionsCollection(organizationID: "{1}") {{
      totalCommitContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      totalRepositoriesWithContributedCommits
      totalRepositoriesWithContributedIssues
    }}
   }}
  
  }}
"""


#@TODO: different notions of contributions
#Need to fogure out org id


org_query ="""
query MyQuery {{
  organization(login: "{0}") {{
    org_id: id
  }}
}}

"""


"""




query MyQuery {
  user(login: "AakashKumarNain") {
    contributionsCollection(organizationID: "MDEyOk9yZ2FuaXphdGlvbjE1NjU4NjM4") {
      totalCommitContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      totalRepositoriesWithContributedCommits
      totalRepositoriesWithContributedIssues
    }
  }
}

"""
                                             



