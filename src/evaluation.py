# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 17:04:51 2018
@author: Tahereh
"""
from simUtil import mean_wordnet_similarity_lists, mean_w2v_similarity_lists, max_wordnet_similarity_lists,median_wordnet_similarity_lists, getSynonyms, isAdjective
import csv 
from numpy import median

def getBestRank(medrank1, medrank2, medrank3):
                               
    if (medrank1 == 0) & (medrank2 == 0) & (medrank3 == 0):
        rankbestP = 101
        
    elif (medrank3 == 0) & (medrank2 == 0):
        rankbestP = medrank1
        #bestItem = item1
        
    elif (medrank3 == 0) & (medrank2 != 0):    
        rankbestP = min(medrank1, medrank2) 
        
    else:
        rankbestP = min(medrank1, medrank2, medrank3) 
       
    return rankbestP
    
def getBestItem(sim1, sim2, sim3, rank1, rank2, rank3, item1, item2,item3):
    threshold = 0.7
    maximum = max(sim1, sim2, sim3)                                
    if (maximum == sim1) & (sim1 >= threshold):
        bestItem = item1 
    elif (maximum == sim2) & (sim2 >= threshold):
        bestItem = item2 
    elif (maximum == sim3) & (sim3 >= threshold):
        bestItem = item3 
    else:
        bestItem = ''
    
    if (sim1 == sim2) & (sim2 == sim3) & (sim1 >= threshold):
        minimum = min(rank1, rank2, rank3)
        if minimum == rank1:
            bestItem = item1
        elif minimum == rank2:
            bestItem = item2
        else:
            bestItem = item3
            
    elif (sim1 == sim2) & (sim1 >= threshold): 
        minimum = min(rank1, rank2)
        if rank1 == minimum: 
            bestItem = item1
        else:
            bestItem = item2
            
    elif (sim1 == sim3) & (sim1 >= threshold):
        minimum = min(rank1, rank3)
        if rank1 == minimum: 
            bestItem = item1
        else:
            bestItem = item3
    elif (sim2 == sim3) & (sim2 >= threshold) :
        minimum = min(rank2, rank3)
        if rank2 == minimum: 
            bestItem = item2
        else:
            bestItem = item3     
    return bestItem        
                                        
def getAvgRankForExactCandidates(method, inter_infile1  , inter_outfile, union_infile1 , union_outfile , infile2):
    
    if method == 'union':
        infile1 = union_infile1   
        outfile = union_outfile
       
    else:   
        infile1 = inter_infile1
        outfile = inter_outfile
                    
     
    with open(infile1 , 'r') as csv_file: 
         reader = csv.reader(csv_file, delimiter=",")    
         header = next(reader)
         t100Index = header.index("top100")
         srcIndex = header.index("source")
         trgIndex = header.index("target")

    
         for row in reader:
            if row:
                   top100 = row[t100Index]
                   source = row[srcIndex]
                   target = row[trgIndex]
                   t100lis = top100.split(",") 
                   
                   with open(infile2 , 'r') as csv_file2: 
                        reader2 = csv.reader(csv_file2, delimiter=",")
                        header2 = next(reader2)
                        P1Index = header2.index("p1")
                        P2Index = header2.index("p2")
                        P3Index = header2.index("p3")
                        P1PIndex = header2.index("p1props")
                        P2PIndex = header2.index("p2props")
                        P3PIndex = header2.index("p3props")
                        srcIdx = header2.index("source")
                        for row2 in reader2:
                          if row2:                              
                            if (source.lower() == row2[srcIdx].lower()):
                                p1 = row2[P1Index]
                                p2 = row2[P2Index]
                                p3 = row2[P3Index]
                                p1props = row2[P1PIndex]
                                p2props = row2[P2PIndex]
                                p3props = row2[P3PIndex]
                                p1propslis = p1props.split(",") 
                                p2propslis = p2props.split(",") 
                                p3propslis = p3props.split(",") 
                                
                                ######################
                                rankListP1 = {}
                                for p in p1propslis:
                                    if p.lower() in t100lis:
                                         prank = t100lis.index(p.lower())   
                                         #print(p1 , p , '***' , prank)
                                    else:
                                         prank = 101
                                         #print(p1 , p , '---' , prank)
                                         
                                    rankListP1[p.lower()] = prank   
                                
                                rankListP1val = list(rankListP1.values())
                                rankavgP1 = sum(rankListP1val)/len(rankListP1val)
                                rankminP1 = min(rankListP1val)
                                minP1 = min(rankListP1, key=rankListP1.get)
                                #print(rankminP1 , minP1 , rankavgP1)
                                ######################  
                                rankListP2 = {}
                                for p in p2propslis:
                                    if p.lower() in t100lis:
                                         prank = t100lis.index(p.lower()) 
                                    else:
                                         prank = 101
                                         
                                    rankListP2[p.lower()] = prank  
                                    
                                rankListP2val = list(rankListP2.values())
                                rankavgP2 = sum(rankListP2val)/len(rankListP2val)
                                rankminP2 = min(rankListP2val)
                                minP2 = min(rankListP2, key=rankListP2.get)   
                                ######################  
                                rankListP3 = {}
                                for p in p3propslis:
                                    if p.lower() in t100lis:
                                         prank = t100lis.index(p.lower())  
                                    else:
                                         prank = 101
                                         
                                    rankListP3[p.lower()] = prank   
                                
                                rankListP3val = list(rankListP3.values())
                                rankavgP3 = sum(rankListP3val)/len(rankListP3val)
                                rankminP3 = min(rankListP3val)
                                minP3 = min(rankListP3, key=rankListP3.get)  
                                ######################    
                                rankbestP = min(rankavgP1, rankavgP2, rankavgP3)                                
                                ######################
                               
                                meansimP1 = mean_wordnet_similarity_lists(t100lis,p1propslis)
                                meansimP2 = mean_wordnet_similarity_lists(t100lis,p2propslis)
                                meansimP3 = mean_wordnet_similarity_lists(t100lis,p3propslis)
                                    
                                maxsim = max(meansimP1, meansimP2, meansimP3)    
                                #print(rankListP1)
                                ######################
                                with open(outfile,'a') as file:
                                    writer = csv.writer(file)
                                    min1 = minP1 + ':' + str(rankminP1)
                                    min2 = minP2 + ':' + str(rankminP2)
                                    min3 = minP3 + ':' + str(rankminP3)
                                    writer.writerow([source, target, p1 , p2 , p3 , rankavgP1  , min1  , rankavgP2 , 
                                                    min2 ,  rankavgP3, min3, rankbestP , meansimP1, meansimP2, meansimP3, maxsim])
    
def getMedianRankForExactCandidates(method, inter_infile1  , inter_outfile, union_infile1 , union_outfile , infile2):
    
    if method == 'union':
        infile1 = union_infile1   
        outfile = union_outfile
       
    else:   
        infile1 = inter_infile1
        outfile = inter_outfile
             
     
    with open(infile1 , 'r') as csv_file: 
         reader = csv.reader(csv_file, delimiter=",")    
         header = next(reader)
         t100Index = header.index("top100")
         srcIndex = header.index("source")
         trgIndex = header.index("target")

    
         for row in reader:
            if row:
                   top100 = row[t100Index]
                   source = row[srcIndex]
                   target = row[trgIndex]
                   t100lis = top100.split(",") 
                   
                   with open(infile2 , 'r') as csv_file2: 
                        reader2 = csv.reader(csv_file2, delimiter=",")
                        header2 = next(reader2)
                        P1Index = header2.index("p1")
                        P2Index = header2.index("p2")
                        P3Index = header2.index("p3")
                        P1PIndex = header2.index("p1props")
                        P2PIndex = header2.index("p2props")
                        P3PIndex = header2.index("p3props")
                        srcIdx = header2.index("source")
                        for row2 in reader2:
                          if row2:                              
                            if (source.lower() == row2[srcIdx].lower()):
                                p1 = row2[P1Index]
                                p2 = row2[P2Index]
                                p3 = row2[P3Index]
                                p1props = row2[P1PIndex]
                                p2props = row2[P2PIndex]
                                p3props = row2[P3PIndex]
                                p1propslis = p1props.split(",") 
                                p2propslis = p2props.split(",") 
                                p3propslis = p3props.split(",") 
                                
                                ######################
                                rankListP1 = {}
                                for p in p1propslis:
                                    if p.lower() in t100lis:
                                         prank = t100lis.index(p.lower())   
                                         #print(p1 , p , '***' , prank)
                                    else:
                                         prank = 101
                                         #print(p1 , p , '---' , prank)
                                         
                                    rankListP1[p.lower()] = prank   
                                
                                rankListP1val = list(rankListP1.values())
                                #rankavgP1 = sum(rankListP1val)/len(rankListP1val)
                                rankListP1val = sorted(rankListP1val)
                                rankmeadianP1 = median(rankListP1val)
                                rankminP1 = min(rankListP1val)
                                minP1 = min(rankListP1, key=rankListP1.get)
                                #print(rankminP1 , minP1 , rankavgP1)
                                ######################  
                                rankListP2 = {}
                                for p in p2propslis:
                                    if p.lower() in t100lis:
                                         prank = t100lis.index(p.lower()) 
                                    else:
                                         prank = 101
                                         
                                    rankListP2[p.lower()] = prank  
                                    
                                rankListP2val = list(rankListP2.values())
                                #rankavgP2 = sum(rankListP2val)/len(rankListP2val)
                                rankListP2val = sorted(rankListP2val)
                                rankmeadianP2 = median(rankListP2val)
                                rankminP2 = min(rankListP2val)
                                minP2 = min(rankListP2, key=rankListP2.get)   
                                ######################  
                                rankListP3 = {}
                                for p in p3propslis:
                                    if p.lower() in t100lis:
                                         prank = t100lis.index(p.lower())  
                                    else:
                                         prank = 101
                                         
                                    rankListP3[p.lower()] = prank   
                                
                                rankListP3val = list(rankListP3.values())
                                #rankavgP3 = sum(rankListP3val)/len(rankListP3val)
                                rankListP3val = sorted(rankListP3val)
                                rankmeadianP3 = median(rankListP3val)
                                rankminP3 = min(rankListP3val)
                                minP3 = min(rankListP3, key=rankListP3.get)  
                                ######################    
                                rankbestP = min(rankmeadianP1, rankmeadianP2, rankmeadianP3)                                
                                ######################
                               
                                meansimP1 = mean_wordnet_similarity_lists(t100lis,p1propslis)
                                meansimP2 = mean_wordnet_similarity_lists(t100lis,p2propslis)
                                meansimP3 = mean_wordnet_similarity_lists(t100lis,p3propslis)
                                
                                
                                    
                                maxsim = max(meansimP1, meansimP2, meansimP3)    
                                #print(rankmeadianP1)
                                ######################
                                with open(outfile,'a') as file:
                                    writer = csv.writer(file)
                                    min1 = minP1 + ':' + str(rankminP1)
                                    min2 = minP2 + ':' + str(rankminP2)
                                    min3 = minP3 + ':' + str(rankminP3)
                                    writer.writerow([source, target, p1 , p2 , p3 , rankmeadianP1  , min1  , rankmeadianP2 , 
                                                    min2 ,  rankmeadianP3, min3, rankbestP , meansimP1, meansimP2, meansimP3, maxsim])    

def getAvgRankForSimilarCandidates(method, inter_infile1  , inter_outfile, union_infile1 , union_outfile , infile2):
    #only for wordnet

    if method == 'union':
        infile1 = union_infile1   
        outfile = union_outfile
       
    else:   
        infile1 = inter_infile1
        outfile = inter_outfile
       
     
    with open(infile1 , 'r') as csv_file: 
         reader = csv.reader(csv_file, delimiter=",")    
         header = next(reader)         
         srcIndex = header.index("source")
         trgIndex = header.index("target")         
         t100Index = header.index("top100")

    
         for row in reader:
            if row:
                   top100 = row[t100Index]
                   source = row[srcIndex]
                   target = row[trgIndex]
                   t100lis = top100.split(",") 
                   
                   with open(infile2 , 'r') as csv_file2: 
                        reader2 = csv.reader(csv_file2, delimiter=",")
                        header2 = next(reader2)
                        P1Index = header2.index("p1")
                        P2Index = header2.index("p2")
                        P3Index = header2.index("p3")
                        P1PIndex = header2.index("p1props")
                        P2PIndex = header2.index("p2props")
                        P3PIndex = header2.index("p3props")
                        srcIdx = header2.index("source")
                        for row2 in reader2:
                          if row2:                              
                            if (source.lower() == row2[srcIdx].lower()):
                                p1 = row2[P1Index]
                                p2 = row2[P2Index]
                                p3 = row2[P3Index]
                                p1props = row2[P1PIndex]
                                p2props = row2[P2PIndex]
                                p3props = row2[P3PIndex]
                                p1propslis = p1props.split(",") 
                                p2propslis = p2props.split(",") 
                                p3propslis = p3props.split(",")                                 
                                ######################                                
                                item1, sim1, rank1, meanrank1 , meansimP1 = max_wordnet_similarity_lists(t100lis , p1propslis)                                  
                                item2, sim2, rank2, meanrank2 , meansimP2 = max_wordnet_similarity_lists(t100lis , p2propslis)
                                item3, sim3, rank3, meanrank3, meansimP3 = max_wordnet_similarity_lists(t100lis , p3propslis)
                                
                                
                                if (meanrank3 == 0) & (meanrank2 == 0) & (meanrank1 == 0):
                                    rankbestP = 101
                                    bestItem = ''
                                    
                                elif (meanrank3 == 0) & (meanrank2 == 0):
                                    rankbestP = meanrank1
                                    bestItem = item1
                                    
                                elif (meanrank3 == 0) & (meanrank2 != 0):    
                                    rankbestP = min(meanrank1, meanrank2) 
                                    if rankbestP == meanrank1:
                                        bestItem = item1
                                    else:
                                        bestItem = item2
                                else:
                                    rankbestP = min(meanrank1, meanrank2, meanrank3) 
                                    if rankbestP == meanrank1:
                                        bestItem = item1
                                    elif rankbestP == meanrank2:
                                        bestItem = item2
                                    else:
                                        bestItem = item3
                                
                                maxsim = max(meansimP1, meansimP2, meansimP3)   
                                
                                print(item1, sim1 , rank1 , meanrank1 , meansimP1)
                                ######################
                                
                                with open(outfile,'a') as file:
                                    writer = csv.writer(file)                                    
                                    writer.writerow([source, target, p1 , p2 , p3 , meanrank1 ,item1 , rank1 , sim1  , meanrank2 , 
                                                    item2, rank2 , sim2 ,  meanrank3 , item3, rank3 , sim3, bestItem , rankbestP , meansimP1, meansimP2, meansimP3, maxsim])

def getMedianRankForSimilarCandidates(method, inter_infile1  , inter_outfile, union_infile1 , union_outfile , infile2):
    if method == 'union':
        infile1 = union_infile1   
        outfile = union_outfile
       
    else:   
        infile1 = inter_infile1
        outfile = inter_outfile
       
     
    with open(infile1 , 'r') as csv_file: 
         reader = csv.reader(csv_file, delimiter=",")    
         header = next(reader)         
         srcIndex = header.index("source")
         trgIndex = header.index("target")         
         t100Index = header.index("top100")

    
         for row in reader:
            if row:
                   top100 = row[t100Index]
                   source = row[srcIndex]
                   target = row[trgIndex]
                   t100lis = top100.split(",") 
                   
                   with open(infile2 , 'r') as csv_file2: 
                        reader2 = csv.reader(csv_file2, delimiter=",")
                        header2 = next(reader2)
                        P1Index = header2.index("p1")
                        P2Index = header2.index("p2")
                        P3Index = header2.index("p3")
                        P1PIndex = header2.index("p1props")
                        P2PIndex = header2.index("p2props")
                        P3PIndex = header2.index("p3props")
                        srcIdx = header2.index("source")
                        for row2 in reader2:
                          if row2:                              
                            if (source.lower() == row2[srcIdx].lower()):
                                p1 = row2[P1Index]
                                p2 = row2[P2Index]
                                p3 = row2[P3Index]
                                p1props = row2[P1PIndex]
                                p2props = row2[P2PIndex]
                                p3props = row2[P3PIndex]
                                p1propslis = p1props.split(",") 
                                p2propslis = p2props.split(",") 
                                p3propslis = p3props.split(",")                                 
                                ######################                                
                                item1, sim1, rank1, medrank1 , meansimP1 = median_wordnet_similarity_lists(t100lis , p1propslis)                                  
                                item2, sim2, rank2, medrank2 , meansimP2 = median_wordnet_similarity_lists(t100lis , p2propslis)
                                item3, sim3, rank3, medrank3, meansimP3 = median_wordnet_similarity_lists(t100lis , p3propslis)
                                
                                #######################
                                bestItem = getBestItem(sim1, sim2, sim3, rank1, rank2, rank3, item1, item2,item3)                        
                                rankbestP = getBestRank(medrank1, medrank2, medrank3)
                                maxsim = max(meansimP1, meansimP2, meansimP3)  
                                print(bestItem , rankbestP , maxsim )
                                ######################
                                
                                with open(outfile,'a') as file:
                                    writer = csv.writer(file)                                    
                                    writer.writerow([source, target, p1 , p2 , p3 , medrank1 ,item1 , rank1 , sim1  , medrank2 , 
                                                    item2, rank2 , sim2 ,  medrank3 , item3, rank3 , sim3, bestItem , rankbestP , meansimP1, meansimP2, meansimP3, maxsim])

                               
def getAvgRankForGTForSimilarCandidates(method, inter_infile1  , inter_outfile, union_infile1 , union_outfile , infile2):
    #only for wordnet

    if method == 'union':
        infile1 = union_infile1   
        outfile = union_outfile
       
    else:   
        infile1 = inter_infile1
        outfile = inter_outfile
       
     
    with open(infile1 , 'r') as csv_file: 
         reader = csv.reader(csv_file, delimiter=",")    
         header = next(reader)         
         srcIndex = header.index("source")
         trgIndex = header.index("target")         
         t100Index = header.index("top100")

    
         for row in reader:
            if row:
                   top100 = row[t100Index]
                   source = row[srcIndex]
                   target = row[trgIndex]
                   t100lis = top100.split(",") 
                   
                   with open(infile2 , 'r') as csv_file2: 
                        reader2 = csv.reader(csv_file2, delimiter=",")
                        header2 = next(reader2)
                        P1Index = header2.index("p1")
                        P2Index = header2.index("p2")
                        P3Index = header2.index("p3")                       
                        srcIdx = header2.index("source")
                        for row2 in reader2:
                          if row2:                              
                            if (source.lower() == row2[srcIdx].lower()):
                                p1 = row2[P1Index]
                                p2 = row2[P2Index]
                                p3 = row2[P3Index]                               
                                p1propslis = p1.split(",") 
                                p2propslis = p2.split(",") 
                                p3propslis = p3.split(",")                                 
                                ######################                                
                                item1, sim1, rank1, meanrank1 , meansimP1 = max_wordnet_similarity_lists(t100lis , p1propslis)                                  
                                item2, sim2, rank2, meanrank2 , meansimP2 = max_wordnet_similarity_lists(t100lis , p2propslis)
                                item3, sim3, rank3, meanrank3, meansimP3 = max_wordnet_similarity_lists(t100lis , p3propslis)
                                
                                
                                if (meanrank3 == 0) & (meanrank2 == 0) & (meanrank1 == 0):
                                    rankbestP = 101
                                    bestItem = ''
                                    
                                elif (meanrank3 == 0) & (meanrank2 == 0):
                                    rankbestP = meanrank1
                                    bestItem = item1
                                    
                                elif (meanrank3 == 0) & (meanrank2 != 0):    
                                    rankbestP = min(meanrank1, meanrank2) 
                                    if rankbestP == meanrank1:
                                        bestItem = item1
                                    else:
                                        bestItem = item2
                                else:
                                    rankbestP = min(meanrank1, meanrank2, meanrank3) 
                                    if rankbestP == meanrank1:
                                        bestItem = item1
                                    elif rankbestP == meanrank2:
                                        bestItem = item2
                                    else:
                                        bestItem = item3
                                
                                maxsim = max(meansimP1, meansimP2, meansimP3)   
                                
                                print(item1, sim1 , rank1 , meanrank1 , meansimP1)
                                ######################
                                
                                with open(outfile,'a') as file:
                                    writer = csv.writer(file)                                    
                                    writer.writerow([source, target, p1 , p2 , p3 , meanrank1 ,item1 , rank1 , sim1  , meanrank2 , 
                                                    item2, rank2 , sim2 ,  meanrank3 , item3, rank3 , sim3, bestItem , rankbestP , meansimP1, meansimP2, meansimP3, maxsim])
                                   
if __name__ == '__main__':
    
    api = "cn" #cn or dm
    infile2 = api + '_GTProps_props_wordnet.csv'    
    union_infile1 = api + '_ranked_props_wordnet_union.csv' 
    inter_infile1 = api + '_ranked_props_wordnet_inter.csv'    
    method = 'union' #inter
    """  
    union_outfile = api + '_dataset_wordnet_union_exact.csv'  
    inter_outfile = api + '_dataset_wordnet_inter_exact.csv'
    getAvgRankForExactCandidates(method , inter_infile1 , inter_outfile, union_infile1 , union_outfile   , infile2 )
    """
    """
    union_outfile = api + '_dataset_wordnet_union_exact_median.csv'      
    inter_outfile = api + '_dataset_wordnet_inter_exact_median.csv'
    getMedianRankForExactCandidates(method , inter_infile1 , inter_outfile, union_infile1 , union_outfile   , infile2 )
    """
    
    """
    union_outfile = api + '_dataset_wordnet_union.csv'      
    inter_outfile = api + '_dataset_wordnet_inter.csv'
    getAvgRankForSimilarCandidates(method , inter_infile1 , inter_outfile, union_infile1 , union_outfile   , infile2 ) 
    """
    
    
    #++++++++++++++most similar , median, with threshold
    
    union_outfile = api + '_dataset_wordnet_union_median.csv'       
    inter_outfile = api + '_dataset_wordnet_inter_median.csv'
    getMedianRankForSimilarCandidates(method , inter_infile1 , inter_outfile, union_infile1 , union_outfile   , infile2 )  
    
       


 
    
    