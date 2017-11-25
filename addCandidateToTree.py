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
    (leaf, maxSimilarity) = findNode(importTree(), candidate, model, -1, -1)
    print(leaf.tag)
    print(maxSimilarity)
    
# =============================================================================
#     
# def findLeaf(tree, candidate, model, maxSimilarityFound, bestChild):
#     if len(tree.children(tree.root)) > 0:
#         for child in tree.children(tree.root):
#             similarityPerWordOfChild = []
#             listOfWordsToAnalyze = child.tag.split(" ")
#             for grandchild in tree.subtree(child.identifier).all_nodes():
#                 listOfWordsToAnalyze.append(grandchild.tag)
#             for wordPerChild in filter(lambda x: x in model.wv.vocab, listOfWordsToAnalyze): # if we have multiple words
#                 similarityPerWordOfChild.append(model.similarity(wordPerChild, candidate))
#             
#             if not similarityPerWordOfChild:
#                 similarityPerWordOfChild = [0]
#             if(numpy.mean(similarityPerWordOfChild) > maxSimilarityFound):
#                 maxSimilarityFound = numpy.mean(similarityPerWordOfChild)    
#                 bestChild = child
#                 print("HEY")
#                 print(maxSimilarityFound,bestChild.tag)
#             print("---")
#             print("---")
#             print(maxSimilarityFound, bestChild)
#             print("We are at this node:")
#             print(child)
#             print("---")
#             (bestChild,maxSimilarityFound) = findLeaf(tree.subtree(child.identifier), candidate, model, maxSimilarityFound, bestChild)
# 
#     else:
#         similarityPerWordOfChild = []
#         for wordPerChild in filter(lambda x: x in model.wv.vocab, tree.all_nodes()[0].tag.split(" ")): # if we have multiple words
#             similarityPerWordOfChild.append(model.similarity(wordPerChild, candidate))
#         if not similarityPerWordOfChild:
#             similarityPerWordOfChild = [0]
#         if(numpy.mean(similarityPerWordOfChild) > maxSimilarityFound):
#             maxSimilarityFound = numpy.mean(similarityPerWordOfChild)    
#             bestChild = tree.all_nodes()[0]
#     return (bestChild,maxSimilarityFound)
# 
# =============================================================================

insertCandidateToTree()

def findNode(tree, candidate, model, maxSimilarityFound, bestNode):
    if len(tree.children(tree.root)) == 0: #if we are at a leaf, so node = tree   
        return compareCurrentNodeWithPreviousBest(tree, tree, maxSimilarityFound, bestNode, model, candidate)
    else:
        bestChildNode = None
        bestChildMaxSimilarityFound = -1
        for child in tree.children(tree.root):
            (bestChildNode, bestChildMaxSimilarityFound) = compareCurrentNodeWithPreviousBest(tree, child, maxSimilarityFound, bestNode, model, candidate)
        
        if(bestChildMaxSimilarityFound > maxSimilarityFound): # if we found a child with something better, we go there
            (bestNode, maxSimilarityFound) = findNode(tree.subtree(bestChildNode.identifier), candidate, model, bestChildMaxSimilarityFound, bestChildNode)

    return (bestNode, maxSimilarityFound)
    
def compareCurrentNodeWithPreviousBest(tree, node, maxSimilarityFound, bestNodeFound, model, candidate):
    listOfWordsToAnalyze = []
    similarityPerWordOfNode = []
    
    if len(tree.children(node.identifier)) == 0: #if we are at a leaf
        listOfWordsToAnalyze.extend(node.tag.split(" "))
    else:
        for aNode in tree.subtree(node.identifier).all_nodes():
            listOfWordsToAnalyze.extend(aNode.tag.split(" "))
            
    for wordPerChild in filter(lambda x: x in model.wv.vocab, listOfWordsToAnalyze): # if we have multiple words
        similarityPerWordOfNode.append(model.similarity(wordPerChild, candidate))
        
    if not similarityPerWordOfNode:
        similarityPerWordOfNode = [0]
        
    if(numpy.mean(similarityPerWordOfNode) > maxSimilarityFound):
        maxSimilarityFound = numpy.mean(similarityPerWordOfNode)    
        bestNodeFound = node
    return (bestNodeFound, maxSimilarityFound)