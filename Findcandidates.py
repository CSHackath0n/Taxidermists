import sklearn.feature_extraction.text
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from nltk import word_tokenize
stopwords = set(stopwords.words('english'))


params: {story: 
            {ngram_range: (0,1)
            stop_words: stopwords
            tokenizer: tokenizer()
            analyzer: 'word'
            
             
             
             
             
             
             
             }
    
    
    
    
    
    }


def tokenizer(x):
    return ( w for w in word_tokenize(x) if len(w) > 3)

def dummytokenizer(x):
    return x

def find_candidates(article_key): 
  
    text = [article[article_key] for article in article_dict]
    
    sklearn_tfidf = TfidfVectorizer(ngram_range = (0,1), stop_words= stopwords, tokenizer=tokenizer, analyzer = 'word')
    X = sklearn_tfidf.fit_transform(text)
    idf = sklearn_tfidf.idf_
    result = pd.DataFrame(
            list(zip(sklearn_tfidf.get_feature_names(), idf)),
            columns=("words","tfidf")
            )
    result = result.sort_values("tfidf", ascending=False)
    
    return result

# print(find_candidates("story"))


stories_tfidf = find_candidates("story")
stories_tfidf.sort_values("tfidf", ascending=False)
stories_top100=stories_tfidf[0:100]
headlines_tfidf = find_candidates("headLine")
headlines_tfidf.sort_values("tfidf", ascending=False)
headlines_top100=headlines_tfidf[0:100]
topicdescriptions_tfidf = find_candidates("topicsDescription")



