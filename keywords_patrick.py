from collections import defaultdict
from gensim import corpora, models

def get_keywords(articles, taxonomy):

    # load text
    from textblob import TextBlob

    texts = list()
    for article in articles:
        blob = TextBlob(article['headLine'] + " " + article['story'])
        #texts = blob.words.singularize()
        phrases = blob.noun_phrases
        thisText = list()
        for phrase in phrases:
            thisText.append(phrase)
        texts.append(thisText)

    # intitialize stoplists
    import nltk
    nltk.download("stopwords")
    from nltk.corpus import stopwords
    stoplist = stopwords.words('english')

    stoplist += ['fitch', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'said', 'would']

    newTexts = list()
    for text in texts:
        newText = list()
        for word in text:
            if word not in stoplist:
                newText.append(word)
        newTexts.append(newText)
    texts = newTexts

    # remove words that appear only once
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    # create dictionary
    #print(texts)
    dictionary = corpora.Dictionary(texts)
    dictionary.save('patrick/dict.txt')  # store the dictionary, for future reference

    # create corpus
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('patrick/corpus.txt', corpus)  # store to disk, for later use

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    weights = [0 for key in dictionary]

    for doc in corpus_tfidf:
        for word in doc:
            weights[word[0]] = weights[word[0]] + word[1]

    wordWeights = list()
    i = 0
    for w in weights:
        wordWeights.append((w, dictionary[i]))
        i += 1

    wordWeights = sorted(wordWeights, key=lambda wordWeight: wordWeight[0], reverse=True)

    #return [word[1] for word in wordWeights]

    tags = set([node.tag.lower() for node in taxonomy.all_nodes_itr()])

    suggestions = list()
    for wordWeight in wordWeights:
        weight = wordWeight[0]
        word = wordWeight[1]
        if((word not in tags) and (weight > 0.2) and len(word) > 4):
            ok = True
            for tag in tags:
                if word in tag:
                    ok = False
                if tag in word:
                    ok = False
            if ok:
                suggestions.append(word)
    return suggestions


# from parse_taxonomy import parse_taxonomy_form_file
# from parse_articles import parse_articles_from_url
# taxonomy = parse_taxonomy_form_file("michaelData/T0.csv")
# articles = parse_articles_from_url('https://hackathon17.mope.ml/HackathonSite/News300.txt')
# 
# print(get_keywords(articles, taxonomy))