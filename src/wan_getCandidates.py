# -*- coding: utf-8 -*-
"""
Updated on Feb 10 10:12:45 2018
@author: Tara
"""

import json
import requests
import csv
import re
from simUtil import wordnet_similarity, w2v_similarity, cosine_similarity
from rank_candidates import calculate_rankall

def get_items(word,limit,api_key,api_url_base,onlyAdj=False):
    
   api_url = api_url_base+'apikey='+api_key+'&text='+word+'&lang=en&limit='+limit+'HTTP/1.1'
   response= requests.get(api_url)
  # print(response.content)
   
   
   if response.status_code >= 500:
      print('[!] [{0}] Server Error'.format(response.status_code))
   elif response.status_code == 404:
      print('[!] [{0}] URL not found: [{1}]'.format(response.status_code,api_url))
   elif response.status_code == 401:
      print('[!] [{0}] Authentication Failed'.format(response.status_code))
   elif response.status_code >= 400:
      print('[!] [{0}] Bad Request'.format(response.status_code))
   elif response.status_code >= 300:
      print('[!] [{0}] Unexpected redirect.'.format(response.status_code))
   elif response.status_code == 201:
      added_key = json.loads(response.content)
      print(added_key)

   j = json.loads(response.text)
   items = []
   length = len(j['response'][0]['items']);
   #print(str(len(j['response'][0]['items'])))
   if j['response'][0]['items']:
       for i in range(0,length-1):
           item = j['response'][0]['items'][i]['item'] 
           if onlyAdj == True:
              if  j['response'][0]['items'][i]['pos'] == 'adjective':
                  items.append(item)
                  #print(item)
           else:
              items.append(item)    
              #print(item)
               
   return items   

def get_common_adj(common_items,limit,api_key,api_url_base):
        common_adj = []
        for i in range(0,len(common_items)):
            for j in range(i+1,len(common_items)):
                items_i = get_items(common_items[i],limit,api_key,api_url_base,True)
                items_j = get_items(common_items[j],limit,api_key,api_url_base,True)
                new_common_items = list(set(items_i).intersection(items_j))
                #print(common_items[i], ',' , common_items[j] , '= ' , new_common_items) 
                common_adj = common_adj + new_common_items
                #print(common_items) 
                
        common_adj = common_items + common_adj        
        common_adj = list(set(common_adj))
        return common_adj
    
def getCandidates_union(source, target, limit):
    api_key = 'd4367eb2-79c1-4223-805f-5a9f032c6678'
    api_url_base = 'https://api.wordassociations.net/associations/v1.0/json/search?'
    
    items_src = get_items(source,limit,api_key,api_url_base, True)
    items_trg = get_items(target,limit,api_key,api_url_base, True)
    
    unionitems = list(set(items_src + items_trg))
    union = []
    if len(unionitems) >= 100:
        length = 100
    else:
        length = len(unionitems)
    
    for i in range(0,length-1): 
            union.append(unionitems[i].lower())
        
    strunion_list = ', '.join(union)
    cmm = re.sub('\'','' , strunion_list)           
    with open('wan_props_union_adj.csv','a') as file:
          writer = csv.writer(file)
          writer.writerow([source, target, cmm])
 
def getCandidates_inter_adj(source, target, limit):
    api_key = 'd4367eb2-79c1-4223-805f-5a9f032c6678'
    api_url_base = 'https://api.wordassociations.net/associations/v1.0/json/search?'
    
    items_src = get_items(source,limit,api_key,api_url_base, True)
    items_trg = get_items(target,limit,api_key,api_url_base, True)
    
    common_items = list(set(items_trg).intersection(items_src))        
    strunion_list = ', '.join(common_items)
    cmm = re.sub('\'','' , strunion_list)           
    with open('wan_props_inter_adj.csv','a') as file:
          writer = csv.writer(file)
          writer.writerow([source, target, cmm])    
       
def getCandidates(source, target, limit):
    api_key = 'd4367eb2-79c1-4223-805f-5a9f032c6678'
    api_url_base = 'https://api.wordassociations.net/associations/v1.0/json/search?'
    
    items_src = get_items(source,limit,api_key,api_url_base)
    items_trg = get_items(target,limit,api_key,api_url_base)
    """ 
    if  len(items_src) == 0:
          print('No Property found for source!')
    if len(items_trg) == 0:
         print('No Property found for target!')
    """     
     
     #find common properties
    common_items = list(set(items_trg).intersection(items_src))
    """
    if not common_items:
        #print('no common words at first level, increase the limit')
        common_items = common_items
    
    else:
    """
    #print(str(len(common_items)))
    #print('common items first level: ', common_items , '\n')
    common_adj = []
    
    #level 2 : get the adjectives of the previous common words
    common_adj = get_common_adj(common_items,limit,api_key,api_url_base)
    #level 3
    #common_adj2 = get_common_adj(common_adj,limit,api_key,api_url_base)
    
    common_adj.append(source)
    common_adj.append(target)
    common_adj = [x.lower() for x in common_adj]
    #print('common items second level: ',common_adj , '\n')
    #print('common items third level: ',common_adj2 , '\n')
    """
    if len(common_adj) == 2:
        common_adj = common_adj
        #print('No Common Properties found!')
    else:    
    """    
    #####################################
    ##write common properties in csv##### 
    strcmm = ', '.join(common_adj)
    cmm = re.sub('\'','' , strcmm)           
    with open('wan_props.csv','a') as file:
          writer = csv.writer(file)
          writer.writerow([source, target, cmm])
    #####################################       
        
if __name__ == '__main__':

     """
     limit = '300'
     infile = 'annotations.csv'          
     csv_file = csv.reader(open(infile, "r"), delimiter=",")
     header = next(csv_file)
     sIndex = header.index("source")
     tIndex = header.index("target")
     for row in csv_file:
        if row:
            source = row[sIndex]
            target = row[tIndex]
            ###run once
            #getCandidates(source, target, limit)  intersection + all words and their adj
            #getCandidates_union(source, target, limit) union + adj 
            getCandidates_inter_adj(source, target, limit) #intersection+ only adj : small list of intersection!!! No good
     """       
     #######################################
     """
     infile = 'wan_props.csv'
     w2v_outfile = 'wan_ranked_props_w2v.csv'
     wn_outfile = 'wan_ranked_props_wordnet_test.csv'
     calculate_rankall('wordnet',infile,w2v_outfile, wn_outfile)
     """
     
 
     
             
      
     



