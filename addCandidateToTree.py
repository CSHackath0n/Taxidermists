# -*- coding: utf-8 -*-
import parse_articles
import parse_taxonomy
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import numpy
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
    return parse_taxonomy.parse_taxonomy_form_file('michaelData/T0.csv')

def importArticleForTraining():
    return parse_articles.parse_articles_from_file('Data/News300.txt')

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
    leaf = findLeaf(importTree(), candidate, model, -1, -1)
    print(leaf.tag)
    
def findLeaf(tree, candidate, model, maxSimilarityFound, bestChild):
    if len(tree.children(tree.root)) > 0:
        for child in tree.children(tree.root):
            similarityPerWordOfChild = []
            
            for wordPerChild in filter(lambda x: x in model.wv.vocab, child.tag.split(" ")): # if we have multiple words
                similarityPerWordOfChild.append(model.similarity(wordPerChild, candidate))
            if not similarityPerWordOfChild:
                similarityPerWordOfChild = [0]
            if(numpy.mean(similarityPerWordOfChild) > maxSimilarityFound):
                maxSimilarityFound = numpy.mean(similarityPerWordOfChild)    
                bestChild = child
                print("HEY")
                print(maxSimilarityFound,bestChild.tag)
            print("---")
            print("---")
            print(maxSimilarityFound, bestChild)
            print("---")
            bestChild = findLeaf(tree.subtree(child.identifier), candidate, model, maxSimilarityFound, bestChild)

    else:
        similarityPerWordOfChild = []
        for wordPerChild in filter(lambda x: x in model.wv.vocab, tree.all_nodes()[0].tag.split(" ")): # if we have multiple words
            similarityPerWordOfChild.append(model.similarity(wordPerChild, candidate))
        if not similarityPerWordOfChild:
            similarityPerWordOfChild = [0]
        if(numpy.mean(similarityPerWordOfChild) > maxSimilarityFound):
            maxSimilarityFound = numpy.mean(similarityPerWordOfChild)    
            bestChild = tree.all_nodes()[0].tag
    return bestChild    


insertCandidateToTree()