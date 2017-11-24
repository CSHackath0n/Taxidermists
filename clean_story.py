import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def tokenize_and_clean_story(article_dict):
    stories = []
    for i in range(len(article_dict)): 
        stories.append(article_dict[i].get("story"))

    stories_cleaned = []
    stories_stem = []
    for i in range(len(stories)):
        corpus = re.sub('[^a-zA-Z]', ' ', stories[i])
        corpus = corpus.lower()
        corpus = corpus.split()
        stories_cleaned.append(corpus)
        ps = PorterStemmer()
        corpus = [ps.stem(word) for word in corpus if not word in set(stopwords.words('english'))]
        corpus = ' '.join(corpus)
        stories_stem.append(corpus)
    return stories_cleaned    
        
cleaned_story = tokenize_and_clean_story(article_dict)
