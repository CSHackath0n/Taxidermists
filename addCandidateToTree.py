# -*- coding: utf-8 -*-
import parse_articles
import parse_taxonomy
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import re

"""
Created on Fri Nov 24 17:02:53 2017

@author: michael
"""
def importCandidates(listOfCandidate):
    #TODO: Process listOfCandidates
    #TODO: Return the post-processed listofCandidates
    return ["Coupon", "Derivative", "NASDAQ"] #meanwhile we return some words

def importTree():
    return parse_taxonomy.parse_taxonomy_form_file('Data/T0.csv')

def importArticleForTraining():
    return parse_articles.parse_articles_from_file('Data/NewsAll.txt')

def prepareGensim():
    trainingSet = importArticleForTraining()
    trainingProcessed = []
    print("Hello")
    for e in trainingSet:
        eTags = e['topicsDescription']
        eWords =  re.sub("[^\w]", " ",  e['story']).split() # look for nltk tokenizer
        eDocument = LabeledSentence(words = eWords, tags = eTags)
        trainingProcessed.append(eDocument)
        
    model = Doc2Vec(size=100, min_count=3, workers=3)
    model.build_vocab(trainingProcessed)
    
    #training of model
    model.train(trainingProcessed, total_examples=len(trainingProcessed), epochs=100)

    
    model.save("doc2vec.model")
    print("model saved")
    
    return model
    
    
def insertCandidateToTree(): 
    model = prepareGensim()
    candidate = "coupon"
    leaf = findLeaf(importTree(), candidate, model)
    print(leaf.tag)
    
def findLeaf(tree, candidate, model):
    if len(tree.children(tree.root)) > 0:
        maxSimilarityFound = 0
        bestChild = ''
        for child in tree.children(tree.root):
            if(model.similarity(child.tag, candidate) > maxSimilarityFound):
                maxSimilarityFound = model.similarity(child.tag, candidate)
                bestChild = child
        return bestChild
    else:
        return tree
    