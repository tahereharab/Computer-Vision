# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 16:29:01 2018

@author: Tahereh
"""
from gensim.models import Word2Vec
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer
import re
import os
import nltk
import operator
from numpy import median



def getSynonyms(word):
    
    synonyms = [] 
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
        
    return list(set(synonyms))
    

def get_best_synset_pair(word_1, word_2):
    """ 
    Choose the pair with highest path similarity among all pairs. 
    """
    max_sim = -1.0
    synsets_1 = wordnet.synsets(word_1)
    synsets_2 = wordnet.synsets(word_2)
    
    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
               sim = wordnet.path_similarity(synset_1, synset_2)
               if sim:
                   if (sim > max_sim):
                       max_sim = sim
                       best_pair = synset_1, synset_2
        return best_pair
            
def text_to_vector(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]
            
def cosine_similarity(plist, source, target):
    sim_src = {}
    sim_trg = {}
    
    for word in plist:
        sim1 = cosdis(text_to_vector(source),text_to_vector(word))
        sim_src[word] = sim1
        if target:
           sim2 = cosdis(text_to_vector(target),text_to_vector(word))
           sim_trg[word] = sim2
           
    if sim_trg:     
       return sim_src, sim_trg   
    else:
        return sim_src

def w2v_similarity(plist, source, target ,modelname ):
    sim_src = {}
    sim_trg = {}
    sentences = [plist]
    #print(sentences)
    model = Word2Vec(sentences,iter=1, min_count=1)
    model.save(modelname)
    model = Word2Vec.load(modelname)
    for word in plist:
        sim1 = model.similarity(source, word)
        sim_src[word] = sim1
        
        if target:
           sim2 = model.similarity(target, word)
           sim_trg[word] = sim2
    
    os.remove(modelname)   
    if sim_trg:     
       return sim_src, sim_trg   
    else:
        return sim_src
    
def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    elif treebank_tag.startswith('I'):
        return wordnet.NOUN
    else:
        return ''

def isAdjective(word):
    text = nltk.word_tokenize(word)
    tagged = nltk.pos_tag(text)
    pos = get_wordnet_pos(tagged[0][1])
    #print(tagged , pos)
    if pos == 'a':
        return True
    else:
        return False
    
def lemmatization(word):
    if not word:
        return word
    
    text = nltk.word_tokenize(word)
    tagged = nltk.pos_tag(text)
    pos = get_wordnet_pos(tagged[0][1])
    wnl = WordNetLemmatizer()
    if pos:
       word = wnl.lemmatize(word , pos)
    return word

def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))    

def wordnet_similarity(plist, source, target):
    sim_src = {}
    sim_trg = {}
    
    for word in plist:
        source = source.replace(" ", "")
        word = word.replace(" ", "")
        
        src = lemmatization(source)
        
        if hasNumbers(word):
           w = word
        else:
           w = lemmatization(word)
           
        best_synset = get_best_synset_pair(w,src)
        w1 = best_synset[0]
        w2 = best_synset[1]
        
        if w1 :
            sim1 = w1.wup_similarity(w2)
            sim_src[word] = sim1
            
        else:
            sim_src[word] = 0   
           
           
        if target: 
            target = target.replace(" ", "")
            trg = lemmatization(target)   
            best_synset = get_best_synset_pair(w,trg)   
            w1 = best_synset[0]
            w2 = best_synset[1]
            if w1 :
                sim2 = w1.wup_similarity(w2)
                sim_trg[word] = sim2
            
            else:
               sim_trg[word] = 0
                      
           
    if sim_trg:     
       return sim_src, sim_trg   
    else:
        return sim_src
    
    
def mean_cosine_similarity_lists(list1, list2):
    
    sumsim = 0
    size = len(list1)* len(list2)
    for word1 in list1:
        for word2 in list2:
            sumsim = sumsim + abs(cosdis(text_to_vector(word1),text_to_vector(word2)))
            
    meansim = round(sumsim/size,3)
        
    return meansim

def mean_w2v_similarity_lists(list1, list2):
    sumsim = 0
    size = len(list1)* len(list2)
    flist = list1 + list2
    sentences = [flist]
    modelname = 'w2vmodelsim'
    model = Word2Vec(sentences,iter=1, min_count=1)
    model.save(modelname)
    model = Word2Vec.load(modelname)
    
    for word1 in list1:
        for word2 in list2:
            sumsim = sumsim + abs(model.similarity(word1, word2))
           
    meansim = round(sumsim/size,3)
    #os.remove(modelname)
        
    return meansim

def mean_wordnet_similarity_lists(list1, list2):
    sumsim = 0
    size = len(list1)* len(list2)

    for word1 in list1:
        for word2 in list2:
            
            word1 = word1.replace(" ", "")
            word2 = word2.replace(" ", "")
            
            if hasNumbers(word1):
                w1 = word1
            else:
                w1 = lemmatization(word1)
           
            if hasNumbers(word2):
                w2 = word2
            else:
                #print(word2)
                w2 = lemmatization(word2)
            
            best_synset = get_best_synset_pair(w1,w2)
            #print(w1 , w2 , best_synset)
            
            w1 = best_synset[0]
            w2 = best_synset[1]
            if w1 :             
                sim = w1.wup_similarity(w2)
                #print('sim = ' , sim )
            else:
                sim = 0
        
            sumsim = sumsim + sim
            
    meansim = round(sumsim/size,3)
   
    return meansim    


def max_wordnet_similarity_lists(list1, list2):
  simdict = {}
  sumrank = 0
  sumsim = 0
  meanrank = 0
  meansim = 0
  itemmax=  ''
  simmax = 0
  rankmax = 101
  if list1:  
    for word1 in list1:
        for word2 in list2:
            
            word11 = word1.replace(" ", "")
            word21 = word2.replace(" ", "")
            
            if hasNumbers(word11):
                w1 = word11
            else:
                w1 = lemmatization(word11)
           
            if hasNumbers(word21):
                w2 = word21
            else:
                #print(word2)
                w2 = lemmatization(word21)
            
            best_synset = get_best_synset_pair(w1,w2)
            #print(w1 , w2 , best_synset)
            valuelist = []
            w1 = best_synset[0]
            w2 = best_synset[1]
            
            if w1 :             #if word has synset we calculate the similarity
                if(word1.lower() == word2.lower()):
                    sim = 1.0
                    prank = min(list1.index(word1), list2.index(word2))                    
                else:    
                    sim = w1.wup_similarity(w2)
                    prank = list1.index(word1) 
                    
                valuelist = [round(sim,3), prank]                
                simdict[word1.lower()] = valuelist
                        
    sort_list = sorted(simdict.items(),key=operator.itemgetter(1) , reverse = True)  
    #print(sort_list)
    if sort_list:
      for i in range(0,len(sort_list)-1):
            sumrank = sumrank + sort_list[i][1][1]
            sumsim = sumsim + sort_list[i][1][0]
            
      meanrank = round(sumrank/len(sort_list),3)            
      meansim = round(sumsim/len(sort_list),3)
      #print(meanrank , meansim)
            
      if (len(sort_list) > 1): 
          if(sort_list[0][1][0] == sort_list[1][1][0]): #if the first two items have the same similarity
              simmax = sort_list[0][1][0]
              if sort_list[0][1][1] < sort_list[1][1][1]:
                  rankmax = sort_list[0][1][1]
                  itemmax = sort_list[0][0]
              else:
                  rankmax = sort_list[1][1][1]
                  itemmax = sort_list[1][0]
          else:   
              simmax = sort_list[0][1][0]
              rankmax = sort_list[0][1][1]
              itemmax = sort_list[0][0]       
      else:   
          simmax = sort_list[0][1][0]
          rankmax = sort_list[0][1][1]
          itemmax = sort_list[0][0]
  else:
       itemmax=  ''
       simmax = 0
       rankmax = 101
       meanrank = 101
       meansim = 0
       
       
  return itemmax, simmax, rankmax, meanrank, meansim

def median_wordnet_similarity_lists(list1, list2):
  simdict = {}
  sumsim = 0
  medianrank = 0
  meansim = 0
  itemmax=  ''
  simmax = 0
  rankmax = 101
  if list1:  
    for word1 in list1:
        for word2 in list2:
            
            word11 = word1.replace(" ", "")
            word21 = word2.replace(" ", "")
            
            if hasNumbers(word11):
                w1 = word11
            else:
                w1 = lemmatization(word11)
           
            if hasNumbers(word21):
                w2 = word21
            else:
                #print(word2)
                w2 = lemmatization(word21)
            
            best_synset = get_best_synset_pair(w1,w2)
            #print(w1 , w2 , best_synset)
            valuelist = []
            w1 = best_synset[0]
            w2 = best_synset[1]
            
            if w1 :             #if word has synset we calculate the similarity
                if(word1.lower() == word2.lower()):
                    sim = 1.0
                    prank = min(list1.index(word1), list2.index(word2))                    
                else:    
                    sim = w1.wup_similarity(w2)
                    prank = list1.index(word1) 
                    
                valuelist = [round(sim,3), prank]                
                simdict[word1.lower()] = valuelist
                        
    sort_list = sorted(simdict.items(),key=operator.itemgetter(1) , reverse = True)  
    #print(sort_list)
    ranklis = []
    if sort_list:
      for i in range(0,len(sort_list)-1):  
            sumsim = sumsim + sort_list[i][1][0]
            ranklis.append(sort_list[i][1][1])
       
      ranklis = sorted(ranklis) 
      #print(ranklis)       
      medianrank = median(ranklis)            
      meansim = round(sumsim/len(sort_list),3)
      #print(meanrank , meansim)
            
      if (len(sort_list) > 1): 
          if(sort_list[0][1][0] == sort_list[1][1][0]): #if the first two items have the same similarity
              simmax = sort_list[0][1][0]
              if sort_list[0][1][1] < sort_list[1][1][1]:
                  rankmax = sort_list[0][1][1]
                  itemmax = sort_list[0][0]
              else:
                  rankmax = sort_list[1][1][1]
                  itemmax = sort_list[1][0]
          else:   
              simmax = sort_list[0][1][0]
              rankmax = sort_list[0][1][1]
              itemmax = sort_list[0][0]       
      else:   
          simmax = sort_list[0][1][0]
          rankmax = sort_list[0][1][1]
          itemmax = sort_list[0][0]
  else:
       itemmax=  ''
       simmax = 0
       rankmax = 101
       medianrank = 101
       meansim = 0
       
       
  return itemmax, simmax, rankmax, medianrank, meansim