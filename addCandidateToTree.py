# -*- coding: utf-8 -*-
import parse_articles
import parse_taxonomy
from gensim.models import Doc2Vec
from gensim.models.doc2vec import LabeledSentence
import numpy
import re
import uuid
from keywords_patrick import get_keywords
"""
Created on Fri Nov 24 17:02:53 2017

"""
def importCandidates():
    #TODO: Process listOfCandidates
    #TODO: Return the post-processed listofCandidates
    return get_keywords(articles= parse_articles.parse_articles_from_file('Data/News300.txt'), taxonomy= parse_taxonomy.parse_taxonomy_form_file('michaelData/T0.csv'))
    #["Disaster", "Google", "NASDAQ", "Merkel"] #meanwhile we return some words

def importTree():
    return parse_taxonomy.parse_taxonomy_form_file('michaelData/T0.csv')

def importArticleForTraining():
    return parse_articles.parse_articles_from_file('Data/News300.txt')

def prepareGensim():
    trainingSet = importArticleForTraining()
    trainingProcessed = []
    print("Model Start the training!")
    for e in trainingSet:
        eTags = e['topicsDescription']
        eTags = [item.lower() for item in eTags]
        eWords =  re.sub("[^\w]", " ",  e['story']).split() # look for nltk tokenizer
        eWords = [item.lower() for item in eWords]
        #eWords = [item.lower() for sublist in eWords for item in sublist]
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
    tree = importTree()
    for candidate in filter(lambda x: x in model.wv.vocab, importCandidates()):
        (leaf, maxSimilarity) = findNode(tree, candidate.lower(), model, -1, -1)
        print("--")
        print(candidate, leaf.tag, maxSimilarity)
        print("--")
        tree.create_node(candidate, uuid.uuid4(), parent=leaf.identifier)
    return tree

def findNode(tree, candidate, model, maxSimilarityFound, bestNodeFound):
# =============================================================================
#     print("findNode")
#     print(maxSimilarityFound, bestNodeFound)
# =============================================================================
    if len(tree.children(tree.root)) == 0: #if we are at a leaf, so node = tree   
        return compareCurrentNodeWithPreviousBest(tree, tree.get_node(tree.root), maxSimilarityFound, bestNodeFound, model, candidate)
    else:
        bestChildNode = None
        bestChildMaxSimilarityFound = -1
        for child in tree.children(tree.root):
            if(bestChildMaxSimilarityFound > maxSimilarityFound):
                (bestChildNode, bestChildMaxSimilarityFound) = compareCurrentNodeWithPreviousBest(tree, child, bestChildMaxSimilarityFound, bestChildNode, model, candidate)
            else:
                (bestChildNode, bestChildMaxSimilarityFound) = compareCurrentNodeWithPreviousBest(tree, child, maxSimilarityFound, bestNodeFound, model, candidate)

        if(bestChildMaxSimilarityFound > maxSimilarityFound): # if we found a child with something better, we go there

             (bestNodeFound, maxSimilarityFound) = findNode(tree.subtree(bestChildNode.identifier), candidate, model, bestChildMaxSimilarityFound, bestChildNode)

    return (bestNodeFound, maxSimilarityFound)
    
def compareCurrentNodeWithPreviousBest(tree, node, maxSimilarityFound, bestNodeFound, model, candidate):
    listOfWordsToAnalyze = []
    similarityPerWordOfNode = []
    
    if len(tree.children(node.identifier)) == 0: #if we are at a leaf
        listOfWordsToAnalyze.append([node.tag.split(" "),1])
    else:
        treeDepth = tree.depth()
        for aNode in tree.subtree(node.identifier).all_nodes():
            aNodeDepth = tree.depth(aNode)
            aNodeCoefficient = treeDepth - aNodeDepth
            currentList = aNode.tag.split(" ")
            aNodeToAnalyze = []
            for e in currentList:
                aNodeToAnalyze.append([e, aNodeCoefficient])
            listOfWordsToAnalyze.extend(aNodeToAnalyze)
    for word, nodeCoefficient in listOfWordsToAnalyze:  
        for wordPerChild in filter(lambda x: x in model.wv.vocab, word):
            similarityPerWordOfNode.append([model.similarity(wordPerChild, candidate),nodeCoefficient])
        
    if not similarityPerWordOfNode:
        similarityPerWordOfNode = [[0,1]]
    similarityValue = [b[0] for b in similarityPerWordOfNode]
    similarityCoefficient = [b[1] for b in similarityPerWordOfNode]
    weightedAverage = numpy.average(similarityValue, weights= similarityCoefficient)
    if(weightedAverage > maxSimilarityFound):
        maxSimilarityFound = weightedAverage   
        bestNodeFound = node
    return (bestNodeFound, maxSimilarityFound)


insertCandidateToTree()