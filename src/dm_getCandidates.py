# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 15:25:34 2018

@author: Tahereh
"""
import json
import urllib.request
import re
import csv
from rank_candidates import calculate_rankall
from simUtil import wordnet_similarity, w2v_similarity


def get_items(word,api_url_base):
    
   query = api_url_base + word
   data = json.loads(urllib.request.urlopen(query).read())

   items = []
   length = len(data);
   if data:
       for i in range(0,length-1):
           item = data[i]['word']
           items.append(item)    
            
   return items   
 
def get_moreAdjs(common_items,api_url_base):
        common_adj = []
        for i in range(0,len(common_items)):
            for j in range(i+1,len(common_items)):
                items_i = get_items(common_items[i],api_url_base)
                items_j = get_items(common_items[j],api_url_base)
                new_common_items = list(set(items_i).intersection(items_j))
                common_adj = common_adj + new_common_items
                
        common_adj = common_items + common_adj        
        common_adj = list(set(common_adj))
        return common_adj
    
def getCandidates_inter(source, target):
    
    api_url_base = 'https://api.datamuse.com/words?rel_jjb='
    items_src = get_items(source,api_url_base)
    items_trg = get_items(target,api_url_base)
    
    common_items = list(set(items_trg).intersection(items_src))
    common_adj = []
    
    #level 2 : get the adjectives of the previous common adjectives
    common_adj = get_moreAdjs(common_items,api_url_base)
    
    common_adj.append(source)
    common_adj.append(target)
    common_adj = [x.lower() for x in common_adj]
    
    strcmm = ', '.join(common_adj)
    cmm = re.sub('\'','' , strcmm)               
    with open('dm_props_inter.csv','a') as file:
          writer = csv.writer(file)
          writer.writerow([source, target, cmm])
          
         
def getCandidates_union(source, target):
    api_url_base = 'https://api.datamuse.com/words?rel_jjb='    
    items_src = get_items(source,api_url_base)
    items_trg = get_items(target,api_url_base)
    
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
    with open('dm_props_union.csv','a') as file:
          writer = csv.writer(file)
          writer.writerow([source, target, cmm])
          
if __name__ == '__main__':
    
     """
     infile = 'annotations.csv'          
     csv_file = csv.reader(open(infile, "r"), delimiter=",")
     header = next(csv_file)
     sIndex = header.index("source")
     tIndex = header.index("target")
     for row in csv_file:
        if row:
            source = row[sIndex]
            target = row[tIndex]
            #getCandidates_inter(source, target) 
            getCandidates_union(source, target) 
     
     """
     """
     infile = 'dm_props_union.csv'
     w2v_outfile = 'dm_ranked_props_w2v_union.csv'
     wn_outfile = 'dm_ranked_props_wordnet_union.csv'
     calculate_rankall('wordnet',infile,w2v_outfile, wn_outfile)   
     """
     