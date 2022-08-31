# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 16:39:44 2018

@author: Tahereh
"""
from simUtil import w2v_similarity, wordnet_similarity
import csv
import operator

def writeTocsv(source, target, ci_list,outfile):
            ci_list10 = [] 
            ci_list100 = []
            
            if ci_list:
                
                cistr1 = ci_list[0][0]         
            
                if len(ci_list) >= 10:
                   for i in range(0,10):
                       prop = ci_list[i][0]
                       ci_list10.append(prop)
                   ci_list10 = ci_list10[:10]
                else:
                    for i in range(0,len(ci_list)):
                       prop = ci_list[i][0]
                       ci_list10.append(prop)
                    ci_list10 = ci_list10[:len(ci_list)] 
                      
               
                if len(ci_list) >= 100:
                   for i in range(0,100):
                      prop = ci_list[i][0]
                      ci_list100.append(prop)
                   ci_list100 = ci_list100[:100]  
                   
                else:
                    for i in range(0,len(ci_list)):
                      prop = ci_list[i][0]
                      ci_list100.append(prop)
                    ci_list100 = ci_list100[:len(ci_list)]
                    
                    
                cistr10 = ', '.join(ci_list10)
                cistr100 = ', '.join(ci_list100)
                
            else:
               cistr1 = ''
               cistr10  = ''
               cistr100 = ''
               
               
            
            with open(outfile,'a') as file:
                  writer = csv.writer(file)
                  writer.writerow([source, target, cistr1 , cistr10 , cistr100])
                  
def rank(sim_src, sim_trg, source, target):
            #	pi = ti * si
            pi_rank = {}
            for key, value in sim_src.items():
                if key != source and key != target:
                   pi = round((sim_src[key] * sim_trg[key]) , 4)
                   pi_rank[key] = pi     
        
            #	di= si - ti
            di_rank = {}
            for key, value in sim_src.items():
                if key != source and key != target:
                   di = round((sim_src[key] - sim_trg[key]) , 4)
                   di_rank[key] = di
                
        
            """
           #zi = ti + si
            zi_rank = {}
            for key, value in sim_src.items():
               if key != source and key != target:
                  zi = round((sim_src[key] + sim_trg[key]) , 4)
                  zi_rank[key] = zi
                  #print(zi)
            """         
        
            #ci = min(rank(pi), rank(di))           
            ci_rank = {}
            for key, value in sim_src.items():
                if key != source and key != target:
                   ci = round(min(abs(pi_rank[key]),abs(di_rank[key])) , 3)
                   #if ci != 0 or outfile != '':
                   ci_rank[key] = ci
            ci_list = sorted(ci_rank.items(),key=operator.itemgetter(1) , reverse = True) 
     
                  
            #ci* = min(rank(zi), rank(di))
            """
            ci_rank2 = {}
            for key, value in sim_src.items():
                if key != source and key != target:
                   ci2 = round(min(abs(zi_rank[key]),aabs(di_rank[key])) , 4)
                   ci_rank2[key] = ci2
            ci_list2 = sorted(ci_rank2.items(),key=operator.itemgetter(1) , reverse = True) 
            print('ci* rank: ',ci_list2 , '\n') 
            """
            return ci_list

def calculate_rankall(method, infile, w2v_outfile, wn_outfile):
    outfile = ''
    with open(infile , 'r') as fp: 
        reader = csv.reader(fp)
        header = next(reader)
        pIndex = header.index("property")
        sIndex = header.index("source")
        tIndex = header.index("target")
    
        for row in reader:
           if row:
              prop = row[pIndex]
              source = row[sIndex]
              target = row[tIndex]
              #make a list 
              prop = prop.strip('\'')
              prop = prop.strip(' ')
              plist = prop.split(",")
              plist = [x.strip(' ') for x in plist]
              #print(plist)

              #word2vec deep learning
              if method == 'w2v':
                  sim_src , sim_trg = w2v_similarity(plist, source, target , 'w2vpmodel')   
                  outfile = w2v_outfile
                    
        
              #wordnet
              else:
                  sim_src , sim_trg = wordnet_similarity(plist, source, target)
                  outfile = wn_outfile
              
              # rank 
              rank_list = rank(sim_src, sim_trg, source, target)
              writeTocsv(source, target, rank_list,outfile)
              ######################### 
