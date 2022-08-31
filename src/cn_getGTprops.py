# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 17:07:11 2018

@author: Tahereh
"""
from cn_getCandidates import get_items
from simUtil import  w2v_similarity, wordnet_similarity
import csv
import operator
import re

def getItemsFromAPI(method):
    
    api_url_base = 'http://api.conceptnet.io/query?node=/c/en/' 
    infile = 'annotations.csv'

    
    csv_file = csv.reader(open(infile, "r"), delimiter=",")
    header = next(csv_file)
    p1Index = header.index("p1")
    p2Index = header.index("p2")
    p3Index = header.index("p3")
    sIndex = header.index("source")
    tIndex = header.index("target")
    for row in csv_file:
        if row:
            
            P1 = row[p1Index]
            P2 = row[p2Index]
            P3 = row[p3Index]
            source = row[sIndex]
            target = row[tIndex]
          
            P1list = []  
            #print(P1, P2, P3)
            P1items  = get_items(P1,api_url_base)
            #print(P1items)
            if len(P1items) >= 10:
                length = 10
            else:
                length = len(P1items)
                
            for i in range(0,length-1): 
                    P1list.append(P1items[i])
            
            P1list.append(P1)  #append the property itself to the list of its properties
            if method == 'w2v':
                sim_dic1P1  = w2v_similarity(P1list, P1 , '', 'w2vSimModel1')
            else:
                sim_dic1P1  = wordnet_similarity(P1list, P1, '')
                
            rank_list_P1 = sorted(sim_dic1P1.items(),key=operator.itemgetter(1) , reverse = True) 
            rank_list_P1 = [i[0] for i in rank_list_P1]
            #print(rank_list_P1)
            strP1 = ', '.join(rank_list_P1)
            P1itemsStr = re.sub('\'','' , strP1)
            
            #######################
            P2list = []        
            P2items  = get_items(P2,api_url_base)    
            if len(P2items) >= 10:
                length = 10
            else:
                length = len(P2items)
            
            for i in range(0,length-1): 
                    P2list.append(P2items[i])
            
            P2list.append(P2)
            if method == 'w2v':
                sim_dic1P2  = w2v_similarity(P2list, P2, '', 'w2vSimModel2')
            else:
                sim_dic1P2  = wordnet_similarity(P2list, P2, '')
                
            rank_list_P2 = sorted(sim_dic1P2.items(),key=operator.itemgetter(1) , reverse = True)    
            rank_list_P2 = [i[0] for i in rank_list_P2]
            strP2 = ', '.join(rank_list_P2)
            P2itemsStr = re.sub('\'','' , strP2)
            #######################
            P3list = []        
            P3items  = get_items(P3,api_url_base)       
            if len(P3items) >= 10:
                length = 10
            else:
                length = len(P3items)
                
            for i in range(0,length-1): 
                    P3list.append(P3items[i])
            
            P3list.append(P3)
            if method == 'w2v':
                sim_dic1P3  = w2v_similarity(P3list, P3, '', 'w2vSimModel3')  #similarities are not absolute!
            else:
                sim_dic1P3  = wordnet_similarity(P3list, P3, '')
                
            rank_list_P3 = sorted(sim_dic1P3.items(),key=operator.itemgetter(1) , reverse = True)  
            rank_list_P3 = [i[0] for i in rank_list_P3]
            strP3 = ', '.join(rank_list_P3)
            P3itemsStr = re.sub('\'','' , strP3)   
            ######################            
            #word2vec
            if method == 'w2v':
                with open('cn_GTProps_props_w2v.csv','a') as file:
                    writer = csv.writer(file)
                    writer.writerow([source, target,P1, P1itemsStr, P2, P2itemsStr, P3, P3itemsStr])
         
            else:            
            #wordnet   
                with open('cn_GTProps_props_wordnet.csv','a') as file:
                    writer = csv.writer(file)
                    writer.writerow([source, target,P1, P1itemsStr, P2, P2itemsStr, P3, P3itemsStr])  
   
                          
if __name__ == '__main__':
    getItemsFromAPI(method='wordnet')